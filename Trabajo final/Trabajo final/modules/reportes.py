import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.database import (
    obtener_reporte_ventas_por_fecha,
    obtener_ventas_por_metodo_pago,
    obtener_top_clientes_compras,
    productos_mas_vendidos,
)

# Constantes de diseño corporativo
BG_REPORTES = "#F8FAFC"       # Fondo general claro
CARD_BG = "#FFFFFF"          # Fondo de tarjetas y paneles
TEXT_PRIMARY = "#0F172A"      # Texto principal
TEXT_SECONDARY = "#64748B"    # Texto secundario/subtítulos
BORDER_COLOR = "#E2E8F0"      # Bordes suaves

# Paleta de color funcional / botones
BTN_PRIMARY = "#2563EB"       # Azul Corporativo
COLOR_HEADER = "#1E293B"      # Azul Oscuro / Slate
COLOR_EXCEL = "#059669"       # Verde Esmeralda (opcional para reportes)


class ReportesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_REPORTES)
        self.pack(expand=True, fill="both")
        self.crear_interfaz()
        self.filtrar_datos()

    def crear_interfaz(self):
        # ---------------------------------------------------------
        # ENCABEZADO
        # ---------------------------------------------------------
        header = tk.Frame(self, bg=COLOR_HEADER, height=50)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=" MÓDULO DE REPORTES Y ESTADÍSTICAS DE FACTURACIÓN",
            bg=COLOR_HEADER,
            fg="white",
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left", padx=15, pady=10)

        # ---------------------------------------------------------
        # BARRA DE FILTROS
        # ---------------------------------------------------------
        filtros_frame = tk.LabelFrame(
            self,
            text=" Filtros de Consulta ",
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0,
            padx=15,
            pady=10,
        )
        filtros_frame.pack(side="top", fill="x", padx=15, pady=10)

        # Fecha Inicio
        tk.Label(
            filtros_frame,
            text="Fecha Inicio (YYYY-MM-DD):",
            bg=CARD_BG,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.ent_fecha_inicio = tk.Entry(filtros_frame, width=14, font=("Segoe UI", 9))
        self.ent_fecha_inicio.grid(row=0, column=1, padx=5, pady=5)

        # Fecha Fin
        tk.Label(
            filtros_frame,
            text="Fecha Fin (YYYY-MM-DD):",
            bg=CARD_BG,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.ent_fecha_fin = tk.Entry(filtros_frame, width=14, font=("Segoe UI", 9))
        self.ent_fecha_fin.grid(row=0, column=3, padx=5, pady=5)

        # Valores por defecto (Últimos 30 días)
        hoy = datetime.now()
        hace_un_mes = hoy - timedelta(days=30)
        self.ent_fecha_inicio.insert(0, hace_un_mes.strftime("%Y-%m-%d"))
        self.ent_fecha_fin.insert(0, hoy.strftime("%Y-%m-%d"))

        # Botón Filtrar
        btn_filtrar = tk.Button(
            filtros_frame,
            text=" Generar Reporte",
            bg=BTN_PRIMARY,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=4,
            command=self.filtrar_datos,
        )
        btn_filtrar.grid(row=0, column=4, padx=15, pady=5)

        # ---------------------------------------------------------
        # ÁREA CONTENEDORA PRINCIPAL (TABLA Y GRÁFICOS)
        # ---------------------------------------------------------
        cuerpo = tk.Frame(self, bg=BG_REPORTES)
        cuerpo.pack(expand=True, fill="both", padx=15, pady=(0, 15))

        # PANEL IZQUIERDO: TABLA DE VENTAS Y TARJETAS
        panel_izq = tk.Frame(cuerpo, bg=BG_REPORTES)
        panel_izq.pack(side="left", expand=True, fill="both", padx=(0, 10))

        # Tarjeta Resumen
        resumen_frame = tk.Frame(
            panel_izq,
            bg=CARD_BG,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0,
        )
        resumen_frame.pack(fill="x", pady=(0, 10))

        self.lbl_total_recaudado = tk.Label(
            resumen_frame,
            text="Total Recaudado: $0.00",
            bg=CARD_BG,
            fg=BTN_PRIMARY,
            font=("Segoe UI", 12, "bold"),
        )
        self.lbl_total_recaudado.pack(side="left", padx=15, pady=12)

        self.lbl_total_facturas = tk.Label(
            resumen_frame,
            text="Total Facturas: 0",
            bg=CARD_BG,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10, "bold"),
        )
        self.lbl_total_facturas.pack(side="right", padx=15, pady=12)

        # Tabla de Facturas
        lbl_tabla = tk.Label(
            panel_izq,
            text="Detalle de Facturas",
            bg=BG_REPORTES,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
        )
        lbl_tabla.pack(anchor="w", pady=(0, 5))

        # Estilos para el Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Reportes.Treeview.Heading",
            background=COLOR_HEADER,
            foreground="white",
            font=("Segoe UI", 9, "bold"),
        )
        style.configure(
            "Reportes.Treeview",
            background=CARD_BG,
            fieldbackground=CARD_BG,
            foreground=TEXT_PRIMARY,
            rowheight=24,
            font=("Segoe UI", 9),
        )

        columnas = ("N° Venta", "Fecha", "Cliente", "Vendedor", "Subtotal", "IVA", "Total", "Método")
        self.tree_ventas = ttk.Treeview(
            panel_izq,
            columns=columnas,
            show="headings",
            height=12,
            style="Reportes.Treeview",
        )

        for col in columnas:
            self.tree_ventas.heading(col, text=col)
            self.tree_ventas.column(col, width=80, anchor="center")

        self.tree_ventas.column("Cliente", width=130, anchor="w")
        self.tree_ventas.column("Vendedor", width=110, anchor="w")
        self.tree_ventas.pack(expand=True, fill="both")

        # PANEL DERECHO: GRÁFICOS DE MATPLOTLIB
        self.panel_der = tk.Frame(
            cuerpo,
            bg=CARD_BG,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0,
        )
        self.panel_der.pack(side="right", expand=True, fill="both")

    # ---------------------------------------------------------
    # MÉTODOS Y LÓGICA DE REPORTES
    # ---------------------------------------------------------
    def filtrar_datos(self):
        fecha_i = self.ent_fecha_inicio.get().strip()
        fecha_f = self.ent_fecha_fin.get().strip()

        # Limpiar tabla
        for row in self.tree_ventas.get_children():
            self.tree_ventas.delete(row)

        try:
            # Obtener ventas filtradas de la base de datos
            ventas = obtener_reporte_ventas_por_fecha(fecha_i, fecha_f)
            total_dinero = 0.0

            if ventas:
                for v in ventas:
                    subtotal = f"${v[4]:,.2f}"
                    iva = f"${v[5]:,.2f}"
                    total = f"${v[6]:,.2f}"

                    self.tree_ventas.insert(
                        "",
                        "end",
                        values=(v[0], v[1], v[2], v[3], subtotal, iva, total, v[7]),
                    )
                    total_dinero += float(v[6])

            # Actualizar indicadores
            self.lbl_total_recaudado.config(text=f"Total Recaudado: ${total_dinero:,.2f}")
            self.lbl_total_facturas.config(text=f"Total Facturas: {len(ventas) if ventas else 0}")

            # Renderizar gráficos
            self.renderizar_graficos()

        except Exception as e:
            messagebox.showerror("Error de Consulta", f"Ocurrió un error al cargar los reportes: {e}")

    def renderizar_graficos(self):
        # Limpiar panel de gráficos anterior
        for widget in self.panel_der.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.2, 5.2), dpi=100)
        fig.patch.set_facecolor("white")

        # Gráfico 1: Métodos de Pago
        try:
            metodos_data = obtener_ventas_por_metodo_pago()
            if metodos_data:
                metodos = [m[0] for m in metodos_data]
                totales = [m[1] for m in metodos_data]
                colores = ["#2563EB", "#059669", "#D97706", "#DC2626", "#64748B"]

                ax1.pie(
                    totales,
                    labels=metodos,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=colores[: len(metodos)],
                    textprops={"fontsize": 8},
                )
                ax1.set_title("Ventas por Método de Pago", fontsize=10, fontweight="bold", color=TEXT_PRIMARY)
            else:
                ax1.text(0.5, 0.5, "Sin Datos", ha="center", va="center", color=TEXT_SECONDARY)
                ax1.set_title("Ventas por Método de Pago", fontsize=10, fontweight="bold", color=TEXT_PRIMARY)
        except Exception:
            ax1.text(0.5, 0.5, "Error al cargar", ha="center", va="center", color="red")

        # Gráfico 2: Top Productos Más Vendidos
        try:
            top_prod = productos_mas_vendidos(limite=5)
            if top_prod:
                prods = [p[0][:12] + "..." if len(p[0]) > 12 else p[0] for p in top_prod]
                cants = [p[1] for p in top_prod]

                ax2.barh(prods, cants, color="#2563EB")
                ax2.set_title("Top 5 Productos Vendidos", fontsize=10, fontweight="bold", color=TEXT_PRIMARY)
                ax2.invert_yaxis()
                ax2.tick_params(axis="both", labelsize=8)
            else:
                ax2.text(0.5, 0.5, "Sin Datos", ha="center", va="center", color=TEXT_SECONDARY)
                ax2.set_title("Top 5 Productos Vendidos", fontsize=10, fontweight="bold", color=TEXT_PRIMARY)
        except Exception:
            ax2.text(0.5, 0.5, "Error al cargar", ha="center", va="center", color="red")

        plt.tight_layout()

        # Dibujar figura en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.panel_der)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

        # Liberar la memoria de la figura al cerrar/sobrescribir
        plt.close(fig)
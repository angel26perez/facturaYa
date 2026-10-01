import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import COLOR_FONDO
from modules.database import (
    total_clientes,
    total_ventas_dinero,
    productos_bajo_stock,
    productos_mas_vendidos,
    ultimas_ventas,
    resumen_inventario
)

# ==========================================
# PALETA DE COLORES PROFESIONAL / ENTERPRISE
# ==========================================
BG_DASHBOARD = "#F8FAFC"      # Fondo general claro
CARD_BG = "#FFFFFF"           # Fondo de tarjetas y marcos
TEXT_PRIMARY = "#0F172A"       # Texto principal (Gris/Azul muy oscuro)
TEXT_SECONDARY = "#64748B"     # Texto secundario (Gris medio)
BORDER_COLOR = "#E2E8F0"       # Bordes sutiles

# Colores para Tarjetas KPI y Gráficos
COLOR_PRIMARY = "#2563EB"      # Azul Corporativo (Ingresos)
COLOR_SUCCESS = "#0D9488"      # Verde / Teal (Valor Inventario)
COLOR_INFO = "#6366F1"         # Índigo (Total Productos)
COLOR_WARNING = "#D97706"      # Ámbar / Dorado (Unidades en Stock)
COLOR_DARK = "#334155"         # Slate Oscuro (Clientes)
COLOR_DANGER = "#DC2626"       # Rojo Alerta (Bajo Stock)


class DashboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_DASHBOARD)
        self.pack(expand=True, fill="both")
        self.crear_dashboard()

    def crear_tarjeta(self, parent, titulo, valor, color_borde):
        """Crea una tarjeta KPI estilo Dashboard moderno con borde de acento."""
        card = tk.Frame(
            parent, 
            bg=CARD_BG, 
            highlightbackground=BORDER_COLOR, 
            highlightthickness=1,
            width=210, 
            height=90
        )
        card.pack_propagate(False)

        # Barra lateral de acento de color
        accent_bar = tk.Frame(card, bg=color_borde, width=5)
        accent_bar.pack(side="left", fill="y")

        content = tk.Frame(card, bg=CARD_BG)
        content.pack(side="left", fill="both", expand=True, padx=12, pady=10)

        tk.Label(
            content, 
            text=titulo.upper(), 
            bg=CARD_BG, 
            fg=TEXT_SECONDARY, 
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        tk.Label(
            content, 
            text=str(valor), 
            bg=CARD_BG, 
            fg=TEXT_PRIMARY, 
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", pady=(2, 0))

        return card

    def crear_dashboard(self):
        # ---------------------------------------------------------
        # TÍTULO PRINCIPAL
        # ---------------------------------------------------------
        header_frame = tk.Frame(self, bg=BG_DASHBOARD)
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="RESUMEN GENERAL DE FACTURACIÓN",
            bg=BG_DASHBOARD,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w")

        # ---------------------------------------------------------
        # SEC-1: TARJETAS KPI RESUMEN
        # ---------------------------------------------------------
        resumen = resumen_inventario()
        ventas_dinero = f"${total_ventas_dinero():,.0f}"
        valor_inv = f"${resumen['valor_inventario']:,.0f}"

        kpi_frame = tk.Frame(self, bg=BG_DASHBOARD)
        kpi_frame.pack(fill="x", padx=20, pady=5)

        self.crear_tarjeta(kpi_frame, "Ingresos Ventas", ventas_dinero, COLOR_PRIMARY).pack(side="left", padx=(0, 10), expand=True, fill="x")
        self.crear_tarjeta(kpi_frame, "Valor Inventario", valor_inv, COLOR_SUCCESS).pack(side="left", padx=5, expand=True, fill="x")
        self.crear_tarjeta(kpi_frame, "Total Productos", resumen['total_items'], COLOR_INFO).pack(side="left", padx=5, expand=True, fill="x")
        self.crear_tarjeta(kpi_frame, "Unidades Stock", resumen['total_unidades'], COLOR_WARNING).pack(side="left", padx=5, expand=True, fill="x")
        self.crear_tarjeta(kpi_frame, "Clientes", total_clientes(), COLOR_DARK).pack(side="left", padx=(10, 0), expand=True, fill="x")

        # ---------------------------------------------------------
        # SEC-2: ÁREA CENTRAL (GRÁFICO Y ÚLTIMAS VENTAS)
        # ---------------------------------------------------------
        mid_frame = tk.Frame(self, bg=BG_DASHBOARD)
        mid_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Gráfico de Productos Más Vendidos (Matplotlib)
        chart_container = tk.LabelFrame(
            mid_frame, 
            text=" Top 5 Productos Más Vendidos ", 
            bg=CARD_BG, 
            fg=TEXT_PRIMARY, 
            font=("Segoe UI", 10, "bold"),
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0
        )
        chart_container.pack(side="left", fill="both", expand=True, padx=(0, 10))

        mas_vendidos = productos_mas_vendidos()
        if mas_vendidos:
            nombres = [item[0][:15] + "..." if len(item[0]) > 15 else item[0] for item in mas_vendidos]
            cantidades = [item[1] for item in mas_vendidos]
        else:
            nombres = ["Sin Datos"]
            cantidades = [0]

        fig, ax = plt.subplots(figsize=(5, 3), dpi=90)
        fig.patch.set_facecolor(CARD_BG)
        ax.set_facecolor(CARD_BG)

        # Barras con color primario corporativo
        bars = ax.barh(nombres, cantidades, color=COLOR_PRIMARY, height=0.55)
        ax.invert_yaxis()

        # Ocultar bordes innecesarios del gráfico
        for spine in ['top', 'right', 'left', 'bottom']:
            ax.spines[spine].set_visible(False)

        ax.tick_params(axis='both', which='both', length=0, labelsize=9, colors=TEXT_SECONDARY)
        ax.xaxis.grid(True, linestyle='--', alpha=0.5, color=BORDER_COLOR)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        plt.close(fig)

        # Tabla Últimas Ventas
        ventas_container = tk.LabelFrame(
            mid_frame, 
            text=" Últimas Ventas Realizadas ", 
            bg=CARD_BG, 
            fg=TEXT_PRIMARY, 
            font=("Segoe UI", 10, "bold"),
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0
        )
        ventas_container.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tree_v = ttk.Treeview(
            ventas_container, 
            columns=("num", "fecha", "total", "pago"), 
            show="headings", 
            height=6
        )

        tree_v.heading("num", text="N° Venta")
        tree_v.heading("fecha", text="Fecha")
        tree_v.heading("total", text="Total")
        tree_v.heading("pago", text="Pago")

        tree_v.column("num", width=90, anchor="center")
        tree_v.column("fecha", width=120, anchor="center")
        tree_v.column("total", width=90, anchor="e")
        tree_v.column("pago", width=100, anchor="center")

        tree_v.pack(fill="both", expand=True, padx=10, pady=10)

        for v in ultimas_ventas():
            tree_v.insert("", "end", values=(v[0], v[1], f"${v[2]:,.0f}", v[3]))

        # ---------------------------------------------------------
        # SEC-3: TABLA PRODUCTOS CON BAJO STOCK
        # ---------------------------------------------------------
        alert_frame = tk.LabelFrame(
            self, 
            text=" ⚠️ ALERTA: PRODUCTOS CON BAJO STOCK (<= 10) ", 
            bg=CARD_BG, 
            fg=COLOR_DANGER, 
            font=("Segoe UI", 10, "bold"),
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0
        )
        alert_frame.pack(fill="x", padx=20, pady=(0, 15))

        tree_stock = ttk.Treeview(
            alert_frame, 
            columns=("codigo", "nombre", "precio", "stock"), 
            show="headings", 
            height=4
        )

        tree_stock.heading("codigo", text="Código")
        tree_stock.heading("nombre", text="Producto")
        tree_stock.heading("precio", text="Precio")
        tree_stock.heading("stock", text="Stock Actual")

        tree_stock.column("codigo", width=100, anchor="center")
        tree_stock.column("nombre", width=400)
        tree_stock.column("precio", width=120, anchor="e")
        tree_stock.column("stock", width=100, anchor="center")

        tree_stock.pack(fill="both", expand=True, padx=10, pady=10)

        for prod in productos_bajo_stock(limite=10):
            tree_stock.insert("", "end", values=(prod[0], prod[1], f"${prod[2]:,.0f}", prod[3]))
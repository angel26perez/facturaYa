import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from config import COLOR_BLANCO, COLOR_FONDO, IVA, LUFFY_BLUE, LUFFY_GOLD
from modules.database import (
    buscar_producto,
    conectar,
    descontar_stock,
    obtener_o_crear_cliente_defecto,
    registrar_detalle,
    registrar_venta,
)

# Constantes de diseño corporativo
BG_VENTAS = "#F8FAFC"        # Fondo general
CARD_BG = "#FFFFFF"           # Contenedores
TEXT_PRIMARY = "#0F172A"     # Texto principal
TEXT_SECONDARY = "#64748B"   # Texto secundario
BORDER_COLOR = "#E2E8F0"     # Bordes

BTN_PRIMARY = "#2563EB"      # Azul Corporativo
BTN_SUCCESS = "#16A34A"      # Verde Facturar / Agregar
BTN_DANGER = "#DC2626"       # Rojo Eliminar
BTN_WARNING = "#D97706"      # Ámbar Limpiar


class VentasFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_VENTAS)
        self.pack(expand=True, fill="both")

        self.cart = []
        self.producto_actual = None
        self.total_actual = 0.0
        self.lista_clientes = []
        self.dic_productos = {}

        self.generar_numero_venta()
        self.crear_interfaz()
        self.cargar_clientes_cb()
        self.cargar_lista_productos()

    def generar_numero_venta(self):
        self.numero_venta = f"VTA-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def cargar_clientes_cb(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, documento FROM clientes ORDER BY nombre")
            self.lista_clientes = cursor.fetchall()
            conn.close()

            opciones = ["Cliente No Frecuente"]
            for c in self.lista_clientes:
                if c[1] != "Cliente No Frecuente":
                    opciones.append(f"{c[0]} - {c[1]} ({c[2]})")

            self.cmb_cliente["values"] = opciones
            self.cmb_cliente.current(0)
        except Exception:
            self.cmb_cliente["values"] = ["Cliente No Frecuente"]
            self.cmb_cliente.current(0)

    def cargar_lista_productos(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, nombre, precio, stock FROM productos WHERE stock > 0 ORDER BY nombre")
            productos = cursor.fetchall()
            conn.close()

            self.dic_productos = {f"{p[1]} (Cód: {p[0]})": p for p in productos}
            self.cmb_busqueda_prod["values"] = list(self.dic_productos.keys())
        except Exception:
            self.cmb_busqueda_prod["values"] = []

    def crear_interfaz(self):
        # ---------------------------------------------------------
        # ENCABEZADO E INFORMACIÓN
        # ---------------------------------------------------------
        header = tk.Frame(self, bg=BG_VENTAS)
        header.pack(fill="x", padx=15, pady=(10, 2))

        tk.Label(
            header,
            text="PUNTO DE VENTA (POS)",
            bg=BG_VENTAS,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w")

        info = tk.Frame(self, bg=BG_VENTAS)
        info.pack(fill="x", padx=15, pady=(0, 5))

        self.lbl_factura = tk.Label(
            info,
            text=f"Factura: {self.numero_venta}",
            bg=BG_VENTAS,
            fg=BTN_PRIMARY,
            font=("Segoe UI", 9, "bold"),
        )
        self.lbl_factura.pack(side="left")

        self.lbl_fecha = tk.Label(
            info,
            text=datetime.now().strftime("%d/%m/%Y %H:%M"),
            bg=BG_VENTAS,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 9),
        )
        self.lbl_fecha.pack(side="right")

        # ---------------------------------------------------------
        # CONTENEDOR PRINCIPAL IZQUIERDA / DERECHA
        # ---------------------------------------------------------
        contenido = tk.Frame(self, bg=BG_VENTAS)
        contenido.pack(fill="both", expand=True, padx=15, pady=2)

        # SECCIÓN IZQUIERDA (Buscador y Carrito)
        panel_izquierdo = tk.Frame(contenido, bg=BG_VENTAS)
        panel_izquierdo.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # 1. BARRA AGREGAR PRODUCTO
        frm_busqueda = tk.LabelFrame(
            panel_izquierdo,
            text=" AGREGAR PRODUCTO ",
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 9, "bold"),
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0,
            padx=8,
            pady=6,
        )
        frm_busqueda.pack(fill="x", pady=(0, 5))

        tk.Label(frm_busqueda, text="Código:", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 8, "bold")).grid(
            row=0, column=0, padx=2
        )
        self.ent_codigo = tk.Entry(frm_busqueda, width=12, font=("Segoe UI", 9))
        self.ent_codigo.grid(row=0, column=1, padx=2)
        self.ent_codigo.bind("<Return>", lambda e: self.buscar_producto_ui())

        tk.Button(
            frm_busqueda,
            text="Buscar Cód",
            bg=BTN_PRIMARY,
            fg="white",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            cursor="hand2",
            padx=6,
            pady=2,
            command=self.buscar_producto_ui,
        ).grid(row=0, column=2, padx=3)

        tk.Label(frm_busqueda, text="O Nombre:", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 8, "bold")).grid(
            row=0, column=3, padx=(8, 2)
        )
        self.cmb_busqueda_prod = ttk.Combobox(frm_busqueda, width=22, font=("Segoe UI", 9))
        self.cmb_busqueda_prod.grid(row=0, column=4, padx=2)
        self.cmb_busqueda_prod.bind("<<ComboboxSelected>>", self.seleccionar_producto_combo)

        self.lbl_precio = tk.Label(
            frm_busqueda,
            text="$ 0.00",
            bg=CARD_BG,
            fg=BTN_PRIMARY,
            font=("Segoe UI", 10, "bold"),
        )
        self.lbl_precio.grid(row=0, column=5, padx=8)

        tk.Label(frm_busqueda, text="Cant:", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 8, "bold")).grid(
            row=0, column=6, padx=2
        )
        self.spin_cantidad = tk.Spinbox(frm_busqueda, from_=1, to=100, width=4, font=("Segoe UI", 9))
        self.spin_cantidad.grid(row=0, column=7, padx=2)

        tk.Button(
            frm_busqueda,
            text="+ Agregar",
            bg=BTN_SUCCESS,
            fg="white",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=2,
            command=self.agregar_carrito,
        ).grid(row=0, column=8, padx=4)

        # 2. CARRITO DE COMPRA
        frame_carrito = tk.LabelFrame(
            panel_izquierdo,
            text=" CARRITO DE COMPRA ",
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 9, "bold"),
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0,
        )
        frame_carrito.pack(fill="both", expand=True, pady=(0, 5))

        # Estilos explícitos para asegurar visibilidad de las filas
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "POS.Treeview.Heading",
            background=BTN_PRIMARY,
            foreground="white",
            font=("Segoe UI", 8, "bold"),
        )
        style.configure(
            "POS.Treeview",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#0F172A",
            rowheight=26,
            font=("Segoe UI", 9),
        )
        style.map("POS.Treeview", background=[("selected", "#2563EB")], foreground=[("selected", "#FFFFFF")])

        columnas = ("codigo", "producto", "cantidad", "precio", "subtotal")
        self.tree = ttk.Treeview(
            frame_carrito,
            columns=columnas,
            show="headings",
            style="POS.Treeview",
        )

        self.tree.heading("codigo", text="CÓDIGO")
        self.tree.heading("producto", text="PRODUCTO")
        self.tree.heading("cantidad", text="CANT.")
        self.tree.heading("precio", text="PRECIO")
        self.tree.heading("subtotal", text="SUBTOTAL")

        self.tree.column("codigo", width=90, anchor="center")
        self.tree.column("producto", width=250, anchor="w")
        self.tree.column("cantidad", width=60, anchor="center")
        self.tree.column("precio", width=100, anchor="e")
        self.tree.column("subtotal", width=110, anchor="e")

        # Scrollbar para el carrito
        scrollbar = ttk.Scrollbar(frame_carrito, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y", pady=6)
        self.tree.pack(fill="both", expand=True, padx=(8, 0), pady=6)

        # Configuración de etiqueta para forzar texto oscuro
        self.tree.tag_configure("item_row", foreground="#0F172A", background="#FFFFFF")

        botones_carrito = tk.Frame(frame_carrito, bg=CARD_BG)
        botones_carrito.pack(fill="x", padx=8, pady=(0, 6))

        tk.Button(
            botones_carrito,
            text="Eliminar Item",
            bg=BTN_DANGER,
            fg="white",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=3,
            command=self.eliminar_item,
        ).pack(side="left", padx=2)

        tk.Button(
            botones_carrito,
            text="Limpiar Carrito",
            bg=BTN_WARNING,
            fg="white",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=3,
            command=self.limpiar_carrito,
        ).pack(side="left", padx=2)

        # ---------------------------------------------------------
        # PANEL DERECHO (CLIENTE, RESUMEN Y PAGO)
        # ---------------------------------------------------------
        panel_derecho = tk.Frame(contenido, bg=BG_VENTAS, width=280)
        panel_derecho.pack(side="right", fill="y")
        panel_derecho.pack_propagate(False)

        # Seleccionar Cliente
        frm_cliente = tk.LabelFrame(
            panel_derecho,
            text=" CLIENTE ",
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 9, "bold"),
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0,
            padx=8,
            pady=4,
        )
        frm_cliente.pack(fill="x", pady=(0, 4))

        self.cmb_cliente = ttk.Combobox(
            frm_cliente, state="readonly", values=["Cliente No Frecuente"], font=("Segoe UI", 9)
        )
        self.cmb_cliente.pack(fill="x", pady=2)

        # Resumen de Compra
        resumen = tk.LabelFrame(
            panel_derecho,
            text=" RESUMEN ",
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 9, "bold"),
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0,
            padx=8,
            pady=4,
        )
        resumen.pack(fill="x", pady=(0, 4))

        self.lbl_subtotal = tk.Label(
            resumen, text="Subtotal: $0.00", bg=CARD_BG, fg=TEXT_SECONDARY, anchor="e", font=("Segoe UI", 9)
        )
        self.lbl_subtotal.pack(fill="x", pady=1)

        descuento_frame = tk.Frame(resumen, bg=CARD_BG)
        descuento_frame.pack(fill="x", pady=1)

        tk.Label(descuento_frame, text="Descuento ($):", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9)).pack(
            side="left"
        )
        self.ent_descuento = tk.Entry(descuento_frame, width=8, font=("Segoe UI", 9), justify="right")
        self.ent_descuento.insert(0, "0")
        self.ent_descuento.pack(side="right")
        self.ent_descuento.bind("<KeyRelease>", lambda e: self.actualizar_totales())

        self.lbl_iva = tk.Label(
            resumen, text="IVA: $0.00", bg=CARD_BG, fg=TEXT_SECONDARY, anchor="e", font=("Segoe UI", 9)
        )
        self.lbl_iva.pack(fill="x", pady=1)

        self.lbl_total = tk.Label(
            resumen,
            text="$ 0.00",
            bg=BTN_PRIMARY,
            fg="white",
            font=("Segoe UI", 15, "bold"),
        )
        self.lbl_total.pack(fill="x", pady=4)

        # Método de Pago
        pago = tk.LabelFrame(
            panel_derecho,
            text=" MÉTODO DE PAGO ",
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 9, "bold"),
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0,
            padx=8,
            pady=4,
        )
        pago.pack(fill="x", pady=4)

        tk.Label(pago, text="Método:", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 8)).pack(anchor="w")
        self.cmb_pago = ttk.Combobox(
            pago,
            values=["Efectivo", "Tarjeta", "Transferencia"],
            state="readonly",
            font=("Segoe UI", 9),
        )
        self.cmb_pago.current(0)
        self.cmb_pago.pack(fill="x", pady=2)

        tk.Label(pago, text="Valor recibido:", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 8)).pack(anchor="w")
        self.ent_pagado = tk.Entry(pago, font=("Segoe UI", 9))
        self.ent_pagado.pack(fill="x", pady=2)
        self.ent_pagado.bind("<KeyRelease>", lambda e: self.calcular_cambio())

        self.lbl_cambio = tk.Label(
            pago,
            text="Cambio: $0.00",
            bg=CARD_BG,
            fg="green",
            font=("Segoe UI", 9, "bold"),
        )
        self.lbl_cambio.pack(pady=3)

        # Botón Facturar
        tk.Button(
            panel_derecho,
            text="FACTURAR VENTA",
            bg=BTN_SUCCESS,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            height=2,
            command=self.facturar,
        ).pack(fill="x", pady=6)

    # ---------------------------------------------------------
    # LÓGICA BÚSQUEDA Y CARRITO
    # ---------------------------------------------------------
    def seleccionar_producto_combo(self, event):
        seleccion = self.cmb_busqueda_prod.get()
        if seleccion in self.dic_productos:
            prod = self.dic_productos[seleccion]
            self.producto_actual = prod
            self.ent_codigo.delete(0, tk.END)
            self.ent_codigo.insert(0, str(prod[0]))
            self.lbl_precio.config(text=f"$ {float(prod[2]):,.2f}")

    def buscar_producto_ui(self):
        codigo = self.ent_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Producto", "Ingrese el código del producto.")
            return

        producto = buscar_producto(codigo)
        if not producto:
            messagebox.showerror("Producto", "Producto no encontrado.")
            self.producto_actual = None
            self.lbl_precio.config(text="$ 0.00")
            return

        self.producto_actual = producto
        precio = float(producto[2])
        self.lbl_precio.config(text=f"$ {precio:,.2f}")

    def agregar_carrito(self):
        if not self.producto_actual:
            messagebox.showwarning("Producto", "Primero busque o seleccione un producto.")
            return

        try:
            cantidad = int(self.spin_cantidad.get())
        except ValueError:
            messagebox.showerror("Cantidad", "Ingrese una cantidad válida.")
            return

        if cantidad <= 0:
            messagebox.showwarning("Cantidad", "La cantidad debe ser mayor que cero.")
            return

        codigo = self.producto_actual[0]
        nombre = self.producto_actual[1]
        precio = float(self.producto_actual[2])
        stock = int(self.producto_actual[3])

        for item in self.cart:
            if item["codigo"] == codigo:
                nueva_cantidad = item["cantidad"] + cantidad
                if nueva_cantidad > stock:
                    disponible = stock - item["cantidad"]
                    messagebox.showerror(
                        "Stock insuficiente",
                        f"Solo puede agregar {disponible} unidades más.",
                    )
                    return
                item["cantidad"] = nueva_cantidad
                item["subtotal"] = nueva_cantidad * precio
                self.refrescar_carrito()
                return

        if cantidad > stock:
            messagebox.showerror("Stock insuficiente", f"Stock disponible: {stock}")
            return

        self.cart.append(
            {
                "codigo": codigo,
                "nombre": nombre,
                "cantidad": cantidad,
                "precio": precio,
                "subtotal": cantidad * precio,
            }
        )
        self.refrescar_carrito()

    def refrescar_carrito(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.cart:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    item["codigo"],
                    item["nombre"],
                    item["cantidad"],
                    f"${item['precio']:,.2f}",
                    f"${item['subtotal']:,.2f}",
                ),
                tags=("item_row",),
            )
        self.actualizar_totales()

    def eliminar_item(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Carrito", "Seleccione un producto del carrito.")
            return

        index = self.tree.index(seleccion[0])
        self.cart.pop(index)
        self.refrescar_carrito()

    def limpiar_carrito(self):
        if self.cart:
            confirmar = messagebox.askyesno("Limpiar", "¿Desea limpiar la venta actual?")
            if not confirmar:
                return

        self.cart.clear()
        self.producto_actual = None
        self.tree.delete(*self.tree.get_children())
        self.ent_codigo.delete(0, tk.END)
        self.cmb_busqueda_prod.set("")
        self.ent_pagado.delete(0, tk.END)
        self.ent_descuento.delete(0, tk.END)
        self.ent_descuento.insert(0, "0")
        self.spin_cantidad.delete(0, tk.END)
        self.spin_cantidad.insert(0, "1")
        self.lbl_precio.config(text="$ 0.00")
        self.lbl_cambio.config(text="Cambio: $0.00", fg="green")
        self.generar_numero_venta()
        self.lbl_factura.config(text=f"Factura: {self.numero_venta}")
        self.cargar_clientes_cb()
        self.actualizar_totales()

    def actualizar_totales(self):
        subtotal = sum(item["subtotal"] for item in self.cart)

        try:
            descuento = float(self.ent_descuento.get())
        except ValueError:
            descuento = 0.0

        if descuento < 0:
            descuento = 0.0
        if descuento > subtotal:
            descuento = subtotal

        base = subtotal - descuento
        iva = base * IVA
        total = base + iva
        self.total_actual = total

        self.lbl_subtotal.config(text=f"Subtotal: ${subtotal:,.2f}")
        self.lbl_iva.config(text=f"IVA: ${iva:,.2f}")
        self.lbl_total.config(text=f"$ {total:,.2f}")

        self.calcular_cambio()

    def calcular_cambio(self):
        try:
            pagado = float(self.ent_pagado.get())
        except ValueError:
            pagado = 0.0

        cambio = pagado - self.total_actual

        if pagado <= 0:
            self.lbl_cambio.config(text="Cambio: $0.00", fg="green")
        elif cambio < 0:
            self.lbl_cambio.config(text=f"Faltan: ${abs(cambio):,.2f}", fg="red")
        else:
            self.lbl_cambio.config(text=f"Cambio: ${cambio:,.2f}", fg="green")

    # ---------------------------------------------------------
    # PROCESAR FACTURACIÓN
    # ---------------------------------------------------------
    def facturar(self):
        if not self.cart:
            messagebox.showwarning("Venta", "No hay productos en el carrito.")
            return

        subtotal = sum(item["subtotal"] for item in self.cart)

        try:
            descuento = float(self.ent_descuento.get())
            if descuento < 0 or descuento > subtotal:
                messagebox.showerror("Descuento", "Descuento inválido.")
                return
        except ValueError:
            messagebox.showerror("Descuento", "El descuento debe ser numérico.")
            return

        base = subtotal - descuento
        iva = base * IVA
        total = base + iva

        try:
            pagado = float(self.ent_pagado.get())
            if pagado < total:
                messagebox.showerror(
                    "Pago insuficiente",
                    f"Total: ${total:,.2f} | Pagado: ${pagado:,.2f}\nFaltan: ${total - pagado:,.2f}",
                )
                return
        except ValueError:
            messagebox.showerror("Pago", "Ingrese un valor recibido válido.")
            return

        cambio = pagado - total
        metodo_pago = self.cmb_pago.get()

        # Obtener cliente
        cliente_seleccionado = self.cmb_cliente.get()
        if cliente_seleccionado == "Cliente No Frecuente":
            cliente_id, cliente_nombre = obtener_o_crear_cliente_defecto()
        else:
            cliente_id = int(cliente_seleccionado.split(" - ")[0])
            cliente_nombre = cliente_seleccionado.split(" - ")[1].split(" (")[0]

        confirmar = messagebox.askyesno(
            "Confirmar venta",
            f"Factura: {self.numero_venta}\n"
            f"Cliente: {cliente_nombre}\n"
            f"TOTAL: ${total:,.2f}\n"
            f"Pago: {metodo_pago} (${pagado:,.2f})\n"
            f"Cambio: ${cambio:,.2f}\n\n"
            "¿Confirmar venta?",
        )

        if confirmar:
            try:
                venta_id = registrar_venta(
                    self.numero_venta,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "ADMIN",
                    cliente_id,
                    cliente_nombre,
                    subtotal,
                    descuento,
                    iva,
                    total,
                    metodo_pago,
                )

                for item in self.cart:
                    registrar_detalle(
                        venta_id,
                        item["codigo"],
                        item["nombre"],
                        item["cantidad"],
                        item["precio"],
                        item["subtotal"],
                    )
                    descontar_stock(item["codigo"], item["cantidad"])

                messagebox.showinfo(
                    "Venta registrada",
                    f"VENTA REGISTRADA EXITOSAMENTE\n\n"
                    f"Factura: {self.numero_venta}\n"
                    f"Total: ${total:,.2f}\n"
                    f"Cambio: ${cambio:,.2f}",
                )

                # Limpiar y actualizar listas
                self.limpiar_carrito()
                self.cargar_lista_productos()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar la venta: {e}")
import tkinter as tk
from tkinter import ttk, messagebox

# Constantes de diseño corporativo / Enterprise
BG_INVENTARIO = "#F8FAFC"      # Fondo general claro
CARD_BG = "#FFFFFF"           # Fondo de contenedores y formularios
TEXT_PRIMARY = "#0F172A"       # Texto principal
TEXT_SECONDARY = "#64748B"     # Texto secundario/subtítulos
BORDER_COLOR = "#E2E8F0"       # Bordes suaves

# Botones con colores profesionales
BTN_GUARDAR = "#2563EB"        # Azul Corporativo
BTN_ACTUALIZAR = "#D97706"     # Ámbar / Dorado
BTN_ELIMINAR = "#DC2626"       # Rojo Alerta
BTN_LIMPIAR = "#64748B"        # Gris Slate

from modules.database import (
    conectar,
    obtener_productos,
    agregar_producto,
    actualizar_producto,
    eliminar_producto,
    buscar_producto,
)


class InventarioFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_INVENTARIO)
        self.pack(expand=True, fill="both")
        self.crear_interfaz()
        self.cargar_productos()

    def crear_interfaz(self):
        # ---------------------------------------------------------
        # ENCABEZADO
        # ---------------------------------------------------------
        header = tk.Frame(self, bg=BG_INVENTARIO)
        header.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(
            header,
            text="GESTIÓN DE INVENTARIO Y PRODUCTOS",
            bg=BG_INVENTARIO,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")

        # ---------------------------------------------------------
        # FORMULARIO
        # ---------------------------------------------------------
        form = tk.LabelFrame(
            self,
            text=" Datos del Producto ",
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0,
            padx=15,
            pady=10,
        )
        form.pack(fill="x", padx=20, pady=10)

        # Campos
        tk.Label(form, text="Código *", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.ent_codigo = tk.Entry(form, width=20, font=("Segoe UI", 9))
        self.ent_codigo.grid(row=1, column=0, padx=5, pady=(2, 5))

        tk.Label(form, text="Nombre del Producto *", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(
            row=0, column=1, sticky="w", padx=5
        )
        self.ent_nombre = tk.Entry(form, width=42, font=("Segoe UI", 9))
        self.ent_nombre.grid(row=1, column=1, padx=5, pady=(2, 5))

        tk.Label(form, text="Precio *", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(
            row=0, column=2, sticky="w", padx=5
        )
        self.ent_precio = tk.Entry(form, width=15, font=("Segoe UI", 9))
        self.ent_precio.grid(row=1, column=2, padx=5, pady=(2, 5))

        tk.Label(form, text="Stock *", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(
            row=0, column=3, sticky="w", padx=5
        )
        self.ent_stock = tk.Entry(form, width=12, font=("Segoe UI", 9))
        self.ent_stock.grid(row=1, column=3, padx=5, pady=(2, 5))

        # ---------------------------------------------------------
        # BARRA DE BOTONES DE ACCIÓN
        # ---------------------------------------------------------
        barra = tk.Frame(self, bg=BG_INVENTARIO)
        barra.pack(fill="x", padx=20, pady=5)

        tk.Button(
            barra,
            text=" Guardar",
            bg=BTN_GUARDAR,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6,
            command=self.agregar_producto,
        ).pack(side="left", padx=(0, 5))

        tk.Button(
            barra,
            text=" Actualizar",
            bg=BTN_ACTUALIZAR,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6,
            command=self.actualizar_producto,
        ).pack(side="left", padx=5)

        tk.Button(
            barra,
            text=" Eliminar",
            bg=BTN_ELIMINAR,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6,
            command=self.eliminar_producto,
        ).pack(side="left", padx=5)

        tk.Button(
            barra,
            text=" Limpiar",
            bg=BTN_LIMPIAR,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6,
            command=self.limpiar_formulario,
        ).pack(side="left", padx=5)

        # ---------------------------------------------------------
        # BUSCADOR Y TABLA (TREEVIEW)
        # ---------------------------------------------------------
        busqueda = tk.Frame(self, bg=BG_INVENTARIO)
        busqueda.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(
            busqueda,
            text="Buscar producto:",
            bg=BG_INVENTARIO,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=(0, 5))

        self.ent_buscar = tk.Entry(busqueda, width=30, font=("Segoe UI", 9))
        self.ent_buscar.pack(side="left", padx=5)

        tk.Button(
            busqueda,
            text=" Buscar",
            bg=BTN_GUARDAR,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=3,
            command=self.buscar_producto,
        ).pack(side="left", padx=5)

        # Frame para la Tabla
        frame_tree = tk.LabelFrame(
            self,
            text=" Catálogo de Productos ",
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0,
        )
        frame_tree.pack(expand=True, fill="both", padx=20, pady=(5, 15))

        # Estilo para el Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview.Heading",
            background=BTN_GUARDAR,
            foreground="white",
            font=("Segoe UI", 9, "bold"),
        )
        style.configure(
            "Treeview",
            background=CARD_BG,
            fieldbackground=CARD_BG,
            foreground=TEXT_PRIMARY,
            rowheight=26,
            font=("Segoe UI", 9),
        )
        style.map("Treeview", background=[("selected", BTN_ACTUALIZAR)])

        columnas = ("codigo", "nombre", "precio", "stock")
        self.tree = ttk.Treeview(frame_tree, columns=columnas, show="headings")

        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre del Producto")
        self.tree.heading("precio", text="Precio Unitario")
        self.tree.heading("stock", text="Stock Disponible")

        self.tree.column("codigo", width=120, anchor="center")
        self.tree.column("nombre", width=380)
        self.tree.column("precio", width=140, anchor="e")
        self.tree.column("stock", width=120, anchor="center")

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_producto)

    # ---------------------------------------------------------
    # MÉTODOS CRUD Y LÓGICA DE NEGOCIO
    # ---------------------------------------------------------
    def agregar_producto(self):
        codigo = self.ent_codigo.get().strip()
        nombre = self.ent_nombre.get().strip()

        if not codigo or not nombre:
            messagebox.showwarning("Advertencia", "El Código y el Nombre son obligatorios.")
            return

        try:
            precio = float(self.ent_precio.get())
            stock = int(self.ent_stock.get())
        except ValueError:
            messagebox.showerror("Error", "Precio o Stock numérico inválido.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO productos (codigo, nombre, precio, stock) VALUES (?, ?, ?, ?)",
                (codigo, nombre, precio, stock),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
            self.cargar_productos()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")

    def actualizar_producto(self):
        codigo = self.ent_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Advertencia", "Seleccione un producto para actualizar.")
            return

        try:
            precio = float(self.ent_precio.get())
            stock = int(self.ent_stock.get())
        except ValueError:
            messagebox.showerror("Error", "Valores de Precio o Stock inválidos.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE codigo = ?",
                (self.ent_nombre.get().strip(), precio, stock, codigo),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            self.cargar_productos()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")

    def eliminar_producto(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")
            return

        codigo = self.tree.item(item)["values"][0]
        respuesta = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto '{codigo}'?")

        if respuesta:
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                self.cargar_productos()
                self.limpiar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")

    def cargar_productos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, nombre, precio, stock FROM productos ORDER BY nombre ASC")
            datos = cursor.fetchall()
            conn.close()

            for fila in datos:
                # Formatear precio para mejor visualización
                precio_fmt = f"${fila[2]:,.0f}"
                self.tree.insert("", tk.END, values=(fila[0], fila[1], precio_fmt, fila[3]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}")

    def buscar_producto(self):
        texto = self.ent_buscar.get().strip()

        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT codigo, nombre, precio, stock FROM productos WHERE nombre LIKE ? OR codigo LIKE ?",
                (f"%{texto}%", f"%{texto}%"),
            )
            productos = cursor.fetchall()
            conn.close()

            for item in productos:
                precio_fmt = f"${item[2]:,.0f}"
                self.tree.insert("", tk.END, values=(item[0], item[1], precio_fmt, item[3]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

    def seleccionar_producto(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            valores = self.tree.item(seleccion[0])["values"]
            self.limpiar_formulario()

            # Limpiar el formato de moneda al cargar en el Entry de precio
            precio_limpio = str(valores[2]).replace("$", "").replace(",", "").strip()

            self.ent_codigo.insert(0, valores[0])
            self.ent_nombre.insert(0, valores[1])
            self.ent_precio.insert(0, precio_limpio)
            self.ent_stock.insert(0, valores[3])

    def limpiar_formulario(self):
        self.ent_codigo.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_precio.delete(0, tk.END)
        self.ent_stock.delete(0, tk.END)
        if hasattr(self, "tree"):
            for item in self.tree.selection():
                self.tree.selection_remove(item)
        self.ent_codigo.focus()
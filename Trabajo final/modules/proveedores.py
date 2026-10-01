import tkinter as tk
from tkinter import ttk, messagebox

# Constantes de diseño corporativo
BG_PROVEEDORES = "#F8FAFC"     # Fondo general claro
CARD_BG = "#FFFFFF"            # Fondo de contenedores y formularios
TEXT_PRIMARY = "#0F172A"        # Texto principal
TEXT_SECONDARY = "#64748B"      # Texto secundario/subtítulos
BORDER_COLOR = "#E2E8F0"        # Bordes suaves

# Botones con colores profesionales
BTN_GUARDAR = "#2563EB"         # Azul Corporativo
BTN_ACTUALIZAR = "#D97706"      # Ámbar / Dorado
BTN_ELIMINAR = "#DC2626"        # Rojo Alerta
BTN_LIMPIAR = "#64748B"         # Gris Slate

from modules.database import conectar


class ProveedoresFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PROVEEDORES)
        self.pack(expand=True, fill="both")
        self.proveedor_id = None
        self.crear_interfaz()
        self.cargar_proveedores()

    def crear_interfaz(self):
        # ---------------------------------------------------------
        # ENCABEZADO
        # ---------------------------------------------------------
        header = tk.Frame(self, bg=BG_PROVEEDORES)
        header.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(
            header,
            text="GESTIÓN DE PROVEEDORES",
            bg=BG_PROVEEDORES,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")

        # ---------------------------------------------------------
        # FORMULARIO
        # ---------------------------------------------------------
        form = tk.LabelFrame(
            self,
            text=" Datos del Proveedor ",
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

        # Razón Social / Nombre
        tk.Label(form, text="Razón Social *", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.ent_nombre = tk.Entry(form, width=38, font=("Segoe UI", 9))
        self.ent_nombre.grid(row=1, column=0, padx=5, pady=(2, 5))

        # NIT
        tk.Label(form, text="NIT / Identificación *", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(
            row=0, column=1, sticky="w", padx=5
        )
        self.ent_nit = tk.Entry(form, width=22, font=("Segoe UI", 9))
        self.ent_nit.grid(row=1, column=1, padx=5, pady=(2, 5))

        # Teléfono
        tk.Label(form, text="Teléfono", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(
            row=0, column=2, sticky="w", padx=5
        )
        self.ent_telefono = tk.Entry(form, width=22, font=("Segoe UI", 9))
        self.ent_telefono.grid(row=1, column=2, padx=5, pady=(2, 5))

        # Dirección
        tk.Label(form, text="Dirección", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(
            row=2, column=0, sticky="w", padx=5
        )
        self.ent_direccion = tk.Entry(form, width=62, font=("Segoe UI", 9))
        self.ent_direccion.grid(row=3, column=0, columnspan=2, padx=5, pady=(2, 5), sticky="w")

        # ---------------------------------------------------------
        # BARRA DE BOTONES
        # ---------------------------------------------------------
        barra = tk.Frame(self, bg=BG_PROVEEDORES)
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
            command=self.guardar_proveedor,
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
            command=self.actualizar_proveedor,
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
            command=self.eliminar_proveedor,
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
        frame_busqueda = tk.Frame(self, bg=BG_PROVEEDORES)
        frame_busqueda.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(
            frame_busqueda,
            text="Buscar proveedor:",
            bg=BG_PROVEEDORES,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=(0, 5))

        self.ent_buscar = tk.Entry(frame_busqueda, width=35, font=("Segoe UI", 9))
        self.ent_buscar.pack(side="left", padx=5)

        tk.Button(
            frame_busqueda,
            text=" Buscar",
            bg=BTN_GUARDAR,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=3,
            command=self.buscar_proveedor,
        ).pack(side="left", padx=5)

        # Frame para la Tabla
        frame_tree = tk.LabelFrame(
            self,
            text=" Listado de Proveedores Registrados ",
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

        columnas = ("id", "nombre", "nit", "telefono", "direccion")
        self.tree = ttk.Treeview(frame_tree, columns=columnas, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="RAZÓN SOCIAL")
        self.tree.heading("nit", text="NIT")
        self.tree.heading("telefono", text="TELÉFONO")
        self.tree.heading("direccion", text="DIRECCIÓN")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=250)
        self.tree.column("nit", width=140)
        self.tree.column("telefono", width=140)
        self.tree.column("direccion", width=280)

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

    # ---------------------------------------------------------
    # MÉTODOS CRUD
    # ---------------------------------------------------------
    def guardar_proveedor(self):
        nombre = self.ent_nombre.get().strip()
        nit = self.ent_nit.get().strip()

        if not nombre or not nit:
            messagebox.showwarning("Validación", "Razón Social y NIT son campos obligatorios.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO proveedores (nombre, nit, telefono, direccion) VALUES (?, ?, ?, ?)",
                (nombre, nit, self.ent_telefono.get().strip(), self.ent_direccion.get().strip()),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Proveedor registrado correctamente.")
            self.cargar_proveedores()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el proveedor: {e}")

    def actualizar_proveedor(self):
        if not self.proveedor_id:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor de la tabla.")
            return

        nombre = self.ent_nombre.get().strip()
        nit = self.ent_nit.get().strip()

        if not nombre or not nit:
            messagebox.showwarning("Validación", "Razón Social y NIT son obligatorios.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE proveedores
                SET nombre = ?, nit = ?, telefono = ?, direccion = ?
                WHERE id = ?
                """,
                (nombre, nit, self.ent_telefono.get().strip(), self.ent_direccion.get().strip(), self.proveedor_id),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
            self.cargar_proveedores()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el proveedor: {e}")

    def eliminar_proveedor(self):
        if not self.proveedor_id:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este proveedor?")
        if confirmar:
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM proveedores WHERE id = ?", (self.proveedor_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
                self.cargar_proveedores()
                self.limpiar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el proveedor: {e}")

    def cargar_proveedores(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, nit, telefono, direccion FROM proveedores ORDER BY nombre ASC")
            datos = cursor.fetchall()
            conn.close()

            for fila in datos:
                self.tree.insert("", tk.END, values=fila)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proveedores: {e}")

    def buscar_proveedor(self):
        texto = self.ent_buscar.get().strip()

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, nit, telefono, direccion FROM proveedores WHERE nombre LIKE ? OR nit LIKE ?",
                (f"%{texto}%", f"%{texto}%"),
            )
            resultados = cursor.fetchall()
            conn.close()

            for fila in resultados:
                self.tree.insert("", tk.END, values=fila)
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {e}")

    def seleccionar_proveedor(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            datos = self.tree.item(seleccion[0])["values"]
            self.proveedor_id = datos[0]
            self.limpiar_formulario(reset_id=False)

            self.ent_nombre.insert(0, datos[1])
            self.ent_nit.insert(0, datos[2])
            self.ent_telefono.insert(0, datos[3])
            self.ent_direccion.insert(0, datos[4])

    def limpiar_formulario(self, reset_id=True):
        self.ent_nombre.delete(0, tk.END)
        self.ent_nit.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_direccion.delete(0, tk.END)
        if reset_id:
            self.proveedor_id = None
            if hasattr(self, "tree"):
                for item in self.tree.selection():
                    self.tree.selection_remove(item)
        self.ent_nombre.focus()
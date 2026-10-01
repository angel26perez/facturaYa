import tkinter as tk
from tkinter import ttk, messagebox

# Constantes de diseño corporativo
BG_CLIENTES = "#F8FAFC"        # Fondo general claro
CARD_BG = "#FFFFFF"             # Fondo de contenedores y formularios
TEXT_PRIMARY = "#0F172A"         # Texto principal
TEXT_SECONDARY = "#64748B"       # Texto secundario/subtítulos
BORDER_COLOR = "#E2E8F0"         # Bordes suaves

# Botones con colores profesionales
BTN_GUARDAR = "#16A34A"          # Verde
BTN_ACTUALIZAR = "#2563EB"       # Azul
BTN_ELIMINAR = "#DC2626"         # Rojo
BTN_LIMPIAR = "#64748B"          # Gris

from modules.database import conectar, obtener_ventas_por_cliente


class ClientesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_CLIENTES)
        self.pack(expand=True, fill="both")
        
        self.cliente_id = None
        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):
        # ---------------------------------------------------------
        # ENCABEZADO
        # ---------------------------------------------------------
        header = tk.Frame(self, bg=BG_CLIENTES)
        header.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(
            header,
            text="GESTIÓN Y DIRECTORIO DE CLIENTES",
            bg=BG_CLIENTES,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")

        # ---------------------------------------------------------
        # FORMULARIO
        # ---------------------------------------------------------
        form = tk.LabelFrame(
            self,
            text=" Información del Cliente ",
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

        # Fila 0: Nombre, Tipo Doc, N° Doc, Sexo
        tk.Label(form, text="Nombre completo *", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        self.ent_nombre = tk.Entry(form, width=32, font=("Segoe UI", 9))
        self.ent_nombre.grid(row=1, column=0, padx=5, pady=(2, 8))

        tk.Label(form, text="Tipo de documento", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(row=0, column=1, sticky="w", padx=5)
        self.cmb_tipo_documento = ttk.Combobox(
            form,
            width=24,
            state="readonly",
            values=["Cédula de Ciudadanía", "Tarjeta de Identidad", "NIT / Empresa", "Permiso Especial Permanente", "Pasaporte"],
            font=("Segoe UI", 9)
        )
        self.cmb_tipo_documento.grid(row=1, column=1, padx=5, pady=(2, 8))
        self.cmb_tipo_documento.current(0)

        tk.Label(form, text="Número de documento *", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=5)
        self.ent_documento = tk.Entry(form, width=22, font=("Segoe UI", 9))
        self.ent_documento.grid(row=1, column=2, padx=5, pady=(2, 8))

        tk.Label(form, text="Sexo / Genero", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(row=0, column=3, sticky="w", padx=5)
        self.cmb_sexo = ttk.Combobox(
            form,
            width=18,
            state="readonly",
            values=["Masculino", "Femenino", "Otro / LGBT+"],
            font=("Segoe UI", 9)
        )
        self.cmb_sexo.grid(row=1, column=3, padx=5, pady=(2, 8))
        self.cmb_sexo.current(0)

        # Fila 2: Teléfono, Dirección, Email
        tk.Label(form, text="Teléfono", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", padx=5)
        self.ent_telefono = tk.Entry(form, width=32, font=("Segoe UI", 9))
        self.ent_telefono.grid(row=3, column=0, padx=5, pady=(2, 5))

        tk.Label(form, text="Dirección", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(row=2, column=1, sticky="w", padx=5)
        self.ent_direccion = tk.Entry(form, width=26, font=("Segoe UI", 9))
        self.ent_direccion.grid(row=3, column=1, padx=5, pady=(2, 5))

        tk.Label(form, text="Correo Electrónico", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9, "bold")).grid(row=2, column=2, columnspan=2, sticky="w", padx=5)
        self.ent_email = tk.Entry(form, width=43, font=("Segoe UI", 9))
        self.ent_email.grid(row=3, column=2, columnspan=2, sticky="w", padx=5, pady=(2, 5))

        # ---------------------------------------------------------
        # BARRA DE BOTONES
        # ---------------------------------------------------------
        barra = tk.Frame(self, bg=BG_CLIENTES)
        barra.pack(fill="x", padx=20, pady=5)

        tk.Button(
            barra, text=" Guardar", bg=BTN_GUARDAR, fg="white", font=("Segoe UI", 9, "bold"),
            relief="flat", cursor="hand2", padx=15, pady=6, command=self.guardar_cliente
        ).pack(side="left", padx=(0, 5))

        tk.Button(
            barra, text=" Actualizar", bg=BTN_ACTUALIZAR, fg="white", font=("Segoe UI", 9, "bold"),
            relief="flat", cursor="hand2", padx=15, pady=6, command=self.actualizar_cliente
        ).pack(side="left", padx=5)

        tk.Button(
            barra, text=" Eliminar", bg=BTN_ELIMINAR, fg="white", font=("Segoe UI", 9, "bold"),
            relief="flat", cursor="hand2", padx=15, pady=6, command=self.eliminar_cliente
        ).pack(side="left", padx=5)

        tk.Button(
            barra, text=" Limpiar", bg=BTN_LIMPIAR, fg="white", font=("Segoe UI", 9, "bold"),
            relief="flat", cursor="hand2", padx=15, pady=6, command=self.limpiar_formulario
        ).pack(side="left", padx=5)

        # ---------------------------------------------------------
        # CONTENEDOR CENTRAL: TABLA CLIENTES E HISTORIAL
        # ---------------------------------------------------------
        cuerpo = tk.Frame(self, bg=BG_CLIENTES)
        cuerpo.pack(fill="both", expand=True, padx=20, pady=10)

        # Tabla Clientes
        frame_tabla = tk.LabelFrame(
            cuerpo, text=" Registro de Clientes ", bg=CARD_BG, fg=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"), highlightbackground=BORDER_COLOR, highlightthickness=1, bd=0
        )
        frame_tabla.pack(side="left", fill="both", expand=True, padx=(0, 5))

        columnas = ("id", "nombre", "tipo_documento", "documento", "sexo", "telefono", "direccion", "email")
        self.tree_clientes = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)

        self.tree_clientes.heading("id", text="ID")
        self.tree_clientes.heading("nombre", text="NOMBRE")
        self.tree_clientes.heading("tipo_documento", text="TIPO DOC.")
        self.tree_clientes.heading("documento", text="DOCUMENTO")
        self.tree_clientes.heading("sexo", text="SEXO")
        self.tree_clientes.heading("telefono", text="TELÉFONO")
        self.tree_clientes.heading("direccion", text="DIRECCIÓN")
        self.tree_clientes.heading("email", text="EMAIL")

        self.tree_clientes.column("id", width=40, anchor="center")
        self.tree_clientes.column("nombre", width=140)
        self.tree_clientes.column("tipo_documento", width=120)
        self.tree_clientes.column("documento", width=100)
        self.tree_clientes.column("sexo", width=80)
        self.tree_clientes.column("telefono", width=100)
        self.tree_clientes.column("direccion", width=120)
        self.tree_clientes.column("email", width=150)

        self.tree_clientes.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree_clientes.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

        # Tabla Historial Compras del Cliente
        frame_historial = tk.LabelFrame(
            cuerpo, text=" Historial de Compras del Cliente ", bg=CARD_BG, fg=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"), highlightbackground=BORDER_COLOR, highlightthickness=1, bd=0
        )
        frame_historial.pack(side="right", fill="both", expand=True, padx=(5, 0))

        cols_hist = ("num", "fecha", "vendedor", "total", "pago")
        self.tree_historial_ventas = ttk.Treeview(frame_historial, columns=cols_hist, show="headings", height=8)

        self.tree_historial_ventas.heading("num", text="N° Factura")
        self.tree_historial_ventas.heading("fecha", text="Fecha")
        self.tree_historial_ventas.heading("vendedor", text="Vendedor")
        self.tree_historial_ventas.heading("total", text="Total")
        self.tree_historial_ventas.heading("pago", text="Pago")

        self.tree_historial_ventas.column("num", width=80, anchor="center")
        self.tree_historial_ventas.column("fecha", width=100, anchor="center")
        self.tree_historial_ventas.column("vendedor", width=110)
        self.tree_historial_ventas.column("total", width=90, anchor="e")
        self.tree_historial_ventas.column("pago", width=90, anchor="center")

        self.tree_historial_ventas.pack(fill="both", expand=True, padx=5, pady=5)

    def guardar_cliente(self):
        nombre = self.ent_nombre.get().strip()
        tipo_documento = self.cmb_tipo_documento.get()
        documento = self.ent_documento.get().strip()
        sexo = self.cmb_sexo.get()
        telefono = self.ent_telefono.get().strip()
        direccion = self.ent_direccion.get().strip()
        email = self.ent_email.get().strip()

        if not nombre:
            messagebox.showwarning("Validación", "El nombre del cliente es obligatorio.")
            self.ent_nombre.focus()
            return

        if not documento:
            messagebox.showwarning("Validación", "El número de documento es obligatorio.")
            self.ent_documento.focus()
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO clientes (nombre, tipo_documento, documento, sexo, telefono, direccion, email)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (nombre, tipo_documento, documento, sexo, telefono, direccion, email),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self.limpiar_formulario()
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el cliente: {e}")

    def actualizar_cliente(self):
        if self.cliente_id is None:
            messagebox.showwarning("Actualizar", "Seleccione un cliente de la tabla.")
            return

        nombre = self.ent_nombre.get().strip()
        tipo_documento = self.cmb_tipo_documento.get()
        documento = self.ent_documento.get().strip()
        sexo = self.cmb_sexo.get()
        telefono = self.ent_telefono.get().strip()
        direccion = self.ent_direccion.get().strip()
        email = self.ent_email.get().strip()

        if not nombre or not documento:
            messagebox.showwarning("Validación", "Nombre y documento son campos obligatorios.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE clientes
                SET nombre = ?, tipo_documento = ?, documento = ?, sexo = ?, telefono = ?, direccion = ?, email = ?
                WHERE id = ?
                """,
                (nombre, tipo_documento, documento, sexo, telefono, direccion, email, self.cliente_id),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            self.limpiar_formulario()
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el cliente: {e}")

    def eliminar_cliente(self):
        if self.cliente_id is None:
            messagebox.showwarning("Eliminar", "Seleccione un cliente de la tabla.")
            return

        confirmar = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de eliminar este cliente?")
        if confirmar:
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id = ?", (self.cliente_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.limpiar_formulario()
                self.cargar_clientes()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")

    def cargar_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, nombre, tipo_documento, documento, sexo, telefono, direccion, email
                FROM clientes
                ORDER BY nombre ASC
                """
            )
            registros = cursor.fetchall()
            conn.close()

            for fila in registros:
                self.tree_clientes.insert("", "end", values=fila)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los clientes: {e}")

    def seleccionar_cliente(self, event):
        seleccion = self.tree_clientes.selection()
        if seleccion:
            datos = self.tree_clientes.item(seleccion[0], "values")
            self.cliente_id = datos[0]

            # Cargar datos al formulario
            self.ent_nombre.delete(0, tk.END)
            self.ent_documento.delete(0, tk.END)
            self.ent_telefono.delete(0, tk.END)
            self.ent_direccion.delete(0, tk.END)
            self.ent_email.delete(0, tk.END)

            self.ent_nombre.insert(0, datos[1])
            self.cmb_tipo_documento.set(datos[2])
            self.ent_documento.insert(0, datos[3])
            self.cmb_sexo.set(datos[4])
            self.ent_telefono.insert(0, datos[5])
            self.ent_direccion.insert(0, datos[6])
            self.ent_email.insert(0, datos[7])

            # Cargar historial de ventas del cliente
            self.cargar_historial_ventas_cliente(self.cliente_id)

    def cargar_historial_ventas_cliente(self, cliente_id):
        for item in self.tree_historial_ventas.get_children():
            self.tree_historial_ventas.delete(item)

        ventas = obtener_ventas_por_cliente(cliente_id)
        if ventas:
            for v in ventas:
                self.tree_historial_ventas.insert(
                    "",
                    "end",
                    values=(v[0], v[1], v[2], f"${v[3]:,.0f}", v[4]),
                )

    def limpiar_formulario(self):
        self.cliente_id = None
        self.ent_nombre.delete(0, tk.END)
        self.ent_documento.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_direccion.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.cmb_tipo_documento.current(0)
        self.cmb_sexo.current(0)

        if hasattr(self, "tree_clientes"):
            for item in self.tree_clientes.selection():
                self.tree_clientes.selection_remove(item)

        for item in self.tree_historial_ventas.get_children():
            self.tree_historial_ventas.delete(item)

        self.ent_nombre.focus()
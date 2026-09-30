import tkinter as tk
from tkinter import messagebox
from config import APP_NAME, COLOR_FONDO, COLOR_SECUNDARIO, EMPRESA, NIT
from modules.database import crear_tablas, insertar_productos_prueba

# Importación de módulos
from modules.dashboard import DashboardFrame
from modules.inventario import InventarioFrame
from modules.clientes import ClientesFrame
from modules.ventas import VentasFrame
from modules.reportes import ReportesFrame

# ==========================================
# PALETA DE COLORES PROFESIONAL / ENTERPRISE
# ==========================================
COLOR_BG_APP = "#F8FAFC"        # Fondo neutro claro
COLOR_NAVBAR = "#0F172A"        # Slate 900 (Azul medianoche)
COLOR_NAV_BTN = "#1E293B"       # Slate 800 (Fondo botones inactivos/hover)
COLOR_ACCENT = "#2563EB"        # Azul corporativo (Módulo activo)
COLOR_TEXT_LIGHT = "#F8FAFC"    # Texto blanco/claro
COLOR_TEXT_MUTED = "#94A3B8"    # Texto secundario en barra
COLOR_TEXT_DARK = "#0F172A"     # Texto principal en workspace

class SistemaFacturacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1366x768")
        self.root.configure(bg=COLOR_BG_APP)
        
        # Confirmación de salida al cerrar la ventana desde la 'X'
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_salida)
        
        self.botones_menu = {}
        self.crear_interfaz()

    def crear_interfaz(self):
        # ---------------------------------------------------------
        # BARRA SUPERIOR HORIZONTAL (NAVBAR)
        # ---------------------------------------------------------
        navbar = tk.Frame(self.root, bg=COLOR_NAVBAR, height=60)
        navbar.pack(side="top", fill="x")
        navbar.pack_propagate(False)

        # BRANDING / LOGO (Izquierda)
        brand_frame = tk.Frame(navbar, bg=COLOR_NAVBAR)
        brand_frame.pack(side="left", padx=(20, 30), pady=8)

        tk.Label(
            brand_frame,
            text="FacturaYA",
            bg=COLOR_NAVBAR,
            fg=COLOR_TEXT_LIGHT,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")

        tk.Label(
            brand_frame, 
            text="Sistema de Facturación", 
            bg=COLOR_NAVBAR, 
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="w")

        # MENÚ DE NAVEGACIÓN PRINCIPAL
        menus = [
            ("Dashboard", "📊 Dashboard"),
            ("Facturación", "💳 Facturación"),
            ("Inventario", "📦 Inventario"),
            ("Clientes", "👥 Clientes"),
            ("Reportes", "📈 Reportes"),
            ("Cerrar Sesión", "🚪 Cerrar Sesión")
        ]

        for clave, etiqueta in menus:
            btn = tk.Button(
                navbar,
                text=etiqueta,
                bg=COLOR_NAVBAR,
                fg=COLOR_TEXT_MUTED,
                activebackground=COLOR_NAV_BTN,
                activeforeground=COLOR_TEXT_LIGHT,
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                padx=16,
                bd=0,
                cursor="hand2",
                command=lambda op=clave: self.cargar_modulo(op),
            )
            btn.pack(side="left", fill="y", padx=1)
            self.botones_menu[clave] = btn

        # PANEL DE INFORMACIÓN INSTITUCIONAL (Derecha)
        info_frame = tk.Frame(navbar, bg="#020617", padx=20)
        info_frame.pack(side="right", fill="y")

        tk.Label(
            info_frame, 
            text=EMPRESA, 
            bg="#020617", 
            fg=COLOR_TEXT_LIGHT,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="e", pady=(10, 0))

        tk.Label(
            info_frame, 
            text=f"NIT: {NIT}", 
            bg="#020617", 
            fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="e")

        # ---------------------------------------------------------
        # ÁREA CENTRAL (WORKSPACE)
        # ---------------------------------------------------------
        self.workspace = tk.Frame(self.root, bg=COLOR_BG_APP)
        self.workspace.pack(expand=True, fill="both")

        # Cargar módulo inicial
        self.cargar_modulo("Dashboard")

    def limpiar_workspace(self):
        for widget in self.workspace.winfo_children():
            widget.destroy()

    def confirmar_salida(self):
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Está seguro de que desea cerrar la sesión actual y salir del sistema?",
            icon="warning"
        )
        if respuesta:
            self.root.destroy()

    def cargar_modulo(self, modulo):
        if modulo == "Cerrar Sesión":
            self.confirmar_salida()
            return

        # 1. Actualizar estilos de la barra de navegación
        for op, btn in self.botones_menu.items():
            btn.config(
                bg=COLOR_NAVBAR, 
                fg=COLOR_TEXT_MUTED, 
                activebackground=COLOR_NAV_BTN
            )

        if modulo in self.botones_menu:
            # Resaltar el botón activo con el color de acento azul
            self.botones_menu[modulo].config(
                bg=COLOR_ACCENT, 
                fg=COLOR_TEXT_LIGHT,
                activebackground=COLOR_ACCENT
            )

        # 2. Renderizar contenido en el workspace
        self.limpiar_workspace()

        if modulo == "Dashboard":
            DashboardFrame(self.workspace).pack(expand=True, fill="both")
        elif modulo == "Facturación":
            VentasFrame(self.workspace).pack(expand=True, fill="both")
        elif modulo == "Inventario":
            InventarioFrame(self.workspace).pack(expand=True, fill="both")
        elif modulo == "Clientes":
            ClientesFrame(self.workspace).pack(expand=True, fill="both")
        elif modulo == "Reportes":
            ReportesFrame(self.workspace).pack(expand=True, fill="both")


if __name__ == "__main__":
    crear_tablas()
    insertar_productos_prueba()

    root = tk.Tk()
    app = SistemaFacturacionApp(root)
    root.mainloop()
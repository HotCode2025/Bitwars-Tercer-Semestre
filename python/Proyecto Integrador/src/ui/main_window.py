"""
ui/main_window.py

Ventana principal de la aplicacion una vez autenticado el usuario.
Contiene un sidebar de navegacion fijo a la izquierda y un area de
contenido a la derecha donde se monta cada vista (clientes, proveedores,
servicios, turnos, pagos) sin abrir ventanas nuevas.
"""

import customtkinter as ctk
from ui.theme import theme

from ui.clientes_view import ClientesView
from ui.proveedores_view import ProveedoresView
from ui.servicios_view import ServiciosView
from ui.turnos_view import TurnosView
from ui.turnos_cliente_view import TurnosClienteView
from ui.pagos_view import PagosView
from ui.exportar_view import ExportarView

# Secciones que pueden ver los administradores
SECCIONES_ADMIN = [
    ("turnos", "🗓  Turnos", TurnosView),
    ("clientes", "👤  Clientes", ClientesView),
    ("proveedores", "🧑‍💼  Proveedores", ProveedoresView),
    ("servicios", "🧾  Servicios", ServiciosView),
    ("pagos", "💳  Pagos", PagosView),
    ("exportar", "⬇  Exportar CSV", ExportarView),
]

# Secciones que pueden ver los clientes
SECCIONES_CLIENTE = [
    ("turnos", "🗓  Turnos", TurnosClienteView),
]


def _secciones_por_rol(rol):
    if (rol or "").upper() == "ADMIN":
        return SECCIONES_ADMIN
    return SECCIONES_CLIENTE


class MainWindow(ctk.CTk):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        rol_usuario_init = usuario.get("rol") if isinstance(usuario, dict) \
            else (usuario["rol"] if usuario else "")
        self.secciones = _secciones_por_rol(rol_usuario_init)
        c = theme.colors

        self.title("Sistema de Turnos")
        self.geometry("1180x720")
        self.minsize(1000, 620)
        self.configure(fg_color=c["bg"])

        theme.suscribir(self._refrescar_colores)

        self._vista_actual_key = None
        self._vista_actual_widget = None
        self._botones_sidebar = {}

        self._construir_layout()
        self._ir_a_seccion("turnos")

    # ------------------------------------------------------------------
    def _construir_layout(self):
        c = theme.colors

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(
            self, width=232, fg_color=c["sidebar_bg"], corner_radius=0,
            border_width=0,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self._construir_sidebar()

        # Separador fino vertical entre sidebar y contenido
        self.sidebar_borde = ctk.CTkFrame(self, width=1, fg_color=c["sidebar_borde"],
                                           corner_radius=0)
        self.sidebar_borde.grid(row=0, column=1, sticky="ns")

        # --- Contenedor de vistas ---
        self.contenedor = ctk.CTkFrame(self, fg_color=c["bg"], corner_radius=0)
        self.contenedor.grid(row=0, column=2, sticky="nsew")
        self.contenedor.grid_columnconfigure(0, weight=1)
        self.contenedor.grid_rowconfigure(0, weight=1)

    def _construir_sidebar(self):
        for w in self.sidebar.winfo_children():
            w.destroy()
        c = theme.colors
        self.sidebar.configure(fg_color=c["sidebar_bg"])
        self._botones_sidebar = {}

        # Marca / encabezado
        marca = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        marca.pack(fill="x", padx=20, pady=(24, 10))
        theme.etiqueta(marca, "📅 Turnos", size=17, weight="bold").pack(anchor="w")

        nombre_usuario = self.usuario.get("nombre") if isinstance(self.usuario, dict) \
            else (self.usuario["nombre"] if self.usuario else "Usuario")
        rol_usuario = self.usuario.get("rol") if isinstance(self.usuario, dict) \
            else (self.usuario["rol"] if self.usuario else "")

        theme.etiqueta(
            marca, f"{nombre_usuario}", size=12, color=c["texto_secundario"],
        ).pack(anchor="w", pady=(6, 0))
        if rol_usuario:
            theme.badge(marca, rol_usuario, tipo="accent").pack(anchor="w", pady=(6, 0))

        theme.separador(self.sidebar).pack(fill="x", padx=20, pady=(14, 10))

        # Navegacion
        nav = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav.pack(fill="x", padx=12)

        for key, label, _ in self.secciones:
            btn = theme.boton_sidebar(
                nav, label, command=lambda k=key: self._ir_a_seccion(k),
            )
            btn.pack(fill="x", pady=3)
            self._botones_sidebar[key] = btn

        # Pie del sidebar: tema + logout
        pie = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        pie.pack(fill="x", side="bottom", padx=16, pady=20)

        theme.separador(self.sidebar).pack(fill="x", side="bottom", padx=20, pady=(0, 12))

        self.switch_tema = theme.switch(
            pie, text="Modo oscuro", command=self._on_toggle_tema,
        )
        if theme.modo == "dark":
            self.switch_tema.select()
        self.switch_tema.pack(fill="x", pady=(0, 10))

        theme.boton_secundario(
            pie, "Cerrar sesión", command=self._cerrar_sesion, width=200,
        ).pack(fill="x")

    # ------------------------------------------------------------------
    def _ir_a_seccion(self, key):
        if key == self._vista_actual_key:
            return

        for k, btn in self._botones_sidebar.items():
            if k == key:
                theme.marcar_sidebar_activo(btn)
            else:
                theme.marcar_sidebar_inactivo(btn)

        if self._vista_actual_widget is not None:
            self._vista_actual_widget.destroy()

        clase_vista = next((c for k, _, c in self.secciones if k == key), None)
        if clase_vista is None:
            return
        vista = clase_vista(self.contenedor, self.usuario)
        vista.grid(row=0, column=0, sticky="nsew")

        self._vista_actual_key = key
        self._vista_actual_widget = vista

    def _on_toggle_tema(self):
        theme.toggle_modo()

    def _refrescar_colores(self):
        self.configure(fg_color=theme.colors["bg"])
        self._construir_sidebar()
        self.sidebar_borde.configure(fg_color=theme.colors["sidebar_borde"])
        self.contenedor.configure(fg_color=theme.colors["bg"])
        for k, btn in self._botones_sidebar.items():
            if k == self._vista_actual_key:
                theme.marcar_sidebar_activo(btn)
        # refrescar el switch de tema tras reconstruir sidebar
        if theme.modo == "dark":
            self.switch_tema.select()
        else:
            self.switch_tema.deselect()
        # re-renderizar la vista actual para que tome los nuevos colores
        if self._vista_actual_key:
            key = self._vista_actual_key
            self._vista_actual_key = None
            self._ir_a_seccion(key)

    def _cerrar_sesion(self):
        from ui.login_view import LoginView
        self.destroy()
        login = LoginView()
        login.mainloop()
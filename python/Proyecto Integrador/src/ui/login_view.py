"""
ui/login_view.py

Pantalla de inicio de sesion y registro. Es la primera ventana que ve
el usuario. Al autenticar correctamente, cierra esta ventana y abre la
ventana principal (MainWindow) pasando el usuario autenticado.

Usa directamente las funciones ya existentes en src/auth.py, sin
modificar ese archivo.
"""

import customtkinter as ctk
from ui.theme import theme
from ui.widgets.toast import mostrar_toast

from auth import autenticar_usuario, registrar_usuario, validar_password


class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()
        c = theme.colors

        self.title("Sistema de Turnos — Iniciar sesión")
        self.geometry("960x600")
        self.minsize(860, 560)
        self.configure(fg_color=c["bg"])

        self._modo_registro = False
        self.usuario_autenticado = None

        theme.suscribir(self._refrescar_colores)

        self._construir_layout()

    # ------------------------------------------------------------------
    # Layout general: panel izquierdo de marca + panel derecho de form
    # ------------------------------------------------------------------
    def _construir_layout(self):
        c = theme.colors

        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # Panel de marca (izquierda)
        self.panel_marca = ctk.CTkFrame(self, fg_color=c["accent"], corner_radius=0)
        self.panel_marca.grid(row=0, column=0, sticky="nsew")
        self._construir_panel_marca()

        # Panel de formulario (derecha)
        self.panel_form = ctk.CTkFrame(self, fg_color=c["bg"], corner_radius=0)
        self.panel_form.grid(row=0, column=1, sticky="nsew")
        self._construir_panel_form()

    def _construir_panel_marca(self):
        for w in self.panel_marca.winfo_children():
            w.destroy()
        c = theme.colors
        self.panel_marca.configure(fg_color=c["accent"])

        contenedor = ctk.CTkFrame(self.panel_marca, fg_color="transparent")
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            contenedor, text="📅", font=theme.fuente(46),
        ).pack(pady=(0, 18))

        ctk.CTkLabel(
            contenedor, text="Sistema de Turnos",
            font=theme.fuente(26, "bold"), text_color=c["accent_texto"],
        ).pack()

        ctk.CTkLabel(
            contenedor,
            text="Gestioná clientes, proveedores,\nservicios y turnos en un solo lugar.",
            font=theme.fuente(13), text_color=c["accent_texto"],
            justify="center",
        ).pack(pady=(10, 0))

    def _construir_panel_form(self):
        for w in self.panel_form.winfo_children():
            w.destroy()
        c = theme.colors
        self.panel_form.configure(fg_color=c["bg"])

        # Switch de tema arriba a la derecha
        top_bar = ctk.CTkFrame(self.panel_form, fg_color="transparent")
        top_bar.pack(fill="x", padx=24, pady=(20, 0))

        self.switch_tema = theme.switch(
            top_bar, text="Modo oscuro", command=self._on_toggle_tema,
        )
        if theme.modo == "dark":
            self.switch_tema.select()
        self.switch_tema.pack(side="right")

        wrapper = ctk.CTkFrame(self.panel_form, fg_color="transparent")
        wrapper.place(relx=0.5, rely=0.5, anchor="center")
        self.form_wrapper = wrapper

        if self._modo_registro:
            self._construir_form_registro(wrapper)
        else:
            self._construir_form_login(wrapper)

    # ------------------------------------------------------------------
    # Formulario de login
    # ------------------------------------------------------------------
    def _construir_form_login(self, parent):
        c = theme.colors

        theme.etiqueta(parent, "Bienvenido de nuevo", size=22,
                        weight="bold").pack(anchor="w")
        theme.etiqueta(parent, "Ingresá tus datos para continuar", size=13,
                        color=c["texto_secundario"]).pack(anchor="w", pady=(4, 24))

        theme.etiqueta(parent, "Email", size=12, weight="bold",
                        color=c["texto_secundario"]).pack(anchor="w")
        self.entry_email = theme.entrada(parent, placeholder="tu@email.com", width=340)
        self.entry_email.pack(anchor="w", pady=(4, 16))

        theme.etiqueta(parent, "Contraseña", size=12, weight="bold",
                        color=c["texto_secundario"]).pack(anchor="w")
        self.entry_password = theme.entrada(parent, placeholder="••••••••",
                                              width=340, show="•")
        self.entry_password.pack(anchor="w", pady=(4, 6))
        self.entry_password.bind("<Return>", lambda e: self._intentar_login())

        self.lbl_error = theme.etiqueta(parent, "", size=12, color=c["peligro"])
        self.lbl_error.pack(anchor="w", pady=(0, 10))

        theme.boton_primario(
            parent, "Iniciar sesión", command=self._intentar_login,
            width=340, height=42,
        ).pack(anchor="w", pady=(8, 0))

        pie = ctk.CTkFrame(parent, fg_color="transparent")
        pie.pack(anchor="w", pady=(20, 0))
        theme.etiqueta(pie, "¿No tenés cuenta? ", size=12,
                        color=c["texto_secundario"]).pack(side="left")
        link = theme.etiqueta(pie, "Registrate", size=12, weight="bold",
                               color=c["accent"])
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: self._ir_a_registro())
        link.configure(cursor="hand2")

    def _intentar_login(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get()

        if not email or not password:
            self.lbl_error.configure(text="Completá email y contraseña.")
            return

        try:
            usuario = autenticar_usuario(email, password)
        except Exception as exc:
            self.lbl_error.configure(text=f"No se pudo conectar con la base de datos.")
            return

        if usuario is None:
            self.lbl_error.configure(text="Email o contraseña incorrectos.")
            return

        self.lbl_error.configure(text="")
        self.usuario_autenticado = usuario
        self._abrir_app_principal()

    # ------------------------------------------------------------------
    # Formulario de registro
    # ------------------------------------------------------------------
    def _construir_form_registro(self, parent):
        c = theme.colors

        theme.etiqueta(parent, "Crear cuenta", size=22, weight="bold").pack(anchor="w")
        theme.etiqueta(parent, "Completá tus datos para registrarte", size=13,
                        color=c["texto_secundario"]).pack(anchor="w", pady=(4, 20))

        theme.etiqueta(parent, "Nombre completo", size=12, weight="bold",
                        color=c["texto_secundario"]).pack(anchor="w")
        self.reg_nombre = theme.entrada(parent, placeholder="Juan Pérez", width=340)
        self.reg_nombre.pack(anchor="w", pady=(4, 12))

        theme.etiqueta(parent, "Teléfono", size=12, weight="bold",
                        color=c["texto_secundario"]).pack(anchor="w")
        self.reg_telefono = theme.entrada(parent, placeholder="261 1234567", width=340)
        self.reg_telefono.pack(anchor="w", pady=(4, 12))

        theme.etiqueta(parent, "Email", size=12, weight="bold",
                        color=c["texto_secundario"]).pack(anchor="w")
        self.reg_email = theme.entrada(parent, placeholder="tu@email.com", width=340)
        self.reg_email.pack(anchor="w", pady=(4, 12))

        theme.etiqueta(parent, "Contraseña", size=12, weight="bold",
                        color=c["texto_secundario"]).pack(anchor="w")
        self.reg_password = theme.entrada(
            parent, placeholder="Mín. 8 caracteres, 1 mayúscula, 1 símbolo",
            width=340, show="•",
        )
        self.reg_password.pack(anchor="w", pady=(4, 6))

        self.lbl_error_reg = theme.etiqueta(parent, "", size=12, color=c["peligro"])
        self.lbl_error_reg.pack(anchor="w", pady=(0, 10))

        theme.boton_primario(
            parent, "Crear cuenta", command=self._intentar_registro,
            width=340, height=42,
        ).pack(anchor="w", pady=(8, 0))

        pie = ctk.CTkFrame(parent, fg_color="transparent")
        pie.pack(anchor="w", pady=(20, 0))
        theme.etiqueta(pie, "¿Ya tenés cuenta? ", size=12,
                        color=c["texto_secundario"]).pack(side="left")
        link = theme.etiqueta(pie, "Iniciar sesión", size=12, weight="bold",
                               color=c["accent"])
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: self._ir_a_login())
        link.configure(cursor="hand2")

    def _intentar_registro(self):
        nombre = self.reg_nombre.get().strip()
        telefono = self.reg_telefono.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get()

        if not nombre or not email or not password:
            self.lbl_error_reg.configure(text="Completá los campos obligatorios.")
            return

        if not validar_password(password):
            self.lbl_error_reg.configure(
                text="La contraseña necesita 8+ caracteres, una mayúscula y un símbolo."
            )
            return

        try:
            registrar_usuario(nombre, telefono, email, password)
        except Exception as exc:
            self.lbl_error_reg.configure(text="No se pudo crear la cuenta. ¿Email ya registrado?")
            return

        self._ir_a_login()
        mostrar_toast(self, "Cuenta creada con éxito. Iniciá sesión.", tipo="exito")

    # ------------------------------------------------------------------
    def _ir_a_registro(self):
        self._modo_registro = True
        self._construir_panel_form()

    def _ir_a_login(self):
        self._modo_registro = False
        self._construir_panel_form()

    def _on_toggle_tema(self):
        theme.toggle_modo()

    def _refrescar_colores(self):
        self.configure(fg_color=theme.colors["bg"])
        self._construir_panel_marca()
        self._construir_panel_form()

    def _abrir_app_principal(self):
        from ui.main_window import MainWindow
        self.destroy()
        app = MainWindow(self.usuario_autenticado)
        app.mainloop()


def iniciar():
    login = LoginView()
    login.mainloop()

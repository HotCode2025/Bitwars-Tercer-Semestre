# sidebar.py — Barra lateral de navegación

import customtkinter as ctk
from theme import COLOR, FONT


class Sidebar(ctk.CTkFrame):
    """
    Barra lateral con logo y botones de navegación.
    Llama a on_navigate(nombre_vista) cuando el usuario selecciona una sección.
    """

    SECCIONES = [
        ("dashboard",   "📊  Dashboard"),
        ("turnos",      "📅  Turnos"),
        ("clientes",    "👥  Clientes"),
        ("proveedores", "🏪  Proveedores"),
        ("servicios",   "✂️   Servicios"),
        ("pagos",       "💳  Pagos"),
    ]

    def __init__(self, master, on_navigate, **kwargs):
        super().__init__(
            master,
            width=210,
            corner_radius=0,
            fg_color=COLOR["bg_sidebar"],
            **kwargs,
        )
        self.on_navigate = on_navigate
        self._botones: dict[str, ctk.CTkButton] = {}
        self._activo: str = ""

        self._construir()

    # ── Construcción ─────────────────────────────────────────────────────────

    def _construir(self):
        self.grid_propagate(False)
        self.grid_rowconfigure(20, weight=1)   # empuja el footer hacia abajo

        # Logo / título
        logo = ctk.CTkLabel(
            self,
            text="🗓  TurnoApp",
            font=("Segoe UI", 16, "bold"),
            text_color=COLOR["text_primary"],
            anchor="w",
        )
        logo.grid(row=0, column=0, padx=20, pady=(24, 4), sticky="ew")

        sub = ctk.CTkLabel(
            self,
            text="Bitwars · Proyecto Integrador",
            font=FONT["small"],
            text_color=COLOR["text_muted"],
            anchor="w",
        )
        sub.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        separador = ctk.CTkFrame(self, height=1, fg_color=COLOR["border"])
        separador.grid(row=2, column=0, padx=12, pady=(0, 12), sticky="ew")

        # Botones de sección
        for i, (clave, etiqueta) in enumerate(self.SECCIONES, start=3):
            btn = ctk.CTkButton(
                self,
                text=etiqueta,
                font=FONT["body"],
                anchor="w",
                height=38,
                corner_radius=8,
                fg_color="transparent",
                hover_color=COLOR["bg_hover"],
                text_color=COLOR["text_secondary"],
                command=lambda c=clave: self.seleccionar(c),
            )
            btn.grid(row=i, column=0, padx=10, pady=2, sticky="ew")
            self._botones[clave] = btn

        # Footer
        footer = ctk.CTkLabel(
            self,
            text="Tercer semestre · 2025",
            font=FONT["small"],
            text_color=COLOR["text_muted"],
        )
        footer.grid(row=21, column=0, padx=20, pady=16, sticky="s")

    # ── Lógica pública ───────────────────────────────────────────────────────

    def seleccionar(self, clave: str):
        """Marca el botón activo y dispara el callback."""
        if self._activo and self._activo in self._botones:
            self._botones[self._activo].configure(
                fg_color="transparent",
                text_color=COLOR["text_secondary"],
            )

        self._activo = clave
        self._botones[clave].configure(
            fg_color=COLOR["accent"],
            text_color=COLOR["text_primary"],
        )
        self.on_navigate(clave)
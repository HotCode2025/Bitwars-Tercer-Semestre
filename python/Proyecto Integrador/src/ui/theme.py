"""
theme.py

Sistema de theming centralizado para la aplicacion.

Define paleta de colores (claro / oscuro), tipografias, radios de
borde y helpers de construccion de widgets (botones, inputs, tarjetas)
con una estetica minimalista: bordes finos redondeados, colores neutros
y transiciones de hover suaves.

Uso:
    from ui.theme import theme

    boton = theme.boton_primario(parent, text="Guardar", command=...)
    theme.toggle_modo()  # alterna claro / oscuro en caliente
"""

import customtkinter as ctk


# ---------------------------------------------------------------------------
# Paletas de color
# ---------------------------------------------------------------------------
# Cada paleta define los mismos roles semanticos para que el resto del
# codigo de UI nunca tenga que preguntar "que modo estoy usando" -- solo
# pide theme.colors["bg"], theme.colors["accent"], etc.

PALETA_CLARA = {
    "bg":              "#FAFAFA",   # fondo general de la ventana
    "bg_secundario":   "#FFFFFF",   # tarjetas / paneles
    "bg_terciario":    "#F2F2F3",   # filas alternadas, hover sutil
    "borde":           "#E3E4E6",   # bordes finos grises claritos
    "borde_focus":     "#C7C9CC",
    "texto":           "#1C1C1E",
    "texto_secundario":"#6E6E73",
    "texto_disabled":  "#B0B0B5",
    "sidebar_bg":      "#FFFFFF",
    "sidebar_borde":   "#ECECEE",
    "input_bg":        "#FFFFFF",
    "input_bg_focus":  "#FFFFFF",

    "accent":          "#2F6FED",   # azul principal
    "accent_hover":    "#2860D0",
    "accent_texto":    "#FFFFFF",

    "secundario":      "#F0F1F3",   # botones secundarios (fondo claro)
    "secundario_hover":"#E5E6E9",
    "secundario_texto":"#1C1C1E",

    "exito":           "#1FA45C",
    "exito_hover":     "#188C4D",
    "peligro":         "#E5484D",
    "peligro_hover":   "#D03A3F",
    "advertencia":     "#E0A100",
    "advertencia_hover":"#C68E00",

    "scrollbar":       "#E3E4E6",
    "scrollbar_hover": "#C7C9CC",
}

PALETA_OSCURA = {
    "bg":              "#1A1A1C",
    "bg_secundario":   "#222224",
    "bg_terciario":    "#2A2A2D",
    "borde":           "#343437",
    "borde_focus":     "#46464A",
    "texto":           "#F2F2F3",
    "texto_secundario":"#9C9CA3",
    "texto_disabled":  "#5C5C60",
    "sidebar_bg":      "#1F1F21",
    "sidebar_borde":   "#2C2C2F",
    "input_bg":        "#262628",
    "input_bg_focus":  "#2C2C2F",

    "accent":          "#4C8DFF",
    "accent_hover":    "#699BFF",
    "accent_texto":    "#0D0D0E",

    "secundario":      "#2A2A2D",
    "secundario_hover":"#343437",
    "secundario_texto":"#F2F2F3",

    "exito":           "#34C77B",
    "exito_hover":     "#2BAE6B",
    "peligro":         "#FF6369",
    "peligro_hover":   "#E5484D",
    "advertencia":     "#F2B705",
    "advertencia_hover":"#D9A400",

    "scrollbar":       "#343437",
    "scrollbar_hover": "#46464A",
}


# ---------------------------------------------------------------------------
# Tipografia y geometria
# ---------------------------------------------------------------------------

FUENTE_FAMILIA = "Segoe UI"

RADIO_SM = 8
RADIO_MD = 12
RADIO_LG = 16

DURACION_HOVER_MS = 90  # animaciones de hover rapidas y fluidas


class Theme:
    """
    Punto unico de acceso a colores, fuentes y fabricas de widgets.

    Se instancia una sola vez (ver instancia `theme` al final del modulo)
    y se importa desde cualquier vista. Mantiene una lista de callbacks
    para poder refrescar pantallas abiertas cuando se cambia de modo.
    """

    def __init__(self):
        self.modo = "light"
        self.colors = PALETA_CLARA
        self._listeners = []

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    # -- gestion de modo -----------------------------------------------

    def set_modo(self, modo: str):
        """modo: 'light' o 'dark'"""
        self.modo = modo
        self.colors = PALETA_CLARA if modo == "light" else PALETA_OSCURA
        ctk.set_appearance_mode(modo)
        for callback in self._listeners:
            try:
                callback()
            except Exception:
                pass

    def toggle_modo(self):
        self.set_modo("dark" if self.modo == "light" else "light")

    def suscribir(self, callback):
        """Registra una funcion sin argumentos a llamar al cambiar de tema."""
        self._listeners.append(callback)

    # -- tipografia -------------------------------------------------------

    def fuente(self, size=14, weight="normal"):
        return ctk.CTkFont(family=FUENTE_FAMILIA, size=size, weight=weight)

    def fuente_titulo(self):
        return self.fuente(22, "bold")

    def fuente_subtitulo(self):
        return self.fuente(15, "bold")

    def fuente_texto(self):
        return self.fuente(13, "normal")

    def fuente_pequena(self):
        return self.fuente(11, "normal")

    # -- fabricas de widgets ------------------------------------------------

    def boton_primario(self, parent, text, command=None, width=140, height=38, **kwargs):
        c = self.colors
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=RADIO_MD,
            fg_color=c["accent"],
            hover_color=c["accent_hover"],
            text_color=c["accent_texto"],
            font=self.fuente(13, "bold"),
            border_width=0,
            **kwargs,
        )

    def boton_secundario(self, parent, text, command=None, width=140, height=38, **kwargs):
        c = self.colors
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=RADIO_MD,
            fg_color=c["secundario"],
            hover_color=c["secundario_hover"],
            text_color=c["secundario_texto"],
            font=self.fuente(13, "bold"),
            border_width=1,
            border_color=c["borde"],
            **kwargs,
        )

    def boton_peligro(self, parent, text, command=None, width=140, height=38, **kwargs):
        c = self.colors
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=RADIO_MD,
            fg_color=c["peligro"],
            hover_color=c["peligro_hover"],
            text_color="#FFFFFF",
            font=self.fuente(13, "bold"),
            border_width=0,
            **kwargs,
        )

    def boton_exito(self, parent, text, command=None, width=140, height=38, **kwargs):
        c = self.colors
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=RADIO_MD,
            fg_color=c["exito"],
            hover_color=c["exito_hover"],
            text_color="#FFFFFF",
            font=self.fuente(13, "bold"),
            border_width=0,
            **kwargs,
        )

    def boton_icono(self, parent, text, command=None, size=36, **kwargs):
        """Boton cuadrado compacto, pensado para iconos/acciones de fila (texto-emoji)."""
        c = self.colors
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=size,
            height=size,
            corner_radius=RADIO_SM,
            fg_color="transparent",
            hover_color=c["bg_terciario"],
            text_color=c["texto_secundario"],
            font=self.fuente(14),
            border_width=0,
            **kwargs,
        )

    def boton_sidebar(self, parent, text, command=None, **kwargs):
        """Boton de navegacion para el menu lateral: ancho completo, alineado a la izquierda."""
        c = self.colors
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            anchor="w",
            width=200,
            height=42,
            corner_radius=RADIO_SM,
            fg_color="transparent",
            hover_color=c["bg_terciario"],
            text_color=c["texto_secundario"],
            font=self.fuente(13, "bold"),
            border_width=0,
            **kwargs,
        )

    def marcar_sidebar_activo(self, boton):
        c = self.colors
        boton.configure(fg_color=c["accent"], text_color=c["accent_texto"],
                         hover_color=c["accent"])

    def marcar_sidebar_inactivo(self, boton):
        c = self.colors
        boton.configure(fg_color="transparent", text_color=c["texto_secundario"],
                         hover_color=c["bg_terciario"])

    def entrada(self, parent, placeholder="", width=260, height=38, show=None, **kwargs):
        c = self.colors
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            width=width,
            height=height,
            corner_radius=RADIO_SM,
            fg_color=c["input_bg"],
            border_color=c["borde"],
            border_width=1,
            text_color=c["texto"],
            placeholder_text_color=c["texto_secundario"],
            font=self.fuente(13),
            show=show,
            **kwargs,
        )

    def combobox(self, parent, values, width=260, height=38, **kwargs):
        c = self.colors
        return ctk.CTkComboBox(
            parent,
            values=values,
            width=width,
            height=height,
            corner_radius=RADIO_SM,
            fg_color=c["input_bg"],
            border_color=c["borde"],
            border_width=1,
            button_color=c["bg_terciario"],
            button_hover_color=c["secundario_hover"],
            dropdown_fg_color=c["bg_secundario"],
            dropdown_hover_color=c["bg_terciario"],
            text_color=c["texto"],
            font=self.fuente(13),
            **kwargs,
        )

    def tarjeta(self, parent, **kwargs):
        """Panel tipo card: fondo secundario, borde fino, esquinas redondeadas."""
        c = self.colors
        return ctk.CTkFrame(
            parent,
            corner_radius=RADIO_LG,
            fg_color=c["bg_secundario"],
            border_width=1,
            border_color=c["borde"],
            **kwargs,
        )

    def panel(self, parent, **kwargs):
        """Frame simple sin borde, para agrupar contenido."""
        c = self.colors
        return ctk.CTkFrame(parent, corner_radius=0, fg_color=c["bg"], **kwargs)

    def etiqueta(self, parent, text, size=13, weight="normal", color=None, **kwargs):
        c = self.colors
        return ctk.CTkLabel(
            parent,
            text=text,
            font=self.fuente(size, weight),
            text_color=color or c["texto"],
            **kwargs,
        )

    def badge(self, parent, text, tipo="neutral", **kwargs):
        """
        Pildora de estado pequeña y redondeada (para PENDIENTE / CONFIRMADO / etc).
        tipo: 'exito' | 'peligro' | 'advertencia' | 'neutral' | 'accent'
        """
        c = self.colors
        mapa_fg = {
            "exito": c["exito"],
            "peligro": c["peligro"],
            "advertencia": c["advertencia"],
            "accent": c["accent"],
            "neutral": c["texto_secundario"],
        }
        color = mapa_fg.get(tipo, c["texto_secundario"])
        return ctk.CTkLabel(
            parent,
            text=f"  {text}  ",
            font=self.fuente(11, "bold"),
            text_color=color,
            fg_color=c["bg_terciario"],
            corner_radius=999,
            **kwargs,
        )

    def separador(self, parent, **kwargs):
        c = self.colors
        return ctk.CTkFrame(parent, height=1, fg_color=c["borde"], **kwargs)

    def switch(self, parent, text="", command=None, **kwargs):
        c = self.colors
        return ctk.CTkSwitch(
            parent,
            text=text,
            command=command,
            progress_color=c["accent"],
            button_color="#FFFFFF",
            button_hover_color="#FFFFFF",
            fg_color=c["bg_terciario"],
            font=self.fuente(13),
            text_color=c["texto"],
            **kwargs,
        )

    def scrollable_frame(self, parent, **kwargs):
        c = self.colors
        return ctk.CTkScrollableFrame(
            parent,
            fg_color=c["bg"],
            scrollbar_button_color=c["scrollbar"],
            scrollbar_button_hover_color=c["scrollbar_hover"],
            corner_radius=0,
            **kwargs,
        )


# Instancia unica compartida por toda la app
theme = Theme()

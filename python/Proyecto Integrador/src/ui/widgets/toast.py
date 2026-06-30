"""
widgets/toast.py

Notificacion flotante (toast) que aparece en la esquina inferior derecha
de la ventana, con auto-cierre. Reemplaza a los messagebox nativos de
Tk para mantener consistencia visual con el resto de la app.
"""

import customtkinter as ctk
from ui.theme import theme


class Toast(ctk.CTkFrame):
    def __init__(self, parent_window, mensaje, tipo="exito", duracion_ms=2800):
        c = theme.colors
        color_map = {
            "exito": c["exito"],
            "peligro": c["peligro"],
            "advertencia": c["advertencia"],
            "info": c["accent"],
        }
        icono_map = {
            "exito": "✓",
            "peligro": "✕",
            "advertencia": "!",
            "info": "i",
        }
        color = color_map.get(tipo, c["accent"])

        super().__init__(
            parent_window,
            fg_color=c["bg_secundario"],
            corner_radius=12,
            border_width=1,
            border_color=c["borde"],
        )

        contenido = ctk.CTkFrame(self, fg_color="transparent")
        contenido.pack(padx=14, pady=10)

        badge = ctk.CTkLabel(
            contenido, text=icono_map.get(tipo, "i"), width=22, height=22,
            corner_radius=11, fg_color=color, text_color="#FFFFFF",
            font=theme.fuente(11, "bold"),
        )
        badge.pack(side="left", padx=(0, 10))

        theme.etiqueta(contenido, mensaje, size=13).pack(side="left")

        self.parent_window = parent_window
        self.place(relx=1.0, rely=1.0, x=-24, y=-24, anchor="se")
        self.lift()

        parent_window.after(duracion_ms, self._cerrar)

    def _cerrar(self):
        try:
            self.destroy()
        except Exception:
            pass


def mostrar_toast(parent_window, mensaje, tipo="exito"):
    return Toast(parent_window, mensaje, tipo=tipo)

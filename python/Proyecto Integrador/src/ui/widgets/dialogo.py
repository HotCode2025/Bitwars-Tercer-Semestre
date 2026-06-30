"""
widgets/dialogo.py

Ventana modal reutilizable para formularios de creacion / edicion.
Centra el dialogo sobre la ventana padre, bloquea interaccion con el
resto de la app (grab_set) y expone un area de contenido (self.body)
donde cada vista agrega sus propios campos.
"""

import customtkinter as ctk
from ui.theme import theme, RADIO_LG


class DialogoFormulario(ctk.CTkToplevel):
    def __init__(self, parent, titulo="Formulario", ancho=420, alto=480):
        super().__init__(parent)
        c = theme.colors

        self.title(titulo)
        self.geometry(f"{ancho}x{alto}")
        self.resizable(False, False)
        self.configure(fg_color=c["bg"])

        self.transient(parent)
        self.lift()
        self.after(50, self.grab_set)
        self.focus_force()

        self._centrar(parent, ancho, alto)

        # --- encabezado ---
        header = ctk.CTkFrame(self, fg_color="transparent", height=56)
        header.pack(fill="x", padx=24, pady=(20, 4))
        theme.etiqueta(header, titulo, size=18, weight="bold").pack(side="left")

        theme.separador(self).pack(fill="x", padx=24, pady=(8, 0))

        # --- area de contenido scrolleable ---
        self.body = theme.scrollable_frame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=24, pady=12)

        # --- footer de acciones ---
        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.pack(fill="x", padx=24, pady=(4, 20))

    def _centrar(self, parent, ancho, alto):
        self.update_idletasks()
        try:
            px = parent.winfo_rootx()
            py = parent.winfo_rooty()
            pw = parent.winfo_width()
            ph = parent.winfo_height()
            x = px + (pw - ancho) // 2
            y = py + (ph - alto) // 2
        except Exception:
            x, y = 200, 120
        self.geometry(f"{ancho}x{alto}+{max(x, 0)}+{max(y, 0)}")

    def agregar_campo_label(self, texto):
        theme.etiqueta(self.body, texto, size=12, weight="bold",
                        color=theme.colors["texto_secundario"]).pack(
            anchor="w", pady=(10, 4)
        )

    def agregar_botones(self, texto_confirmar, on_confirmar, on_cancelar=None,
                         tipo_confirmar="primario"):
        fabricante = {
            "primario": theme.boton_primario,
            "exito": theme.boton_exito,
            "peligro": theme.boton_peligro,
        }.get(tipo_confirmar, theme.boton_primario)

        btn_cancelar = theme.boton_secundario(
            self.footer, "Cancelar",
            command=on_cancelar or self.destroy,
            width=120,
        )
        btn_cancelar.pack(side="right", padx=(8, 0))

        btn_confirmar = fabricante(
            self.footer, texto_confirmar,
            command=on_confirmar,
            width=160,
        )
        btn_confirmar.pack(side="right")


def mostrar_confirmacion(parent, titulo, mensaje, on_confirmar, texto_confirmar="Eliminar"):
    """Dialogo corto de confirmacion (usado antes de eliminar registros)."""
    c = theme.colors
    win = ctk.CTkToplevel(parent)
    win.title(titulo)
    win.geometry("360x190")
    win.resizable(False, False)
    win.configure(fg_color=c["bg"])
    win.transient(parent)
    win.lift()
    win.after(50, win.grab_set)
    win.focus_force()

    win.update_idletasks()
    try:
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        x = px + (pw - 360) // 2
        y = py + (ph - 190) // 2
        win.geometry(f"360x190+{max(x,0)}+{max(y,0)}")
    except Exception:
        pass

    contenido = ctk.CTkFrame(win, fg_color="transparent")
    contenido.pack(fill="both", expand=True, padx=24, pady=20)

    theme.etiqueta(contenido, titulo, size=16, weight="bold").pack(anchor="w")
    theme.etiqueta(
        contenido, mensaje, size=13, color=c["texto_secundario"]
    ).pack(anchor="w", pady=(8, 0))

    botones = ctk.CTkFrame(contenido, fg_color="transparent")
    botones.pack(fill="x", side="bottom", pady=(20, 0))

    def confirmar():
        win.destroy()
        on_confirmar()

    theme.boton_secundario(botones, "Cancelar", command=win.destroy,
                            width=110).pack(side="right", padx=(8, 0))
    theme.boton_peligro(botones, texto_confirmar, command=confirmar,
                         width=110).pack(side="right")

    return win

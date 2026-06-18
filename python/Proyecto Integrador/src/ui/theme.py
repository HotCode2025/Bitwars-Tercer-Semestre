# theme.py — Paleta y constantes visuales compartidas por todas las vistas

import customtkinter as ctk

# ── Configuración global de apariencia ──────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Colores ──────────────────────────────────────────────────────────────────
COLOR = {
    # Fondo
    "bg_app":       "#1a1a2e",
    "bg_sidebar":   "#16213e",
    "bg_card":      "#0f3460",
    "bg_input":     "#1a1a2e",
    "bg_hover":     "#1e2a45",
    "bg_selected":  "#534ab7",

    # Texto
    "text_primary":   "#e8e8f0",
    "text_secondary": "#9090aa",
    "text_muted":     "#5a5a7a",

    # Acento principal (púrpura)
    "accent":         "#534ab7",
    "accent_hover":   "#3c3489",
    "accent_light":   "#eeedfe",

    # Estados de turno
    "pendiente":      "#EF9F27",
    "confirmado":     "#1D9E75",
    "completado":     "#534AB7",
    "cancelado":      "#E24B4A",
    "no_asistio":     "#888780",

    # Borde
    "border":         "#2a2a4a",
}

# ── Fuentes ───────────────────────────────────────────────────────────────────
FONT = {
    "title":    ("Segoe UI", 20, "bold"),
    "subtitle": ("Segoe UI", 14, "bold"),
    "body":     ("Segoe UI", 13),
    "small":    ("Segoe UI", 11),
    "button":   ("Segoe UI", 13, "bold"),
    "table_h":  ("Segoe UI", 11, "bold"),
    "table_b":  ("Segoe UI", 12),
}

# ── Estados válidos ───────────────────────────────────────────────────────────
ESTADOS_TURNO = ["PENDIENTE", "CONFIRMADO", "COMPLETADO", "CANCELADO", "NO_ASISTIO"]
ESTADOS_PAGO  = ["PENDIENTE", "PAGADO", "REEMBOLSADO"]
METODOS_PAGO  = ["Efectivo", "Tarjeta de débito", "Tarjeta de crédito", "Transferencia"]


def color_estado_turno(estado: str) -> str:
    """Devuelve el color hex correspondiente al estado de un turno."""
    return COLOR.get(estado.lower(), COLOR["text_secondary"])


def aplicar_tema_ventana(ventana: ctk.CTk | ctk.CTkToplevel) -> None:
    """Aplica fondo y tamaño mínimo estándar a una ventana."""
    ventana.configure(fg_color=COLOR["bg_app"])
    ventana.minsize(960, 620)
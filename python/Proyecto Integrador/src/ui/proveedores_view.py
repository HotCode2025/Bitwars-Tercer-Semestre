"""
ui/proveedores_view.py

Vista de gestion de proveedores (tabla `proveedores`).
"""

import customtkinter as ctk
from ui.theme import theme
from ui.widgets.tabla import Tabla
from ui.widgets.dialogo import DialogoFormulario, mostrar_confirmacion
from ui.widgets.toast import mostrar_toast

from repositories.proveedores import (
    obtener_proveedores,
    crear_proveedor,
    actualizar_proveedor,
    eliminar_proveedor,
)


def _campo(fila, clave, idx):
    if isinstance(fila, dict):
        return fila.get(clave)
    try:
        return fila[idx]
    except Exception:
        return None


class ProveedoresView(ctk.CTkFrame):
    def __init__(self, parent, usuario_actual):
        c = theme.colors
        super().__init__(parent, fg_color=c["bg"], corner_radius=0)
        self.usuario_actual = usuario_actual

        self._construir()
        self.recargar()

    def _construir(self):
        c = theme.colors

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 16))
        header.grid_columnconfigure(0, weight=1)

        titulo_box = ctk.CTkFrame(header, fg_color="transparent")
        titulo_box.grid(row=0, column=0, sticky="w")
        theme.etiqueta(titulo_box, "Proveedores", size=22, weight="bold").pack(anchor="w")
        theme.etiqueta(
            titulo_box, "Profesionales y prestadores que atienden turnos.",
            size=13, color=c["texto_secundario"],
        ).pack(anchor="w", pady=(2, 0))

        theme.boton_primario(
            header, "+ Nuevo proveedor", command=self._abrir_dialogo_crear, width=180,
        ).grid(row=0, column=1, sticky="e")

        tarjeta = theme.tarjeta(self)
        tarjeta.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 28))
        tarjeta.grid_columnconfigure(0, weight=1)
        tarjeta.grid_rowconfigure(0, weight=1)

        self.tabla = Tabla(
            tarjeta,
            columnas=[
                ("Nombre", 3),
                ("Teléfono", 2),
                ("Email", 3),
            ],
            on_editar=self._abrir_dialogo_editar,
            on_eliminar=self._confirmar_eliminar,
        )
        self.tabla.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

    def recargar(self):
        try:
            filas = obtener_proveedores()
        except Exception:
            filas = []
            mostrar_toast(self.winfo_toplevel(),
                          "No se pudo conectar con la base de datos.", tipo="peligro")

        self.tabla.cargar_filas(
            filas,
            valores_por_fila=lambda f: [
                _campo(f, "nombre", 1),
                _campo(f, "telefono", 2) or "—",
                _campo(f, "email", 3) or "—",
            ],
        )

    # ------------------------------------------------------------------
    def _abrir_dialogo_crear(self):
        dialogo = DialogoFormulario(self.winfo_toplevel(), titulo="Nuevo proveedor", alto=380)

        dialogo.agregar_campo_label("Nombre completo")
        entry_nombre = theme.entrada(dialogo.body, placeholder="Dr. Carlos Gómez", width=340)
        entry_nombre.pack(anchor="w")

        dialogo.agregar_campo_label("Teléfono")
        entry_telefono = theme.entrada(dialogo.body, placeholder="261 1234567", width=340)
        entry_telefono.pack(anchor="w")

        dialogo.agregar_campo_label("Email")
        entry_email = theme.entrada(dialogo.body, placeholder="proveedor@email.com", width=340)
        entry_email.pack(anchor="w")

        lbl_error = theme.etiqueta(dialogo.body, "", size=12, color=theme.colors["peligro"])
        lbl_error.pack(anchor="w", pady=(10, 0))

        def confirmar():
            nombre = entry_nombre.get().strip()
            telefono = entry_telefono.get().strip()
            email = entry_email.get().strip()

            if not nombre:
                lbl_error.configure(text="El nombre es obligatorio.")
                return

            try:
                crear_proveedor(nombre, telefono, email)
            except Exception:
                lbl_error.configure(text="No se pudo crear el proveedor.")
                return

            dialogo.destroy()
            self.recargar()
            mostrar_toast(self.winfo_toplevel(), "Proveedor creado con éxito.", tipo="exito")

        dialogo.agregar_botones("Crear proveedor", confirmar)

    def _abrir_dialogo_editar(self, fila):
        id_proveedor = _campo(fila, "id_proveedor", 0)
        dialogo = DialogoFormulario(self.winfo_toplevel(), titulo="Editar proveedor", alto=380)

        dialogo.agregar_campo_label("Nombre completo")
        entry_nombre = theme.entrada(dialogo.body, width=340)
        entry_nombre.insert(0, _campo(fila, "nombre", 1) or "")
        entry_nombre.pack(anchor="w")

        dialogo.agregar_campo_label("Teléfono")
        entry_telefono = theme.entrada(dialogo.body, width=340)
        entry_telefono.insert(0, _campo(fila, "telefono", 2) or "")
        entry_telefono.pack(anchor="w")

        dialogo.agregar_campo_label("Email")
        entry_email = theme.entrada(dialogo.body, width=340)
        entry_email.insert(0, _campo(fila, "email", 3) or "")
        entry_email.pack(anchor="w")

        lbl_error = theme.etiqueta(dialogo.body, "", size=12, color=theme.colors["peligro"])
        lbl_error.pack(anchor="w", pady=(10, 0))

        def confirmar():
            nombre = entry_nombre.get().strip()
            telefono = entry_telefono.get().strip()
            email = entry_email.get().strip()

            if not nombre:
                lbl_error.configure(text="El nombre es obligatorio.")
                return

            try:
                actualizar_proveedor(id_proveedor, nombre, telefono, email)
            except Exception:
                lbl_error.configure(text="No se pudo actualizar el proveedor.")
                return

            dialogo.destroy()
            self.recargar()
            mostrar_toast(self.winfo_toplevel(), "Proveedor actualizado.", tipo="exito")

        dialogo.agregar_botones("Guardar cambios", confirmar)

    def _confirmar_eliminar(self, fila):
        id_proveedor = _campo(fila, "id_proveedor", 0)
        nombre = _campo(fila, "nombre", 1)

        def eliminar():
            try:
                eliminar_proveedor(id_proveedor)
                self.recargar()
                mostrar_toast(self.winfo_toplevel(), "Proveedor eliminado.", tipo="exito")
            except Exception:
                mostrar_toast(self.winfo_toplevel(),
                              "No se pudo eliminar (puede tener turnos asociados).",
                              tipo="peligro")

        mostrar_confirmacion(
            self.winfo_toplevel(),
            "Eliminar proveedor",
            f"¿Seguro que querés eliminar a {nombre}? Esta acción no se puede deshacer.",
            on_confirmar=eliminar,
        )

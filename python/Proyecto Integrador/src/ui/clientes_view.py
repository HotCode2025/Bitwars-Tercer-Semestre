"""
ui/clientes_view.py

Vista de gestion de clientes (tabla `usuarios`).
Permite ver, editar y eliminar usuarios mediante las funciones
ya existentes en src/repositories/usuarios.py (no se modifica ese archivo).

Nota: los clientes se dan de alta ellos mismos desde la pantalla de
registro (ui/login_view.py). El administrador NO crea clientes manualmente
desde aca, por eso no hay boton "Nuevo cliente" ni dialogo de creacion.
"""

import customtkinter as ctk
from ui.theme import theme
from ui.widgets.tabla import Tabla
from ui.widgets.dialogo import DialogoFormulario, mostrar_confirmacion
from ui.widgets.toast import mostrar_toast

from repositories.usuarios import (
    obtener_usuarios,
    actualizar_usuario,
    eliminar_usuario,
)


def _campo(fila, clave, idx):
    """Acceso tolerante: sirve tanto si la fila es dict (RealDictCursor) como tupla."""
    if isinstance(fila, dict):
        return fila.get(clave)
    try:
        return fila[idx]
    except Exception:
        return None


class ClientesView(ctk.CTkFrame):
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
        theme.etiqueta(titulo_box, "Clientes", size=22, weight="bold").pack(anchor="w")
        theme.etiqueta(
            titulo_box, "Gestioná los usuarios registrados en el sistema.",
            size=13, color=c["texto_secundario"],
        ).pack(anchor="w", pady=(2, 0))

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
                ("Rol", 1),
            ],
            on_editar=self._abrir_dialogo_editar,
            on_eliminar=self._confirmar_eliminar,
        )
        self.tabla.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

    def recargar(self):
        try:
            filas = obtener_usuarios()
        except Exception:
            filas = []
            mostrar_toast(self.winfo_toplevel(),
                          "No se pudo conectar con la base de datos.", tipo="peligro")

        # Esta vista es de "Clientes": no debe mostrar cuentas de ADMIN,
        # esas se gestionan aparte (evita que datos del administrador
        # aparezcan mezclados en el listado de clientes).
        filas = [
            f for f in filas
            if (_campo(f, "rol", 5) or "CLIENTE").upper() == "CLIENTE"
        ]

        self.tabla.cargar_filas(
            filas,
            valores_por_fila=lambda f: [
                _campo(f, "nombre", 1),
                _campo(f, "telefono", 2) or "—",
                _campo(f, "email", 3),
                _campo(f, "rol", 5) or "CLIENTE",
            ],
        )

    # ------------------------------------------------------------------
    def _abrir_dialogo_editar(self, fila):
        id_usuario = _campo(fila, "id_usuario", 0)
        dialogo = DialogoFormulario(self.winfo_toplevel(), titulo="Editar cliente", alto=400)

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

            if not nombre or not email:
                lbl_error.configure(text="Nombre y email son obligatorios.")
                return

            try:
                actualizar_usuario(id_usuario, nombre, telefono, email)
            except Exception:
                lbl_error.configure(text="No se pudo actualizar el cliente.")
                return

            dialogo.destroy()
            self.recargar()
            mostrar_toast(self.winfo_toplevel(), "Cliente actualizado.", tipo="exito")

        dialogo.agregar_botones("Guardar cambios", confirmar)

    def _confirmar_eliminar(self, fila):
        id_usuario = _campo(fila, "id_usuario", 0)
        nombre = _campo(fila, "nombre", 1)

        def eliminar():
            try:
                eliminar_usuario(id_usuario)
                self.recargar()
                mostrar_toast(self.winfo_toplevel(), "Cliente eliminado.", tipo="exito")
            except Exception:
                mostrar_toast(self.winfo_toplevel(),
                              "No se pudo eliminar (puede tener turnos asociados).",
                              tipo="peligro")

        mostrar_confirmacion(
            self.winfo_toplevel(),
            "Eliminar cliente",
            f"¿Seguro que querés eliminar a {nombre}? Esta acción no se puede deshacer.",
            on_confirmar=eliminar,
        )

"""
ui/servicios_view.py

Vista de gestion de servicios (tabla `servicios`).
"""

import customtkinter as ctk
from ui.theme import theme
from ui.widgets.tabla import Tabla
from ui.widgets.dialogo import DialogoFormulario, mostrar_confirmacion
from ui.widgets.toast import mostrar_toast

from repositories.servicios import (
    obtener_servicios,
    crear_servicio,
    actualizar_servicio,
    eliminar_servicio,
)


def _campo(fila, clave, idx):
    if isinstance(fila, dict):
        return fila.get(clave)
    try:
        return fila[idx]
    except Exception:
        return None


def _fmt_precio(valor):
    try:
        return f"${float(valor):,.2f}"
    except Exception:
        return str(valor)


class ServiciosView(ctk.CTkFrame):
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
        theme.etiqueta(titulo_box, "Servicios", size=22, weight="bold").pack(anchor="w")
        theme.etiqueta(
            titulo_box, "Servicios disponibles para reservar.",
            size=13, color=c["texto_secundario"],
        ).pack(anchor="w", pady=(2, 0))

        theme.boton_primario(
            header, "+ Nuevo servicio", command=self._abrir_dialogo_crear, width=170,
        ).grid(row=0, column=1, sticky="e")

        tarjeta = theme.tarjeta(self)
        tarjeta.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 28))
        tarjeta.grid_columnconfigure(0, weight=1)
        tarjeta.grid_rowconfigure(0, weight=1)

        self.tabla = Tabla(
            tarjeta,
            columnas=[
                ("Servicio", 3),
                ("Duración", 2),
                ("Precio", 2),
            ],
            on_editar=self._abrir_dialogo_editar,
            on_eliminar=self._confirmar_eliminar,
        )
        self.tabla.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

    def recargar(self):
        try:
            filas = obtener_servicios()
        except Exception:
            filas = []
            mostrar_toast(self.winfo_toplevel(),
                          "No se pudo conectar con la base de datos.", tipo="peligro")

        self.tabla.cargar_filas(
            filas,
            valores_por_fila=lambda f: [
                _campo(f, "nombre_servicio", 1),
                f"{_campo(f, 'duracion_minutos', 2)} min",
                _fmt_precio(_campo(f, "precio", 3)),
            ],
        )

    # ------------------------------------------------------------------
    def _abrir_dialogo_crear(self):
        dialogo = DialogoFormulario(self.winfo_toplevel(), titulo="Nuevo servicio", alto=380)

        dialogo.agregar_campo_label("Nombre del servicio")
        entry_nombre = theme.entrada(dialogo.body, placeholder="Consulta inicial", width=340)
        entry_nombre.pack(anchor="w")

        dialogo.agregar_campo_label("Duración (minutos)")
        entry_duracion = theme.entrada(dialogo.body, placeholder="30", width=340)
        entry_duracion.pack(anchor="w")

        dialogo.agregar_campo_label("Precio")
        entry_precio = theme.entrada(dialogo.body, placeholder="15000", width=340)
        entry_precio.pack(anchor="w")

        lbl_error = theme.etiqueta(dialogo.body, "", size=12, color=theme.colors["peligro"])
        lbl_error.pack(anchor="w", pady=(10, 0))

        def confirmar():
            nombre = entry_nombre.get().strip()
            duracion = entry_duracion.get().strip()
            precio = entry_precio.get().strip()

            if not nombre or not duracion or not precio:
                lbl_error.configure(text="Completá todos los campos.")
                return

            try:
                duracion_int = int(duracion)
                precio_float = float(precio)
            except ValueError:
                lbl_error.configure(text="Duración y precio deben ser numéricos.")
                return

            try:
                crear_servicio(nombre, duracion_int, precio_float)
            except Exception:
                lbl_error.configure(text="No se pudo crear el servicio.")
                return

            dialogo.destroy()
            self.recargar()
            mostrar_toast(self.winfo_toplevel(), "Servicio creado con éxito.", tipo="exito")

        dialogo.agregar_botones("Crear servicio", confirmar)

    def _abrir_dialogo_editar(self, fila):
        id_servicio = _campo(fila, "id_servicio", 0)
        dialogo = DialogoFormulario(self.winfo_toplevel(), titulo="Editar servicio", alto=380)

        dialogo.agregar_campo_label("Nombre del servicio")
        entry_nombre = theme.entrada(dialogo.body, width=340)
        entry_nombre.insert(0, _campo(fila, "nombre_servicio", 1) or "")
        entry_nombre.pack(anchor="w")

        dialogo.agregar_campo_label("Duración (minutos)")
        entry_duracion = theme.entrada(dialogo.body, width=340)
        entry_duracion.insert(0, str(_campo(fila, "duracion_minutos", 2) or ""))
        entry_duracion.pack(anchor="w")

        dialogo.agregar_campo_label("Precio")
        entry_precio = theme.entrada(dialogo.body, width=340)
        entry_precio.insert(0, str(_campo(fila, "precio", 3) or ""))
        entry_precio.pack(anchor="w")

        lbl_error = theme.etiqueta(dialogo.body, "", size=12, color=theme.colors["peligro"])
        lbl_error.pack(anchor="w", pady=(10, 0))

        def confirmar():
            nombre = entry_nombre.get().strip()
            duracion = entry_duracion.get().strip()
            precio = entry_precio.get().strip()

            if not nombre or not duracion or not precio:
                lbl_error.configure(text="Completá todos los campos.")
                return

            try:
                duracion_int = int(duracion)
                precio_float = float(precio)
            except ValueError:
                lbl_error.configure(text="Duración y precio deben ser numéricos.")
                return

            try:
                actualizar_servicio(id_servicio, nombre, duracion_int, precio_float)
            except Exception:
                lbl_error.configure(text="No se pudo actualizar el servicio.")
                return

            dialogo.destroy()
            self.recargar()
            mostrar_toast(self.winfo_toplevel(), "Servicio actualizado.", tipo="exito")

        dialogo.agregar_botones("Guardar cambios", confirmar)

    def _confirmar_eliminar(self, fila):
        id_servicio = _campo(fila, "id_servicio", 0)
        nombre = _campo(fila, "nombre_servicio", 1)

        def eliminar():
            try:
                eliminar_servicio(id_servicio)
                self.recargar()
                mostrar_toast(self.winfo_toplevel(), "Servicio eliminado.", tipo="exito")
            except Exception:
                mostrar_toast(self.winfo_toplevel(),
                              "No se pudo eliminar (puede tener turnos asociados).",
                              tipo="peligro")

        mostrar_confirmacion(
            self.winfo_toplevel(),
            "Eliminar servicio",
            f"¿Seguro que querés eliminar '{nombre}'? Esta acción no se puede deshacer.",
            on_confirmar=eliminar,
        )

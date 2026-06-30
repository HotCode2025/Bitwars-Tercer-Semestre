"""
ui/turnos_view.py

Vista de gestion de turnos (tabla `turnos`).
Cruza datos de usuarios, proveedores y servicios para mostrar nombres
en lugar de IDs, y permite filtrar por estado.

Nota: las funciones crear_turno / actualizar_turno en
src/repositories/turnos.py reciben el parametro `id_cliente` (asi esta
escrito por el compañero del equipo), por lo que se respeta ese nombre
exacto al llamarlas desde esta vista.
"""

import customtkinter as ctk
from ui.theme import theme
from ui.widgets.tabla import Tabla
from ui.widgets.dialogo import DialogoFormulario, mostrar_confirmacion
from ui.widgets.toast import mostrar_toast

from repositories.turnos import (
    obtener_turnos,
    obtener_turnos_por_estado,
    crear_turno,
    actualizar_turno,
    actualizar_estado_turno,
    eliminar_turno,
)
from repositories.usuarios import obtener_usuarios
from repositories.proveedores import obtener_proveedores
from repositories.servicios import obtener_servicios


ESTADOS = ["PENDIENTE", "CONFIRMADO", "COMPLETADO", "CANCELADO", "NO_ASISTIO"]
ESTADO_BADGE = {
    "PENDIENTE": "advertencia",
    "CONFIRMADO": "accent",
    "COMPLETADO": "exito",
    "CANCELADO": "peligro",
    "NO_ASISTIO": "neutral",
}


def _campo(fila, clave, idx):
    if isinstance(fila, dict):
        return fila.get(clave)
    try:
        return fila[idx]
    except Exception:
        return None


class TurnosView(ctk.CTkFrame):
    """
    Orden esperado de columnas en `turnos` segun sql/schema.sql:
    0 id_turno, 1 id_usuario, 2 id_proveedor, 3 id_servicio,
    4 fecha_turno, 5 estado, 6 notas, 7 fecha_creacion
    """

    def __init__(self, parent, usuario_actual):
        c = theme.colors
        super().__init__(parent, fg_color=c["bg"], corner_radius=0)
        self.usuario_actual = usuario_actual
        self.filtro_estado = "TODOS"

        self._cargar_referencias()
        self._construir()
        self.recargar()

    def _cargar_referencias(self):
        """Cachea usuarios/proveedores/servicios para resolver nombres por ID."""
        try:
            self.mapa_usuarios = {
                _campo(u, "id_usuario", 0): _campo(u, "nombre", 1)
                for u in obtener_usuarios()
            }
        except Exception:
            self.mapa_usuarios = {}

        try:
            self.mapa_proveedores = {
                _campo(p, "id_proveedor", 0): _campo(p, "nombre", 1)
                for p in obtener_proveedores()
            }
        except Exception:
            self.mapa_proveedores = {}

        try:
            self.mapa_servicios = {
                _campo(s, "id_servicio", 0): _campo(s, "nombre_servicio", 1)
                for s in obtener_servicios()
            }
        except Exception:
            self.mapa_servicios = {}

    def _construir(self):
        c = theme.colors

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 16))
        header.grid_columnconfigure(0, weight=1)

        titulo_box = ctk.CTkFrame(header, fg_color="transparent")
        titulo_box.grid(row=0, column=0, sticky="w")
        theme.etiqueta(titulo_box, "Turnos", size=22, weight="bold").pack(anchor="w")
        theme.etiqueta(
            titulo_box, "Reservas de clientes con proveedores y servicios.",
            size=13, color=c["texto_secundario"],
        ).pack(anchor="w", pady=(2, 0))

        acciones = ctk.CTkFrame(header, fg_color="transparent")
        acciones.grid(row=0, column=1, sticky="e")

        self.combo_filtro = theme.combobox(
            acciones, values=["TODOS"] + ESTADOS, width=170,
            command=self._on_cambiar_filtro,
        )
        self.combo_filtro.set("TODOS")
        self.combo_filtro.pack(side="left", padx=(0, 10))

        theme.boton_primario(
            acciones, "+ Nuevo turno", command=self._abrir_dialogo_crear, width=150,
        ).pack(side="left")

        tarjeta = theme.tarjeta(self)
        tarjeta.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 28))
        tarjeta.grid_columnconfigure(0, weight=1)
        tarjeta.grid_rowconfigure(0, weight=1)

        self.tabla = Tabla(
            tarjeta,
            columnas=[
                ("Cliente", 2),
                ("Proveedor", 2),
                ("Servicio", 2),
                ("Fecha", 2),
                ("Estado", 1),
            ],
            on_editar=self._abrir_dialogo_editar,
            on_eliminar=self._confirmar_eliminar,
        )
        self.tabla.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

    def _on_cambiar_filtro(self, valor):
        self.filtro_estado = valor
        self.recargar()

    def recargar(self):
        self._cargar_referencias()
        try:
            if self.filtro_estado == "TODOS":
                filas = obtener_turnos()
            else:
                filas = obtener_turnos_por_estado(self.filtro_estado)
        except Exception:
            filas = []
            mostrar_toast(self.winfo_toplevel(),
                          "No se pudo conectar con la base de datos.", tipo="peligro")

        def fila_a_valores(f):
            id_usuario = _campo(f, "id_usuario", 1)
            id_proveedor = _campo(f, "id_proveedor", 2)
            id_servicio = _campo(f, "id_servicio", 3)
            fecha = _campo(f, "fecha_turno", 4)
            estado = _campo(f, "estado", 5) or "PENDIENTE"

            return [
                self.mapa_usuarios.get(id_usuario, f"#{id_usuario}") if id_usuario else "— Disponible —",
                self.mapa_proveedores.get(id_proveedor, f"#{id_proveedor}"),
                self.mapa_servicios.get(id_servicio, f"#{id_servicio}"),
                str(fecha),
                estado,
            ]

        self.tabla.cargar_filas(filas, valores_por_fila=fila_a_valores)
        self._pintar_badges_estado()

    def _pintar_badges_estado(self):
        """Reemplaza la celda de texto de estado por un badge de color, fila por fila."""
        # Recorremos las filas dibujadas y sustituimos la ultima columna visible
        # de "estado" por un badge — se hace en una segunda pasada simple buscando
        # los labels de texto que coinciden con un estado conocido.
        for row in self.tabla._filas_widgets:
            for child in row.winfo_children():
                if isinstance(child, ctk.CTkLabel):
                    texto = child.cget("text")
                    if texto in ESTADO_BADGE:
                        info = child.grid_info()
                        child.destroy()
                        badge = theme.badge(row, texto, tipo=ESTADO_BADGE[texto])
                        badge.grid(row=info.get("row", 0), column=info.get("column", 0),
                                    sticky="w", padx=12, pady=10)

    # ------------------------------------------------------------------
    def _form_comun(self, dialogo, fila=None):
        """Construye los campos compartidos entre crear/editar y devuelve los widgets."""
        nombres_usuarios = ["(Sin asignar — turno disponible)"] + list(self.mapa_usuarios.values())
        nombres_proveedores = list(self.mapa_proveedores.values()) or ["Sin proveedores"]
        nombres_servicios = list(self.mapa_servicios.values()) or ["Sin servicios"]

        dialogo.agregar_campo_label("Cliente (opcional — dejalo sin asignar para turno disponible)")
        combo_cliente = theme.combobox(dialogo.body, values=nombres_usuarios, width=340)
        combo_cliente.set(nombres_usuarios[0])
        combo_cliente.pack(anchor="w")

        dialogo.agregar_campo_label("Proveedor")
        combo_proveedor = theme.combobox(dialogo.body, values=nombres_proveedores, width=340)
        combo_proveedor.pack(anchor="w")

        dialogo.agregar_campo_label("Servicio")
        combo_servicio = theme.combobox(dialogo.body, values=nombres_servicios, width=340)
        combo_servicio.pack(anchor="w")

        dialogo.agregar_campo_label("Fecha y hora (AAAA-MM-DD HH:MM)")
        entry_fecha = theme.entrada(dialogo.body, placeholder="2026-06-25 15:30", width=340)
        entry_fecha.pack(anchor="w")

        dialogo.agregar_campo_label("Notas (opcional)")
        entry_notas = theme.entrada(dialogo.body, placeholder="Observaciones...", width=340)
        entry_notas.pack(anchor="w")

        if fila is not None:
            id_usuario_fila = _campo(fila, "id_usuario", 1)
            combo_cliente.set(
                self.mapa_usuarios.get(id_usuario_fila, nombres_usuarios[0])
                if id_usuario_fila is not None else nombres_usuarios[0]
            )
            combo_proveedor.set(self.mapa_proveedores.get(_campo(fila, "id_proveedor", 2), ""))
            combo_servicio.set(self.mapa_servicios.get(_campo(fila, "id_servicio", 3), ""))
            entry_fecha.insert(0, str(_campo(fila, "fecha_turno", 4) or ""))
            entry_notas.insert(0, _campo(fila, "notas", 6) or "")

        lbl_error = theme.etiqueta(dialogo.body, "", size=12, color=theme.colors["peligro"])
        lbl_error.pack(anchor="w", pady=(10, 0))

        return combo_cliente, combo_proveedor, combo_servicio, entry_fecha, entry_notas, lbl_error

    def _id_por_nombre(self, mapa, nombre):
        for id_, n in mapa.items():
            if n == nombre:
                return id_
        return None

    def _abrir_dialogo_crear(self):
        dialogo = DialogoFormulario(self.winfo_toplevel(), titulo="Nuevo turno", alto=560)
        combo_cliente, combo_proveedor, combo_servicio, entry_fecha, entry_notas, lbl_error = \
            self._form_comun(dialogo)

        def confirmar():
            id_cliente = self._id_por_nombre(self.mapa_usuarios, combo_cliente.get())
            id_proveedor = self._id_por_nombre(self.mapa_proveedores, combo_proveedor.get())
            id_servicio = self._id_por_nombre(self.mapa_servicios, combo_servicio.get())
            fecha = entry_fecha.get().strip()
            notas = entry_notas.get().strip() or None

            if not (id_proveedor and id_servicio and fecha):
                lbl_error.configure(text="Completá proveedor, servicio y fecha.")
                return

            try:
                crear_turno(id_cliente, id_proveedor, id_servicio, fecha, notas)
            except Exception:
                lbl_error.configure(
                    text="No se pudo crear el turno. Verificá el formato de fecha."
                )
                return

            dialogo.destroy()
            self.recargar()
            mostrar_toast(self.winfo_toplevel(), "Turno creado con éxito.", tipo="exito")

        dialogo.agregar_botones("Crear turno", confirmar)

    def _abrir_dialogo_editar(self, fila):
        id_turno = _campo(fila, "id_turno", 0)
        dialogo = DialogoFormulario(self.winfo_toplevel(), titulo="Editar turno", alto=620)
        combo_cliente, combo_proveedor, combo_servicio, entry_fecha, entry_notas, lbl_error = \
            self._form_comun(dialogo, fila=fila)

        dialogo.agregar_campo_label("Estado")
        combo_estado = theme.combobox(dialogo.body, values=ESTADOS, width=340)
        combo_estado.set(_campo(fila, "estado", 5) or "PENDIENTE")
        combo_estado.pack(anchor="w")

        def confirmar():
            id_cliente = self._id_por_nombre(self.mapa_usuarios, combo_cliente.get())
            id_proveedor = self._id_por_nombre(self.mapa_proveedores, combo_proveedor.get())
            id_servicio = self._id_por_nombre(self.mapa_servicios, combo_servicio.get())
            fecha = entry_fecha.get().strip()
            notas = entry_notas.get().strip() or None
            estado = combo_estado.get()

            if not (id_proveedor and id_servicio and fecha):
                lbl_error.configure(text="Completá proveedor, servicio y fecha.")
                return

            try:
                actualizar_turno(id_turno, id_cliente, id_proveedor, id_servicio, fecha, notas)
                actualizar_estado_turno(id_turno, estado)
            except Exception:
                lbl_error.configure(
                    text="No se pudo actualizar el turno. Verificá el formato de fecha."
                )
                return

            dialogo.destroy()
            self.recargar()
            mostrar_toast(self.winfo_toplevel(), "Turno actualizado.", tipo="exito")

        dialogo.agregar_botones("Guardar cambios", confirmar)

    def _confirmar_eliminar(self, fila):
        id_turno = _campo(fila, "id_turno", 0)

        def eliminar():
            try:
                eliminar_turno(id_turno)
                self.recargar()
                mostrar_toast(self.winfo_toplevel(), "Turno eliminado.", tipo="exito")
            except Exception:
                mostrar_toast(self.winfo_toplevel(),
                              "No se pudo eliminar (puede tener un pago asociado).",
                              tipo="peligro")

        mostrar_confirmacion(
            self.winfo_toplevel(),
            "Eliminar turno",
            "¿Seguro que querés eliminar este turno? Esta acción no se puede deshacer.",
            on_confirmar=eliminar,
        )
"""
ui/pagos_view.py

Vista de gestion de pagos (tabla `pagos`), asociados a turnos.

Orden de columnas en `pagos` segun sql/schema.sql:
0 id_pago, 1 id_turno, 2 monto, 3 metodo_pago, 4 estado,
5 fecha_pago, 6 fecha_creacion
"""

import customtkinter as ctk
from ui.theme import theme
from ui.widgets.tabla import Tabla
from ui.widgets.dialogo import DialogoFormulario, mostrar_confirmacion
from ui.widgets.toast import mostrar_toast

from repositories.pagos import (
    obtener_pagos,
    obtener_pagos_por_estado,
    crear_pago,
    actualizar_pago,
    actualizar_estado_pago,
    eliminar_pago,
)
from repositories.turnos import obtener_turnos
from repositories.usuarios import obtener_usuarios
from repositories.servicios import obtener_servicios


ESTADOS_PAGO = ["PENDIENTE", "PAGADO", "REEMBOLSADO"]
METODOS_PAGO = ["Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "Transferencia bancaria"]

ESTADO_BADGE = {
    "PENDIENTE": "advertencia",
    "PAGADO": "exito",
    "REEMBOLSADO": "neutral",
}


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


class PagosView(ctk.CTkFrame):
    def __init__(self, parent, usuario_actual):
        c = theme.colors
        super().__init__(parent, fg_color=c["bg"], corner_radius=0)
        self.usuario_actual = usuario_actual
        self.filtro_estado = "TODOS"

        self._cargar_referencias()
        self._construir()
        self.recargar()

    def _cargar_referencias(self):
        try:
            usuarios = {u["id_usuario"] if isinstance(u, dict) else u[0]:
                        (u["nombre"] if isinstance(u, dict) else u[1])
                        for u in obtener_usuarios()}
        except Exception:
            usuarios = {}
        try:
            servicios = {s["id_servicio"] if isinstance(s, dict) else s[0]:
                         (s["nombre_servicio"] if isinstance(s, dict) else s[1])
                         for s in obtener_servicios()}
        except Exception:
            servicios = {}

        self.mapa_turnos_label = {}
        self.lista_turnos_ids = []
        try:
            for t in obtener_turnos():
                id_turno = _campo(t, "id_turno", 0)
                id_usuario = _campo(t, "id_usuario", 1)
                id_servicio = _campo(t, "id_servicio", 3)
                fecha = _campo(t, "fecha_turno", 4)
                nombre_cliente = usuarios.get(id_usuario, f"#{id_usuario}")
                nombre_servicio = servicios.get(id_servicio, f"#{id_servicio}")
                label = f"#{id_turno} · {nombre_cliente} · {nombre_servicio} · {fecha}"
                self.mapa_turnos_label[id_turno] = label
                self.lista_turnos_ids.append(id_turno)
        except Exception:
            pass

    def _construir(self):
        c = theme.colors

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 16))
        header.grid_columnconfigure(0, weight=1)

        titulo_box = ctk.CTkFrame(header, fg_color="transparent")
        titulo_box.grid(row=0, column=0, sticky="w")
        theme.etiqueta(titulo_box, "Pagos", size=22, weight="bold").pack(anchor="w")
        theme.etiqueta(
            titulo_box, "Pagos asociados a los turnos reservados.",
            size=13, color=c["texto_secundario"],
        ).pack(anchor="w", pady=(2, 0))

        acciones = ctk.CTkFrame(header, fg_color="transparent")
        acciones.grid(row=0, column=1, sticky="e")

        self.combo_filtro = theme.combobox(
            acciones, values=["TODOS"] + ESTADOS_PAGO, width=170,
            command=self._on_cambiar_filtro,
        )
        self.combo_filtro.set("TODOS")
        self.combo_filtro.pack(side="left", padx=(0, 10))

        theme.boton_primario(
            acciones, "+ Nuevo pago", command=self._abrir_dialogo_crear, width=150,
        ).pack(side="left")

        tarjeta = theme.tarjeta(self)
        tarjeta.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 28))
        tarjeta.grid_columnconfigure(0, weight=1)
        tarjeta.grid_rowconfigure(0, weight=1)

        self.tabla = Tabla(
            tarjeta,
            columnas=[
                ("Turno", 3),
                ("Monto", 1),
                ("Método", 2),
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
                filas = obtener_pagos()
            else:
                filas = obtener_pagos_por_estado(self.filtro_estado)
        except Exception:
            filas = []
            mostrar_toast(self.winfo_toplevel(),
                          "No se pudo conectar con la base de datos.", tipo="peligro")

        def fila_a_valores(f):
            id_turno = _campo(f, "id_turno", 1)
            monto = _campo(f, "monto", 2)
            metodo = _campo(f, "metodo_pago", 3) or "—"
            estado = _campo(f, "estado", 4) or "PENDIENTE"
            return [
                self.mapa_turnos_label.get(id_turno, f"Turno #{id_turno}"),
                _fmt_precio(monto),
                metodo,
                estado,
            ]

        self.tabla.cargar_filas(filas, valores_por_fila=fila_a_valores)
        self._pintar_badges_estado()

    def _pintar_badges_estado(self):
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
    def _abrir_dialogo_crear(self):
        dialogo = DialogoFormulario(self.winfo_toplevel(), titulo="Nuevo pago", alto=460)

        opciones_turno = list(self.mapa_turnos_label.values()) or ["Sin turnos registrados"]

        dialogo.agregar_campo_label("Turno")
        combo_turno = theme.combobox(dialogo.body, values=opciones_turno, width=340)
        combo_turno.pack(anchor="w")

        dialogo.agregar_campo_label("Monto")
        entry_monto = theme.entrada(dialogo.body, placeholder="15000", width=340)
        entry_monto.pack(anchor="w")

        dialogo.agregar_campo_label("Método de pago")
        combo_metodo = theme.combobox(dialogo.body, values=METODOS_PAGO, width=340)
        combo_metodo.pack(anchor="w")

        lbl_error = theme.etiqueta(dialogo.body, "", size=12, color=theme.colors["peligro"])
        lbl_error.pack(anchor="w", pady=(10, 0))

        def confirmar():
            label_turno = combo_turno.get()
            id_turno = next(
                (k for k, v in self.mapa_turnos_label.items() if v == label_turno), None
            )
            monto = entry_monto.get().strip()
            metodo = combo_metodo.get()

            if not (id_turno and monto and metodo):
                lbl_error.configure(text="Completá turno, monto y método de pago.")
                return

            try:
                monto_float = float(monto)
            except ValueError:
                lbl_error.configure(text="El monto debe ser numérico.")
                return

            try:
                crear_pago(id_turno, monto_float, metodo)
            except Exception:
                lbl_error.configure(text="No se pudo registrar el pago.")
                return

            dialogo.destroy()
            self.recargar()
            mostrar_toast(self.winfo_toplevel(), "Pago registrado con éxito.", tipo="exito")

        dialogo.agregar_botones("Registrar pago", confirmar)

    def _abrir_dialogo_editar(self, fila):
        id_pago = _campo(fila, "id_pago", 0)
        dialogo = DialogoFormulario(self.winfo_toplevel(), titulo="Editar pago", alto=520)

        dialogo.agregar_campo_label("Monto")
        entry_monto = theme.entrada(dialogo.body, width=340)
        entry_monto.insert(0, str(_campo(fila, "monto", 2) or ""))
        entry_monto.pack(anchor="w")

        dialogo.agregar_campo_label("Método de pago")
        combo_metodo = theme.combobox(dialogo.body, values=METODOS_PAGO, width=340)
        combo_metodo.set(_campo(fila, "metodo_pago", 3) or METODOS_PAGO[0])
        combo_metodo.pack(anchor="w")

        dialogo.agregar_campo_label("Estado")
        combo_estado = theme.combobox(dialogo.body, values=ESTADOS_PAGO, width=340)
        combo_estado.set(_campo(fila, "estado", 4) or "PENDIENTE")
        combo_estado.pack(anchor="w")

        lbl_error = theme.etiqueta(dialogo.body, "", size=12, color=theme.colors["peligro"])
        lbl_error.pack(anchor="w", pady=(10, 0))

        def confirmar():
            monto = entry_monto.get().strip()
            metodo = combo_metodo.get()
            estado = combo_estado.get()

            try:
                monto_float = float(monto)
            except ValueError:
                lbl_error.configure(text="El monto debe ser numérico.")
                return

            try:
                actualizar_pago(id_pago, monto_float, metodo)
                actualizar_estado_pago(id_pago, estado)
            except Exception:
                lbl_error.configure(text="No se pudo actualizar el pago.")
                return

            dialogo.destroy()
            self.recargar()
            mostrar_toast(self.winfo_toplevel(), "Pago actualizado.", tipo="exito")

        dialogo.agregar_botones("Guardar cambios", confirmar)

    def _confirmar_eliminar(self, fila):
        id_pago = _campo(fila, "id_pago", 0)

        def eliminar():
            try:
                eliminar_pago(id_pago)
                self.recargar()
                mostrar_toast(self.winfo_toplevel(), "Pago eliminado.", tipo="exito")
            except Exception:
                mostrar_toast(self.winfo_toplevel(), "No se pudo eliminar el pago.",
                              tipo="peligro")

        mostrar_confirmacion(
            self.winfo_toplevel(),
            "Eliminar pago",
            "¿Seguro que querés eliminar este pago? Esta acción no se puede deshacer.",
            on_confirmar=eliminar,
        )

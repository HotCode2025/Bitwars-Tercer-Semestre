"""
ui/turnos_cliente_view.py

Vista de turnos para el rol CLIENTE.

A diferencia de TurnosView (uso exclusivo de ADMINISTRADOR), esta vista:
  - Solo muestra turnos disponibles (sin cliente asignado) para reservar.
  - Solo muestra los turnos ya reservados por el propio cliente logueado.
  - No permite editar/eliminar turnos, ni consultar la tabla de usuarios
    o pagos de otros clientes.
"""

import customtkinter as ctk
from ui.theme import theme
from ui.widgets.tabla import Tabla
from ui.widgets.dialogo import mostrar_confirmacion
from ui.widgets.toast import mostrar_toast

from repositories.turnos import (
    obtener_turnos_disponibles,
    obtener_turnos_por_cliente,
    reservar_turno,
)
from repositories.proveedores import obtener_proveedores
from repositories.servicios import obtener_servicios


def _campo(fila, clave, idx):
    if isinstance(fila, dict):
        return fila.get(clave)
    try:
        return fila[idx]
    except Exception:
        return None


class TurnosClienteView(ctk.CTkFrame):
    """
    Orden esperado de columnas en `turnos` segun sql/schema.sql:
    0 id_turno, 1 id_usuario, 2 id_proveedor, 3 id_servicio,
    4 fecha_turno, 5 estado, 6 notas, 7 fecha_creacion
    """

    def __init__(self, parent, usuario_actual):
        c = theme.colors
        super().__init__(parent, fg_color=c["bg"], corner_radius=0)
        self.usuario_actual = usuario_actual
        self.id_usuario_actual = (
            usuario_actual.get("id_usuario") if isinstance(usuario_actual, dict)
            else usuario_actual["id_usuario"]
        )

        self._cargar_referencias()
        self._construir()
        self.recargar()

    def _cargar_referencias(self):
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
        self.grid_rowconfigure(3, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 12))
        theme.etiqueta(header, "Turnos disponibles", size=20, weight="bold").pack(anchor="w")
        theme.etiqueta(
            header, "Elegí un turno disponible y reservalo.",
            size=13, color=c["texto_secundario"],
        ).pack(anchor="w", pady=(2, 0))

        tarjeta_disp = theme.tarjeta(self)
        tarjeta_disp.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 18))
        tarjeta_disp.grid_columnconfigure(0, weight=1)
        tarjeta_disp.grid_rowconfigure(0, weight=1)

        self.tabla_disponibles = Tabla(
            tarjeta_disp,
            columnas=[
                ("Proveedor", 2),
                ("Servicio", 2),
                ("Fecha", 2),
            ],
            on_editar=self._confirmar_reserva,  # boton "✎" reutilizado como "Reservar"
        )
        self.tabla_disponibles.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

        header2 = ctk.CTkFrame(self, fg_color="transparent")
        header2.grid(row=2, column=0, sticky="ew", padx=32, pady=(0, 12))
        theme.etiqueta(header2, "Mis turnos reservados", size=20, weight="bold").pack(anchor="w")

        tarjeta_mios = theme.tarjeta(self)
        tarjeta_mios.grid(row=3, column=0, sticky="nsew", padx=32, pady=(0, 28))
        tarjeta_mios.grid_columnconfigure(0, weight=1)
        tarjeta_mios.grid_rowconfigure(0, weight=1)

        self.tabla_mios = Tabla(
            tarjeta_mios,
            columnas=[
                ("Proveedor", 2),
                ("Servicio", 2),
                ("Fecha", 2),
                ("Estado", 1),
            ],
        )
        self.tabla_mios.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

    def recargar(self):
        self._cargar_referencias()

        try:
            disponibles = obtener_turnos_disponibles()
        except Exception:
            disponibles = []
            mostrar_toast(self.winfo_toplevel(),
                          "No se pudo conectar con la base de datos.", tipo="peligro")

        try:
            mios = obtener_turnos_por_cliente(self.id_usuario_actual)
        except Exception:
            mios = []

        def valores_disponible(f):
            id_proveedor = _campo(f, "id_proveedor", 2)
            id_servicio = _campo(f, "id_servicio", 3)
            fecha = _campo(f, "fecha_turno", 4)
            return [
                self.mapa_proveedores.get(id_proveedor, f"#{id_proveedor}"),
                self.mapa_servicios.get(id_servicio, f"#{id_servicio}"),
                str(fecha),
            ]

        def valores_mio(f):
            id_proveedor = _campo(f, "id_proveedor", 2)
            id_servicio = _campo(f, "id_servicio", 3)
            fecha = _campo(f, "fecha_turno", 4)
            estado = _campo(f, "estado", 5) or "PENDIENTE"
            return [
                self.mapa_proveedores.get(id_proveedor, f"#{id_proveedor}"),
                self.mapa_servicios.get(id_servicio, f"#{id_servicio}"),
                str(fecha),
                estado,
            ]

        self.tabla_disponibles.cargar_filas(disponibles, valores_por_fila=valores_disponible)
        self.tabla_mios.cargar_filas(mios, valores_por_fila=valores_mio)

    def _confirmar_reserva(self, fila):
        id_turno = _campo(fila, "id_turno", 0)

        def reservar():
            try:
                ok = reservar_turno(id_turno, self.id_usuario_actual)
            except Exception:
                ok = False

            if ok:
                mostrar_toast(self.winfo_toplevel(), "Turno reservado con éxito.", tipo="exito")
            else:
                mostrar_toast(
                    self.winfo_toplevel(),
                    "Ese turno ya no está disponible.", tipo="peligro",
                )
            self.recargar()

        mostrar_confirmacion(
            self.winfo_toplevel(),
            "Reservar turno",
            "¿Confirmás que querés reservar este turno?",
            on_confirmar=reservar,
        )
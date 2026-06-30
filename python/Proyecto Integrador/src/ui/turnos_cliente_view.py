"""
ui/turnos_cliente_view.py

Vista de turnos para el rol CLIENTE.

A diferencia de TurnosView (uso exclusivo de ADMINISTRADOR), esta vista:
  - Solo muestra turnos disponibles (sin cliente asignado) para reservar.
  - Solo muestra los turnos ya reservados por el propio cliente logueado.
  - No permite editar/eliminar turnos, ni consultar la tabla de usuarios
    o pagos de otros clientes.

Flujo de reserva:
  1. El administrador crea el turno (proveedor, servicio, fecha), sin
     cliente asignado -> queda "disponible".
  2. El cliente elige un turno disponible y pide reservarlo. Antes de
     confirmar la reserva se le muestra un dialogo de pago de prueba
     (monto = precio del servicio, metodo de pago a elegir).
  3. Solo si el "pago" se confirma, se reserva el turno (CONFIRMADO) y
     se registra el pago asociado como PAGADO.
"""

import customtkinter as ctk
from ui.theme import theme
from ui.widgets.tabla import Tabla
from ui.widgets.dialogo import DialogoFormulario
from ui.widgets.toast import mostrar_toast

from repositories.turnos import (
    obtener_turnos_disponibles,
    obtener_turnos_por_cliente,
    reservar_turno,
)
from repositories.proveedores import obtener_proveedores
from repositories.servicios import obtener_servicios
from repositories.pagos import crear_pago, obtener_pago_por_turno, actualizar_estado_pago


METODOS_PAGO = ["Tarjeta de crédito", "Tarjeta de débito", "Transferencia bancaria", "Efectivo"]


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
            servicios = obtener_servicios()
            self.mapa_servicios = {
                _campo(s, "id_servicio", 0): _campo(s, "nombre_servicio", 1)
                for s in servicios
            }
            self.mapa_servicios_precio = {
                _campo(s, "id_servicio", 0): _campo(s, "precio", 3)
                for s in servicios
            }
        except Exception:
            self.mapa_servicios = {}
            self.mapa_servicios_precio = {}

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
        id_proveedor = _campo(fila, "id_proveedor", 2)
        id_servicio = _campo(fila, "id_servicio", 3)
        fecha = _campo(fila, "fecha_turno", 4)

        nombre_proveedor = self.mapa_proveedores.get(id_proveedor, f"#{id_proveedor}")
        nombre_servicio = self.mapa_servicios.get(id_servicio, f"#{id_servicio}")
        precio = self.mapa_servicios_precio.get(id_servicio, 0) or 0

        self._abrir_dialogo_pago(id_turno, nombre_proveedor, nombre_servicio, fecha, precio)

    def _abrir_dialogo_pago(self, id_turno, nombre_proveedor, nombre_servicio, fecha, precio):
        """Pago de prueba: el cliente confirma el medio de pago y recien ahi
        se reserva el turno. No se cobra de verdad, es solo una simulacion."""
        c = theme.colors
        dialogo = DialogoFormulario(self.winfo_toplevel(), titulo="Pagar y reservar turno", alto=480)

        theme.etiqueta(
            dialogo.body, f"{nombre_servicio} con {nombre_proveedor}",
            size=14, weight="bold",
        ).pack(anchor="w", pady=(0, 2))
        theme.etiqueta(
            dialogo.body, str(fecha), size=12, color=c["texto_secundario"],
        ).pack(anchor="w", pady=(0, 12))

        dialogo.agregar_campo_label("Monto a pagar")
        entry_monto = theme.entrada(dialogo.body, width=340)
        entry_monto.insert(0, f"{float(precio):.2f}")
        entry_monto.configure(state="disabled")
        entry_monto.pack(anchor="w")

        dialogo.agregar_campo_label("Método de pago")
        combo_metodo = theme.combobox(dialogo.body, values=METODOS_PAGO, width=340)
        combo_metodo.set(METODOS_PAGO[0])
        combo_metodo.pack(anchor="w")

        theme.etiqueta(
            dialogo.body,
            "Esto es un pago de prueba: no se realiza ningún cobro real.",
            size=11, color=c["texto_secundario"],
        ).pack(anchor="w", pady=(10, 0))

        lbl_error = theme.etiqueta(dialogo.body, "", size=12, color=c["peligro"])
        lbl_error.pack(anchor="w", pady=(6, 0))

        def confirmar():
            metodo = combo_metodo.get()
            if not metodo:
                lbl_error.configure(text="Elegí un método de pago.")
                return

            try:
                reservado = reservar_turno(id_turno, self.id_usuario_actual)
            except Exception:
                reservado = False

            if not reservado:
                dialogo.destroy()
                mostrar_toast(
                    self.winfo_toplevel(),
                    "Ese turno ya no está disponible.", tipo="peligro",
                )
                self.recargar()
                return

            try:
                crear_pago(id_turno, float(precio), metodo)
                pago = obtener_pago_por_turno(id_turno)
                id_pago = _campo(pago, "id_pago", 0) if pago is not None else None
                if id_pago is not None:
                    actualizar_estado_pago(id_pago, "PAGADO")
            except Exception:
                # El turno ya quedo reservado aunque el registro de pago falle;
                # se avisa igual para que el cliente sepa que el turno es suyo.
                mostrar_toast(
                    self.winfo_toplevel(),
                    "Turno reservado, pero no se pudo registrar el pago.",
                    tipo="advertencia",
                )
                dialogo.destroy()
                self.recargar()
                return

            dialogo.destroy()
            mostrar_toast(self.winfo_toplevel(), "Pago confirmado y turno reservado.", tipo="exito")
            self.recargar()

        dialogo.agregar_botones("Pagar y reservar", confirmar, tipo_confirmar="exito")
"""
widgets/tabla.py

Tabla simple basada en CTkScrollableFrame: encabezado fijo + filas con
hover y botones de accion (editar / eliminar) a la derecha.

No depende de Treeview (que no sigue el theming de customtkinter), por
lo que se ve consistente con el resto de la app y mantiene el estilo
de bordes finos redondeados en cada fila.
"""

import customtkinter as ctk
from ui.theme import theme


class Tabla(ctk.CTkFrame):
    """
    columnas: lista de tuplas (titulo, ancho_relativo_weight)
    on_editar / on_eliminar: callbacks que reciben la fila completa (dict)
    """

    def __init__(self, parent, columnas, on_editar=None, on_eliminar=None,
                 alto=420, **kwargs):
        c = theme.colors
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.columnas = columnas
        self.on_editar = on_editar
        self.on_eliminar = on_eliminar
        self._filas_widgets = []

        # --- encabezado ---
        self.header = ctk.CTkFrame(
            self, fg_color=c["bg_terciario"], corner_radius=10,
            height=40,
        )
        self.header.pack(fill="x", padx=2, pady=(0, 6))
        self.header.grid_propagate(False)

        for i, (titulo, weight) in enumerate(columnas):
            self.header.grid_columnconfigure(i, weight=weight)
            lbl = theme.etiqueta(self.header, titulo, size=12, weight="bold",
                                  color=c["texto_secundario"], anchor="w")
            lbl.grid(row=0, column=i, sticky="ew", padx=12, pady=8)

        if on_editar or on_eliminar:
            self.header.grid_columnconfigure(len(columnas), weight=0, minsize=96)

        # --- cuerpo con scroll ---
        self.body = theme.scrollable_frame(self, height=alto)
        self.body.pack(fill="both", expand=True, padx=2)
        for i, (_, weight) in enumerate(columnas):
            self.body.grid_columnconfigure(i, weight=weight)
        if on_editar or on_eliminar:
            self.body.grid_columnconfigure(len(columnas), weight=0, minsize=96)

        self._vacio_label = None

    def limpiar(self):
        for w in self._filas_widgets:
            w.destroy()
        self._filas_widgets = []
        if self._vacio_label:
            self._vacio_label.destroy()
            self._vacio_label = None

    def mostrar_vacio(self, mensaje="No hay registros para mostrar."):
        self.limpiar()
        c = theme.colors
        self._vacio_label = theme.etiqueta(
            self.body, mensaje, size=13, color=c["texto_secundario"]
        )
        self._vacio_label.grid(row=0, column=0, columnspan=len(self.columnas) + 1,
                                pady=40)

    def cargar_filas(self, filas, valores_por_fila):
        """
        filas: lista de objetos/dicts identificadores (uno por registro)
        valores_por_fila: funcion(fila) -> lista de strings, una por columna
        """
        self.limpiar()
        c = theme.colors

        if not filas:
            self.mostrar_vacio()
            return

        for idx, fila in enumerate(filas):
            valores = valores_por_fila(fila)
            row_frame = ctk.CTkFrame(
                self.body,
                fg_color=c["bg_secundario"] if idx % 2 == 0 else c["bg"],
                corner_radius=10,
                height=46,
            )
            row_frame.grid(row=idx, column=0, columnspan=len(self.columnas) + 1,
                            sticky="ew", pady=2)
            for i, (_, weight) in enumerate(self.columnas):
                row_frame.grid_columnconfigure(i, weight=weight)
            if self.on_editar or self.on_eliminar:
                row_frame.grid_columnconfigure(len(self.columnas), weight=0, minsize=96)

            for i, valor in enumerate(valores):
                lbl = theme.etiqueta(row_frame, str(valor), size=13, anchor="w")
                lbl.grid(row=0, column=i, sticky="ew", padx=12, pady=10)

            acciones = ctk.CTkFrame(row_frame, fg_color="transparent")
            acciones.grid(row=0, column=len(self.columnas), sticky="e", padx=8)

            if self.on_editar:
                btn_edit = theme.boton_icono(
                    acciones, "✎",
                    command=lambda f=fila: self.on_editar(f),
                )
                btn_edit.pack(side="left", padx=2)

            if self.on_eliminar:
                btn_del = theme.boton_icono(
                    acciones, "🗑",
                    command=lambda f=fila: self.on_eliminar(f),
                )
                btn_del.pack(side="left", padx=2)

            self._filas_widgets.append(row_frame)

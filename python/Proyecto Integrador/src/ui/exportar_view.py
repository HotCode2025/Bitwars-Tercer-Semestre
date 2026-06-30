"""
ui/exportar_view.py
 
Vista exclusiva para el rol ADMINISTRADOR: permite exportar las tablas
turnos, usuarios y pagos a archivos CSV (carpeta data/exports/).
"""
 
import customtkinter as ctk
from ui.theme import theme
from ui.widgets.toast import mostrar_toast
 
from import_export.csv_exporter import exportar_tabla_csv, exportar_todas
 
 
class ExportarView(ctk.CTkFrame):
    def __init__(self, parent, usuario_actual):
        c = theme.colors
        super().__init__(parent, fg_color=c["bg"], corner_radius=0)
        self.usuario_actual = usuario_actual
 
        self.grid_columnconfigure(0, weight=1)
 
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 16))
        theme.etiqueta(header, "Exportar datos", size=22, weight="bold").pack(anchor="w")
        theme.etiqueta(
            header, "Generá archivos CSV de las tablas del sistema.",
            size=13, color=c["texto_secundario"],
        ).pack(anchor="w", pady=(2, 0))
 
        tarjeta = theme.tarjeta(self)
        tarjeta.grid(row=1, column=0, sticky="ew", padx=32, pady=(0, 28))
 
        cuerpo = ctk.CTkFrame(tarjeta, fg_color="transparent")
        cuerpo.pack(fill="x", padx=24, pady=24)
 
        theme.etiqueta(
            cuerpo, "Los archivos se guardan en la carpeta data/exports/.",
            size=12, color=c["texto_secundario"],
        ).pack(anchor="w", pady=(0, 16))
 
        fila_botones = ctk.CTkFrame(cuerpo, fg_color="transparent")
        fila_botones.pack(anchor="w")
 
        theme.boton_secundario(
            fila_botones, "Exportar usuarios", width=200,
            command=lambda: self._exportar("usuarios"),
        ).pack(side="left", padx=(0, 10))
 
        theme.boton_secundario(
            fila_botones, "Exportar turnos", width=200,
            command=lambda: self._exportar("turnos"),
        ).pack(side="left", padx=(0, 10))
 
        theme.boton_secundario(
            fila_botones, "Exportar pagos", width=200,
            command=lambda: self._exportar("pagos"),
        ).pack(side="left", padx=(0, 10))
 
        theme.boton_primario(
            cuerpo, "Exportar todo (usuarios + turnos + pagos)", width=320,
            command=self._exportar_todo,
        ).pack(anchor="w", pady=(16, 0))
 
        self.lbl_estado = theme.etiqueta(cuerpo, "", size=12, color=c["texto_secundario"])
        self.lbl_estado.pack(anchor="w", pady=(14, 0))
 
    def _exportar(self, tabla):
        try:
            archivo = exportar_tabla_csv(tabla)
            self.lbl_estado.configure(text=f"Generado: {archivo}")
            mostrar_toast(self.winfo_toplevel(), f"{tabla}.csv exportado con éxito.", tipo="exito")
        except Exception as exc:
            self.lbl_estado.configure(text=f"Error al exportar {tabla}: {exc}")
            mostrar_toast(self.winfo_toplevel(), f"No se pudo exportar {tabla}.", tipo="peligro")
 
    def _exportar_todo(self):
        try:
            archivos = exportar_todas()
            self.lbl_estado.configure(
                text="Generados: " + ", ".join(str(a) for a in archivos)
            )
            mostrar_toast(self.winfo_toplevel(), "Exportación completa.", tipo="exito")
        except Exception as exc:
            self.lbl_estado.configure(text=f"Error al exportar: {exc}")
            mostrar_toast(self.winfo_toplevel(), "No se pudo completar la exportación.",
                          tipo="peligro")
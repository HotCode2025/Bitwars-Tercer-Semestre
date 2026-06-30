"""
import_export/csv_exporter.py

Exportacion de tablas a CSV para el rol ADMINISTRADOR.

Usa la misma conexion centralizada de config/database.py (en vez de
credenciales hardcodeadas y una conexion via polars/adbc aparte, como
estaba antes) para mantener un solo punto de configuracion de la base
de datos.
"""

import csv
from pathlib import Path
from config.database import obtener_conexion

TABLAS_EXPORTABLES = ["usuarios", "turnos", "pagos"]
CARPETA_EXPORTS = Path(__file__).resolve().parent.parent.parent / "data" / "exports"


def exportar_tabla_csv(tabla, carpeta=None):
    """
    Exporta el contenido completo de una tabla a un archivo CSV.
    `tabla` debe ser una de TABLAS_EXPORTABLES.

    Devuelve el Path del archivo generado.
    """

    if tabla not in TABLAS_EXPORTABLES:
        raise ValueError(f"Tabla no exportable: {tabla}")

    destino = Path(carpeta) if carpeta else CARPETA_EXPORTS
    destino.mkdir(parents=True, exist_ok=True)
    archivo = destino / f"{tabla}.csv"

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {tabla}")
            filas = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]

    with open(archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columnas)
        writer.writerows(filas)

    return archivo


def exportar_todas(carpeta=None):
    """Exporta usuarios, turnos y pagos. Devuelve una lista de Paths generados."""

    return [exportar_tabla_csv(tabla, carpeta=carpeta) for tabla in TABLAS_EXPORTABLES]
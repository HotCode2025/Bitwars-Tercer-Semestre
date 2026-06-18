import logging
from pathlib import Path

def configurar_logger():
    """
    Configura el logger principal de la aplicación.
    """

    Path("logs").mkdir(exist_ok=True) # Crear la carpeta "logs" si no existe

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(
                "logs/app.log", # Archivo donde se guardarán los logs de la aplicación
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )


def obtener_logger(nombre):
    """
    Devuelve una instancia del logger.
    """

    return logging.getLogger(nombre)
"""
main.py

Punto de entrada de la aplicacion. Configura el logger, inicializa el
sistema de theming y lanza la pantalla de login.

Ejecutar desde la carpeta src/:
    python main.py
"""

from config.logger import configurar_logger
from ui.login_view import iniciar


if __name__ == "__main__":
    configurar_logger()
    iniciar()

"""
crear_admin.py

Script de un solo uso para crear (o resetear) la cuenta de administrador
"maestra" del sistema, con credenciales fijas y simples para entrar rapido,
similar al login Admin/Admin de un router casero.

Uso:
    cd src
    python crear_admin.py

Credenciales que va a dejar listas:
    Usuario (campo Email del login):  Admin
    Contraseña:                       Admin

Nota: esta cuenta se crea saltando las validaciones normales de
contraseña de la app (que exigen 8+ caracteres, mayuscula y simbolo),
porque es un acceso tecnico/interno, no una cuenta de cliente real.
No se modifica auth.py ni la logica de registro normal de la app.
"""

import sys
sys.path.insert(0, ".")

from auth import hashear_password
from repositories.usuarios import (
    obtener_usuario_por_email,
    crear_usuario,
    actualizar_password,
    actualizar_rol,
)

USUARIO_ADMIN = "Admin"
PASSWORD_ADMIN = "Admin"


def asegurar_admin():
    """
    Si la cuenta "Admin" no existe, la crea como ADMIN.
    Si ya existe, le resetea la contraseña y se asegura de que sea ADMIN.
    """

    password_hash = hashear_password(PASSWORD_ADMIN)

    existente = obtener_usuario_por_email(USUARIO_ADMIN)

    if existente is None:
        crear_usuario(
            "Administrador",
            None,
            USUARIO_ADMIN,
            password_hash,
            "ADMIN"
        )
        print(f"Cuenta admin creada: usuario='{USUARIO_ADMIN}' password='{PASSWORD_ADMIN}'")
        return

    actualizar_password(existente["id_usuario"], password_hash)
    actualizar_rol(existente["id_usuario"], "ADMIN")
    print(f"Cuenta admin ya existia, contraseña y rol actualizados: usuario='{USUARIO_ADMIN}' password='{PASSWORD_ADMIN}'")


if __name__ == "__main__":
    asegurar_admin()

import bcrypt

from repositories.usuarios import (
    obtener_usuario_por_email,
    crear_usuario
)


def hashear_password(password):
    """
    Generar un hash seguro a partir de una contraseña.
    """

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verificar_password(password, password_hash):
    """
    Verificar si una contraseña coincide con su hash almacenado.
    """

    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode()
    )


def validar_password(password):
    return len(password >= 8)


def autenticar_usuario(email, password):
    """
    Autenticar un usuario mediante email y contraseña.
    """

    usuario = obtener_usuario_por_email(email)

    if usuario is None:
        return None

    password_hash = usuario["password_hash"]

    if verificar_password(password, password_hash):
        return usuario

    return None


def registrar_usuario(
        nombre,
        telefono,
        email,
        password,
        rol='CLIENTE'):
    """
    Registrar un nuevo usuario almacenando su contraseña hasheada.
    """

    password_hash = hashear_password(password) # Hashear contraseña

    crear_usuario(
        nombre,
        telefono,
        email,
        password_hash, # Guarda la contraseña hasheada
        rol
    )
import bcrypt

from repositories.usuarios import (
    obtener_usuario_por_email,
    crear_usuario
)

def validar_password(password):
    """
    Validar que la contraseña tenga al menos 8 caracteres,
    una mayúscula y un carácter especial.
    """

    tiene_longitud = len(password) >= 8
    tiene_mayuscula = any(caracter.isupper() for caracter in password)
    tiene_especial = any(not caracter.isalnum() for caracter in password)

    return (
        tiene_longitud
        and tiene_mayuscula
        and tiene_especial
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

    if not validar_password(password):
        raise ValueError(
            "La contraseña debe tener al menos 8 caracteres, una mayúscula y un carácter especial."
        )

    password_hash = hashear_password(password)

    crear_usuario(
        nombre,
        telefono,
        email,
        password_hash,
        rol
    )
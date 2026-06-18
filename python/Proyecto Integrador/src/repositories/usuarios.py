from config.database import obtener_conexion
from psycopg2.extras import RealDictCursor

def obtener_usuarios():

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM usuarios
                ORDER BY nombre
                """
            )

            return cursor.fetchall()


def obtener_usuario_por_id(id_usuario):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM usuarios
                WHERE id_usuario = %s
                """,
                (id_usuario,)
            )

            return cursor.fetchone()


def obtener_usuario_por_email(email):

    with obtener_conexion() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:

            cursor.execute(
                """
                SELECT *
                FROM usuarios
                WHERE email = %s
                """,
                (email,)
            )

            return cursor.fetchone()


def crear_usuario(
    nombre,
    telefono,
    email,
    password_hash,
    rol="CLIENTE"
):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO usuarios
                (
                    nombre,
                    telefono,
                    email,
                    password_hash,
                    rol
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    nombre,
                    telefono,
                    email,
                    password_hash,
                    rol
                )
            )


def actualizar_usuario(
    id_usuario,
    nombre,
    telefono,
    email
):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE usuarios
                SET
                    nombre = %s,
                    telefono = %s,
                    email = %s
                WHERE id_usuario = %s
                """,
                (
                    nombre,
                    telefono,
                    email,
                    id_usuario
                )
            )


def actualizar_password(
    id_usuario,
    password_hash
):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE usuarios
                SET
                    password_hash = %s
                WHERE id_usuario = %s
                """,
                (
                    password_hash,
                    id_usuario
                )
            )


def actualizar_rol(
    id_usuario,
    rol
):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE usuarios
                SET
                    rol = %s
                WHERE id_usuario = %s
                """,
                (
                    rol,
                    id_usuario
                )
            )


def eliminar_usuario(id_usuario):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM usuarios
                WHERE id_usuario = %s
                """,
                (id_usuario,)
            )
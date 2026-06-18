from config.database import obtener_conexion


# ---- Crear proveedor ----
def crear_proveedor(
        nombre,
        telefono,
        email):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO proveedores
                (
                    nombre,
                    telefono,
                    email
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    nombre,
                    telefono,
                    email
                )
            )


# ---- Actualizar proveedor ----
def actualizar_proveedor(
        id_proveedor,
        nombre,
        telefono,
        email):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE proveedores
                SET
                    nombre = %s,
                    telefono = %s,
                    email = %s
                WHERE id_proveedor = %s
                """,
                (
                    nombre,
                    telefono,
                    email,
                    id_proveedor
                )
            )


# ---- Obtener proveedores ----
def obtener_proveedores():

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM proveedores
                ORDER BY nombre
                """
            )

            return cursor.fetchall()


# ---- Obtener proveedor por ID ----
def obtener_proveedor_por_id(id_proveedor):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM proveedores
                WHERE id_proveedor = %s
                """,
                (id_proveedor,)
            )

            return cursor.fetchone()


# ---- Eliminar proveedor ----
def eliminar_proveedor(id_proveedor):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM proveedores
                WHERE id_proveedor = %s
                """,
                (id_proveedor,)
            )
from config.database import obtener_conexion


# ---- Crear servicio ----
def crear_servicio(
        nombre_servicio,
        duracion_minutos,
        precio):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO servicios
                (
                    nombre_servicio,
                    duracion_minutos,
                    precio
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    nombre_servicio,
                    duracion_minutos,
                    precio
                )
            )


# ---- Actualizar servicio ----
def actualizar_servicio(
        id_servicio,
        nombre_servicio,
        duracion_minutos,
        precio):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE servicios
                SET
                    nombre_servicio = %s,
                    duracion_minutos = %s,
                    precio = %s
                WHERE id_servicio = %s
                """,
                (
                    nombre_servicio,
                    duracion_minutos,
                    precio,
                    id_servicio
                )
            )


# ---- Obtener servicios ----
def obtener_servicios():

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM servicios
                ORDER BY nombre_servicio
                """
            )

            return cursor.fetchall()


# ---- Obtener servicio por ID ----
def obtener_servicio_por_id(id_servicio):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM servicios
                WHERE id_servicio = %s
                """,
                (id_servicio,)
            )

            return cursor.fetchone()


# ---- Eliminar servicio ----
def eliminar_servicio(id_servicio):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM servicios
                WHERE id_servicio = %s
                """,
                (id_servicio,)
            )
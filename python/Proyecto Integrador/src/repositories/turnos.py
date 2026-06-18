from config.database import obtener_conexion


# ---- Crear turno ----
def crear_turno(
        id_cliente,
        id_proveedor,
        id_servicio,
        fecha_turno,
        notas=None):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO turnos
                (
                    id_cliente,
                    id_proveedor,
                    id_servicio,
                    fecha_turno,
                    notas
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
                    id_cliente,
                    id_proveedor,
                    id_servicio,
                    fecha_turno,
                    notas
                )
            )


# ---- Actualizar turno ----
def actualizar_turno(
        id_turno,
        id_cliente,
        id_proveedor,
        id_servicio,
        fecha_turno,
        notas):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE turnos
                SET
                    id_cliente = %s,
                    id_proveedor = %s,
                    id_servicio = %s,
                    fecha_turno = %s,
                    notas = %s
                WHERE id_turno = %s
                """,
                (
                    id_cliente,
                    id_proveedor,
                    id_servicio,
                    fecha_turno,
                    notas,
                    id_turno
                )
            )


# ---- Obtener turnos ----
def obtener_turnos():

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM turnos
                ORDER BY fecha_turno
                """
            )

            return cursor.fetchall()


# ---- Obtener turno por ID ----
def obtener_turno_por_id(id_turno):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM turnos
                WHERE id_turno = %s
                """,
                (id_turno,)
            )

            return cursor.fetchone()


# ---- Obtener turnos por cliente ----
def obtener_turnos_por_cliente(id_cliente):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM turnos
                WHERE id_cliente = %s
                ORDER BY fecha_turno
                """,
                (id_cliente,)
            )

            return cursor.fetchall()


# ---- Obtener turnos por proveedor ----
def obtener_turnos_por_proveedor(id_proveedor):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM turnos
                WHERE id_proveedor = %s
                ORDER BY fecha_turno
                """,
                (id_proveedor,)
            )

            return cursor.fetchall()


# ---- Obtener turnos por estado ----
def obtener_turnos_por_estado(estado):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM turnos
                WHERE estado = %s
                ORDER BY fecha_turno
                """,
                (estado,)
            )

            return cursor.fetchall()


# ---- Actualizar estado ----
def actualizar_estado_turno(
        id_turno,
        estado):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE turnos
                SET
                    estado = %s
                WHERE id_turno = %s
                """,
                (
                    estado,
                    id_turno
                )
            )


# ---- Eliminar turno ----
def eliminar_turno(id_turno):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM turnos
                WHERE id_turno = %s
                """,
                (id_turno,)
            )
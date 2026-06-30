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
                    id_usuario,
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
                    id_usuario = %s,
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


# ---- Obtener turnos disponibles (sin cliente asignado, usados por rol CLIENTE) ----
def obtener_turnos_disponibles():

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM turnos
                WHERE estado = 'PENDIENTE'
                AND id_usuario IS NULL
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
                WHERE id_usuario = %s
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


# ---- Reservar turno (usado por rol CLIENTE) ----
def reservar_turno(id_turno, id_usuario):
    """
    Asigna un turno PENDIENTE (disponible, sin cliente asignado) al
    cliente que lo reserva, y lo pasa a estado CONFIRMADO.
    Solo afecta turnos que sigan disponibles (evita reservas duplicadas
    por carrera entre dos clientes).
    """

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE turnos
                SET
                    id_usuario = %s,
                    estado = 'CONFIRMADO'
                WHERE id_turno = %s
                AND estado = 'PENDIENTE'
                AND id_usuario IS NULL
                """,
                (
                    id_usuario,
                    id_turno
                )
            )

            return cursor.rowcount > 0


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
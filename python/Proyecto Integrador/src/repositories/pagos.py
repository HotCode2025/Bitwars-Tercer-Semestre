from config.database import obtener_conexion

def crear_pago(
        id_turno,
        monto,
        metodo_pago):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO pagos
                (
                    id_turno,
                    monto,
                    metodo_pago
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    id_turno,
                    monto,
                    metodo_pago
                )
            )


def eliminar_pago(id_pago):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM pagos
                WHERE id_pago = %s
                """,
                (id_pago,)
            )



def actualizar_pago(
        id_pago,
        monto,
        metodo_pago):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE pagos
                SET
                    monto = %s,
                    metodo_pago = %s
                WHERE id_pago = %s
                """,
                (
                    monto,
                    metodo_pago,
                    id_pago
                )
            )


def obtener_pagos():
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM pagos
                ORDER BY fecha_pago
                """
            )

            return cursor.fetchall()

def obtener_pago_por_id(id_pago):
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM pagos
                WHERE id_pago = %s
                """,
                (id_pago,)
            )

            return cursor.fetchone()

def obtener_pago_por_turno(id_turno):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM pagos
                WHERE id_turno = %s
                """,
                (id_turno,)
            )

            return cursor.fetchone()


# ---- Obtener pagos por estado ----
def obtener_pagos_por_estado(estado):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT *
                FROM pagos
                WHERE estado = %s
                ORDER BY fecha_pago
                """,
                (estado,)
            )

            return cursor.fetchall()


# ---- Actualizar estado ----
def actualizar_estado_pago(
        id_pago,
        estado):

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE pagos
                SET
                    estado = %s
                WHERE id_pago = %s
                """,
                (
                    estado,
                    id_pago
                )
            )
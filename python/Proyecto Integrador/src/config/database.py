import os
import psycopg2

def obtener_conexion():
    """
    Crea y devuelve una conexion a PostgreSQL.
    """

    try:
        conexion = psycopg2.connect(
            host="localhost",
            port="5433",
            database="sistema_turnos",
            user="postgres",
            password="elefantito"
        )

        return conexion

    except psycopg2.Error as error:
        raise ConnectionError(
            f"No fue posible conectar con PostgreSQL: {error}"
        )
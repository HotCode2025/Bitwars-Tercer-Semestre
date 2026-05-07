import psycopg2

conn = psycopg2.connect(
    user="postgres",
    password="admin",
    host="localhost",
    port="5433"
)

try:
    with conn:
        with conn.cursor() as cursor:
            query = """
            SELECT
                *
            FROM
                persona
            WHERE
                id_persona = %s
            """
            id_persona = input("Ingrese el id de la persona: ")
            cursor.execute(sentencia, (id_persona,))
            registros = cursor.fetchone()
            print(registros)

except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    conn.close()
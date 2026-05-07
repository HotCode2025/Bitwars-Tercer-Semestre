import psycopg2

conn = psycopg2.connect(
    user="postgres",
    password="admin",
    host="localhost",
    port="5433"
)

try:
    id_persona = int(input("Ingrese el ID de la persona a borrar: "))

    with conn:
        with conn.cursor() as cursor:
            query = "DELETE FROM persona WHERE id_persona=%s"
            valores = (id_persona,)

            cursor.execute(query, valores)

            registros_borrados = cursor.rowcount
            print(f"{registros_borrados} registros borrados")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    conn.close()
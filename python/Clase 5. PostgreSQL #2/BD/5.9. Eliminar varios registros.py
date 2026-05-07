import psycopg2

conn = psycopg2.connect(
    user="postgres",
    password="admin",
    host="localhost",
    port="5433"
)

try:
    ids = input(
        "Ingrese los IDs a borrar separados por coma: "
    )

    # "1,5,8" -> [(1,), (5,), (8,)]
    valores = [(int(id.strip()),) for id in ids.split(",")]

    with conn:
        with conn.cursor() as cursor:
            query = "DELETE FROM persona WHERE id_persona=%s"

            cursor.executemany(query, valores)

            registros_borrados = cursor.rowcount

            print(f"{registros_borrados} registros borrados")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    conn.close()
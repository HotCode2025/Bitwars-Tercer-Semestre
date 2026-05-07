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
            query = "UPDATE persona SET nombre=%s, apellido=%s, email=%s WHERE id_persona=%s"
            valores = [
                ('Juan Carlos', 'Roldan', 'rcarlos@gmail.com', 1)
            ]

            cursor.execute(query, valores)

            registros_actualizados = cursor.rowcount
            print(f"{registros_actualizados} registros actualizados")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    conn.close()
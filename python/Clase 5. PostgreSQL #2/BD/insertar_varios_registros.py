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
            INSERT INTO persona(nombre, apellido, email)
            VALUES (%s, %s, %s)
            """

            valores = [
                ('Carlos', 'Lara', 'carloslara@gmail.com'),
                ('Marcos', 'Canto', 'mcanto@gmail.com'),
                ('Marcelo', 'Cuenca', 'mcuenca@gmail.com')
            ]

            cursor.executemany(query, valores)

            registros_insertados = cursor.rowcount
            print(f"{registros_insertados} registros insertados")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    conn.close()
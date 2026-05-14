import psycopg2

conn = psycopg2.connect(
    user="postgres",
    password="admin",
    host="localhost",
    port="5433"
)

conn.autocommit = False

try:
    cursor = conn.cursor()

    query = "INSERT INTO persona(nombre, apellido, email) VALUES (%s, %s, %s)"
    values = [(
        "Carlos", "Lara", "c_lara@gmail.com"
    )]

    query = "UPDATE persona SET nombre =%s, apellido=%s, email=%s WHERE id_persona=%s"
    values = [
        ('Juan', 'Juarez', 'jjuarez@gmail.com', 1)
    ]
    
    cursor.execute(query, values)
    conn.commit() # Hacemos el commit manual
    
except Exception as e:
    conn.rollback() # Se deshace la acción
    print(f"Ocurrió un error, se hizo un rollback: {e}")
finally:
    conn.close()
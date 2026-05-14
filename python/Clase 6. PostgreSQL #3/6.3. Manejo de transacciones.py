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
    query = "INSERT INTO persona(nombre, apellido, email) VALUES(%s, %s, %s)"
    values = [
        ('Maria', 'Esparza', 'mesparza@gmail.com')
    ]
    
    cursor.execute(query, values)
    
except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    conn.close()
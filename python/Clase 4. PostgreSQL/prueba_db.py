import psycopg2

USER = 'postgres'
PASSWORD = 'elefantito' # admin
HOST = 'localhost'
PORT = '5433' # 5432
DATABASE = 'test_db'

# Conectar a Postgres
conn = psycopg2.connect(
    user = USER,
    password = PASSWORD,
    host = HOST,
    port = PORT,
    database = DATABASE
)

cursor = conn.cursor() # Crear cursor

query = "SELECT * FROM persona"
cursor.execute(query) # Ejecutar query
rows = cursor.fetchall()

print(rows)

cursor.close() # Cerrar cursor
conn.close() # Cerrar conexión
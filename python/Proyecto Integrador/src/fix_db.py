"""
fix_db.py

Script de arreglo unico: permite que la tabla `turnos` acepte turnos
sin cliente asignado (turnos "disponibles" creados por el admin, que
el cliente reserva despues).

Como correrlo:
    cd src
    python fix_db.py

Se puede correr una sola vez. Si lo corres de nuevo y ya estaba
arreglado, no rompe nada (Postgres simplemente no hace cambios).
"""

from config.database import obtener_conexion


def main():
    print("Conectando a la base de datos...")
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            print("Permitiendo turnos sin cliente asignado (id_usuario nullable)...")
            cursor.execute(
                "ALTER TABLE turnos ALTER COLUMN id_usuario DROP NOT NULL;"
            )
    print("¡Listo! Ya podés crear turnos disponibles sin cliente asignado.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        input("Presioná Enter para cerrar...")

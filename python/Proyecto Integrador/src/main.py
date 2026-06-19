from auth import registrar_usuario, autenticar_usuario
from menu_cliente import menu_cliente

def main():

    while True:

        print("\n=== Sistema de Turnos ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("> ")

        if opcion == "1":
            print("\n--- Registro ---")

            nombre = input("Nombre: ")
            telefono = input("Teléfono: ")
            email = input("Email: ")
            password = input("Contraseña: ")

            try:
                registrar_usuario(
                    nombre=nombre,
                    telefono=telefono,
                    email=email,
                    password=password
                )

                print("\nUsuario registrado correctamente.")

            except Exception as e:

                print(f"\nError: {e}")

        elif opcion == "2":
            print("\n--- Iniciar Sesión ---")

            email = input("Email: ")
            password = input("Contraseña: ")

            usuario = autenticar_usuario(
                email,
                password
            )

            if usuario:
                print("\nLogin exitoso")
                print(f"Bienvenido {usuario['nombre']}")

                menu_cliente(usuario)

            else:
                print("\nCredenciales incorrectas.")

        elif opcion == "3":
            print("\nHasta luego.")
            break

        else:
            print("\nOpción inválida.")


if __name__ == "__main__":
    main()
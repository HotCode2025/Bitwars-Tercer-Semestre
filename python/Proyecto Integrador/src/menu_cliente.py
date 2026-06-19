def menu_cliente(usuario):

    while True:

        print("\n=== Menú Cliente ===")
        print("1. Reservar turno")
        print("2. Ver mis turnos")
        print("3. Cancelar turno")
        print("4. Editar mi perfil")
        print("5. Ver mis pagos")
        print("6. Cerrar sesión")

        opcion = input("> ")

        if opcion == "1":
            reservar_turno(usuario)

        elif opcion == "2":
            ver_mis_turnos(usuario)

        elif opcion == "3":
            cancelar_turno(usuario)

        elif opcion == "4":
            editar_perfil(usuario)

        elif opcion == "5":
            ver_mis_pagos(usuario)

        elif opcion == "6":
            print("\nSesión cerrada.")
            break

        else:
            print("Opción inválida.")
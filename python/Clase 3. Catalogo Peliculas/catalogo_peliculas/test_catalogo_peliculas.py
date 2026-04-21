import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from dominio.pelicula import Pelicula
from servicio.catalogo_peliculas import CatalogoPeliculas


def mostrar_menu():
    print("\n1) Agregar pelicula")
    print("2) Listar peliculas")
    print("3) Eliminar archivo de peliculas")
    print("4) Salir")


def main():
    while True:
        mostrar_menu()
        opcion = input("Ingrese una opcion: ")

        if opcion == "1":
            nombre = input("Nombre de la pelicula: ")
            pelicula = Pelicula(nombre)
            CatalogoPeliculas.agregar_pelicula(pelicula)

        elif opcion == "2":
            CatalogoPeliculas.listar_peliculas()

        elif opcion == "3":
            CatalogoPeliculas.eliminar()

        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opcion no valida")


main()

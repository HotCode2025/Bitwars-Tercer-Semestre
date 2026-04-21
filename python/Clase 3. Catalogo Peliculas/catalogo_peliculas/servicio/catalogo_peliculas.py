import os
from dominio.pelicula import Pelicula


class CatalogoPeliculas:

    ruta_archivo = "peliculas.txt"

    @staticmethod
    def agregar_pelicula(pelicula):
        archivo = open(CatalogoPeliculas.ruta_archivo, "a")
        archivo.write(str(pelicula) + "\n")
        archivo.close()
        print("Pelicula agregada:", pelicula)

    @staticmethod
    def listar_peliculas():
        try:
            archivo = open(CatalogoPeliculas.ruta_archivo, "r")
            peliculas = archivo.readlines()
            archivo.close()

            if len(peliculas) == 0:
                print("No hay peliculas guardadas.")
                return

            print("\n--- Lista de peliculas ---")
            for i in range(len(peliculas)):
                print(str(i + 1) + ". " + peliculas[i].strip())
            print("--------------------------")

        except FileNotFoundError:
            print("No hay peliculas guardadas.")

    @staticmethod
    def eliminar():
        try:
            os.remove(CatalogoPeliculas.ruta_archivo)
            print("Archivo eliminado.")
        except FileNotFoundError:
            print("No habia archivo para eliminar.")

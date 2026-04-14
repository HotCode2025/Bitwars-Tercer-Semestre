from ManejoArchivos import ManejoArchivos

with open('prueba.txt', 'r', encoding='utf8') as archivo: # with: abre y cierra el archivo
    print(archivo.read())

with ManejoArchivos('prueba.txt') as archivo:
    print(archivo.read())
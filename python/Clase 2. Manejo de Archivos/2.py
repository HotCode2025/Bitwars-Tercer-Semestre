# Write crea el archivo si es que no existe
archivo = open('prueba.txt', 'w') # W: Write - Escribir
archivo.write("Este es un mensaje de prueba.\n") # Escribir un mensaje en el archivo prueba.txt
archivo.write("Esto va en la segunda línea")
# \n = Salto de línea
archivo.close()
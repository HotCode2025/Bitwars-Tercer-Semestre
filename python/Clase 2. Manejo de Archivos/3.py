# Write crea el archivo si es que no existe
archivo = open('prueba.txt', 'w', encoding="utf8") # utf8 Encoding
archivo.write("Este es un mensaje de prueba.\n") 
archivo.write("Esto va en la segunda línea") # Reconoce acentos y se elimina el error (�)
# \n = Salto de línea
archivo.close()
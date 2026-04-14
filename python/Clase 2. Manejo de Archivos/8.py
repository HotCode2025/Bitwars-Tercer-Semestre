archivo = open('archivos/prueba.txt', 'r', encoding='utf8')

for line in archivo: # Iterar línea por línea
    print(archivo.readline()) # Acceder al archivo como una lista
    # print(archivo.readline([1])) # Leer línea específica

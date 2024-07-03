def leer_textos(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        textos = [linea.strip().upper() for linea in archivo]
    return textos

def escribir_resultado(nombre_archivo_salida, texto, distancia_maxima):
    with open(nombre_archivo_salida, 'w') as archivo:
        archivo.write(f'{texto}\n')
        archivo.write(f'{distancia_maxima}\n')

import random
from collections import Counter

def letras_unicas(textos):
    """
    Toma una lista de textos y devuelve un conjunto con todas las letras únicas presentes en ellos.
    """
    letras = set()
    for texto in textos:
        letras.update(texto)
    return letras

def construir_solucion_inicial(textos):
    longitud_texto = len(textos[0])
    texto_inicial = []

    for i in range(longitud_texto):
        caracteres = [texto[i] for texto in textos]
        contador = Counter(caracteres)
        
        # Creamos una lista de candidatos basada en la frecuencia
        candidatos = [caracter for caracter, _ in contador.items()]
        
        # Seleccionamos un caracter aleatorio de la lista de candidatos
        caracter_seleccionado = random.choice(candidatos)
        texto_inicial.append(caracter_seleccionado)
    
    return ''.join(texto_inicial)

def distancia(a, b):
    """
    Calcula la distancia entre dos cadenas de caracteres del mismo largo
    """
    change = 0
    n = len(a)

    for i in range(1, n + 1):
        if a[i - 1] != b[i - 1]:
            change += 1
    
    return change

def generar_vecinos(texto):
    vecinos = set()
    longitud_texto = len(texto)
    letras = set(texto.upper())
    
    for i in range(longitud_texto):
        for letra in letras:
            if texto[i].upper() != letra.upper():
                vecino = texto[:i] + letra + texto[i+1:]
                vecinos .add(vecino)
    
    return vecinos

def busqueda_local(texto_inicial, textos, mejor_distancia_maxima_global, vecinos_recorridos, letras):
    texto_actual = texto_inicial
    mejor_texto = texto_actual
    mejor_distancia_maxima = mejor_distancia_maxima_global
    print("2.mejor_distancia_maxima: ", mejor_distancia_maxima)
    
    while True:
        vecinos = generar_vecinos(texto_actual, letras)
        vecinosARecorrer = vecinos - vecinos_recorridos
        mejor_vecino = None
        
        for vecino in vecinosARecorrer:
            distancias = [distancia(vecino, texto) for texto in textos]
            distancia_maxima = max(distancias)
        
            if distancia_maxima < mejor_distancia_maxima:
                print("3.mejor_vecino: ", vecino, distancia_maxima)
                mejor_distancia_maxima = distancia_maxima
                mejor_vecino = vecino

        vecinos_recorridos.update(vecinosARecorrer)
        
        if mejor_vecino is None:
            # No hay mejor vecino, se alcanza un optimo local
            break
        
        texto_actual = mejor_vecino
        mejor_texto = mejor_vecino
    
    return mejor_texto, mejor_distancia_maxima, vecinos_recorridos

def grasp(textos, max_iter=100):
    mejor_texto_global = None
    mejor_distancia_maxima_global = float('inf')
    vecinos_recorridos = set()
    counter = 0
    letras = letras_unicas(textos)
    
    for _ in range(max_iter):
        texto_inicial = construir_solucion_inicial(textos)
        texto_mejorado, distancia_maxima, vecinos = busqueda_local(texto_inicial, textos, mejor_texto_global, mejor_distancia_maxima_global, vecinos_recorridos, letras)
        
        if distancia_maxima < mejor_distancia_maxima_global:
            mejor_distancia_maxima_global = distancia_maxima
            mejor_texto_global = texto_mejorado
            counter = 0
        else:
            # Vamos acumulando la cantidad de iteraciones en las cuales la distancia no mejora
            counter += 1

        vecinos_recorridos.update(vecinos)

        # Si la cantidad de iteraciones en las cuales la distancia no mejora es 1000, salimos de las iteraciones
        if counter > 999:
            break
    
    return mejor_texto_global, mejor_distancia_maxima_global

def main(nombre_archivo_entrada, nombre_archivo_salida, max_iter=100):
    textos = leer_textos(nombre_archivo_entrada)
    mejor_texto, mejor_distancia_maxima = grasp(textos, max_iter)
    escribir_resultado(nombre_archivo_salida, mejor_texto, mejor_distancia_maxima)

# Ejemplo de uso
nombre_archivo_entrada = 'textos_entrada.txt'
nombre_archivo_salida = 'resultado_salida.txt'
main(nombre_archivo_entrada, nombre_archivo_salida, max_iter=100)

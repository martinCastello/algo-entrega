def leer_textos(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        textos = [linea.strip().upper() for linea in archivo]
    return textos

def distancia(a, b):
    change = 0
    n = len(a)

    for i in range(1, n + 1):
        if a[i - 1] != b[i - 1]:
            change += 1
    
    return change

import time
import random
from collections import Counter
import matplotlib.pyplot as plt

def construir_solucion_random_inicial(textos):
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

def letras_unicas(textos):
    """
    Toma una lista de textos y devuelve un conjunto con todas las letras únicas presentes en ellos.
    """
    letras = set()
    for texto in textos:
        letras.update(texto)
    return letras

def generar_vecinos(texto, letras):
    vecinos = set()
    longitud_texto = len(texto)
    
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
    scoring_por_iteracion = []
    vecinos_recorridos = set()
    start_time = time.time()
    counter = 0
    letras = letras_unicas(textos)

    for i in range(max_iter):
        texto_inicial = construir_solucion_random_inicial(textos)
        texto_mejorado, distancia_maxima, vecinos = busqueda_local(texto_inicial, textos, mejor_distancia_maxima_global, vecinos_recorridos, letras)
        
        if distancia_maxima < mejor_distancia_maxima_global:
            mejor_distancia_maxima_global = distancia_maxima
            mejor_texto_global = texto_mejorado
            counter = 0
        else:
            # Vamos acumulando la cantidad de iteraciones en las cuales la distancia no mejora
            counter += 1
        
        vecinos_recorridos.update(vecinos)
    
        scoring_por_iteracion.append(mejor_distancia_maxima_global)

        # Si la cantidad de iteraciones en las cuales la distancia no mejora es 1000, salimos de las iteraciones
        if counter > 999:
            break

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo de ejecución grasp: {elapsed_time} segundos")

    return mejor_texto_global, mejor_distancia_maxima_global, scoring_por_iteracion


def ejecutar_grasp_variadas(instancias, max_iter=100):
    resultados = {}
    start_time = time.time()
    for nombre_instancia in instancias:
        textos = leer_textos(nombre_instancia)
        _, _, scoring_por_iteracion = grasp(textos, max_iter)
        resultados[nombre_instancia] = scoring_por_iteracion
        print("scoring instancia: ", nombre_instancia, scoring_por_iteracion)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo de ejecución grasp_variadas: {elapsed_time} segundos")

    return resultados

instancias = ['texto_mas_parecido_10_300_1.txt', 'texto_mas_parecido_10_500_2.txt', 'texto_mas_parecido_10_700_3.txt']
resultados = ejecutar_grasp_variadas(instancias, max_iter=3000)

def graficar_resultados(resultados):
    plt.figure(figsize=(12, 8))
    for nombre_instancia, scoring in resultados.items():
        plt.plot(range(len(scoring)), scoring, label=nombre_instancia)
    
    plt.xlabel('Iteraciones')
    plt.ylabel('Scoring (Distancia Máxima)')
    plt.title('Scoring vs Iteraciones para Distintas Instancias')
    plt.legend()
    plt.grid(True)
    plt.show()

# Graficar los resultados
graficar_resultados(resultados)


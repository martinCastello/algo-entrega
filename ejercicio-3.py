import random
from collections import Counter

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


def generar_texto_random(textos):
    """
    Genera un texto aleatorio basado en los textos de entrada.
    
    :param textos: Lista de textos de igual longitud.
    :return: Texto aleatorio generado.
    """
    longitud_texto = len(textos[0])  # Asumimos que todos los textos tienen la misma longitud
    texto_resultado = []
    
    #print("random: ", textos)

    for i in range(longitud_texto):
        caracteres = [texto[i] for texto in textos]
        caracter_aleatorio = random.choice(caracteres)
        texto_resultado.append(caracter_aleatorio)
    
    return ''.join(texto_resultado)


def generar_texto_inicial(textos):
    """
    Genera un texto inicial basado en los caracteres más frecuentes en cada posición.
    """
    longitud_texto = len(textos[0])
    texto_inicial = []
    
    for i in range(longitud_texto):
        caracteres = [texto[i] for texto in textos if i < len(texto)]
        contador = Counter(caracteres)
        caracter_mas_frecuente = contador.most_common(1)[0][0]
        texto_inicial.append(caracter_mas_frecuente)
    
    return ''.join(texto_inicial)

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

def texto_mas_equilibrado_busqueda_local(textos, max_iter=1000):
    texto_actual = generar_texto_inicial(textos)
    mejor_texto = texto_actual
    mejor_distancia_maxima = float('inf')
    vecinos_recorridos = set()
    
    for _ in range(max_iter):
        vecinos = generar_vecinos(texto_actual)
        vecinosARecorrer = vecinos - vecinos_recorridos
        mejor_vecino = None
        
        for vecino in vecinosARecorrer:
            distancias = [distancia(vecino, texto) for texto in textos]
            distancia_maxima = max(distancias)
            
            if distancia_maxima < mejor_distancia_maxima:
                print("vecino: ", vecino, distancia_maxima)
                mejor_distancia_maxima = distancia_maxima
                mejor_vecino = vecino
        
        vecinos_recorridos.update(vecinosARecorrer)
        
        if mejor_vecino is None:
            print("No hay mejor vecino, se alcanza un optimo local")
            break

        texto_actual = mejor_vecino
        mejor_texto = mejor_vecino
    
    return mejor_texto

# Ejemplo de uso
#textos = ["ABBAC", "BBAAC", "CBAAB", "ABCAA", "ACCCC", "BCACB"]
textos = ["ABBACBB", "BBAACBD", "CBAABDB"]
#textos = ["ABBACBB", "BBAACBD", "CBAABDB", "ABCAAAA", "ACCCCCC", "BCACBCB"]
#textos = ["ABBACHAEF", "BBAACHACD", "CBAHABAAA", "AHBCAAFFF", "ACHCCCCCC", "BCACBHEEE", "AAACBEEEH"]
texto_generado = texto_mas_equilibrado_busqueda_local(textos)
print(f'El texto mas parecido generado es: "{texto_generado}".')
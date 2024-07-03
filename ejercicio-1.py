
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

def texto_mas_equilibrado(textos):
    # Inicializar el texto resultado
    texto_resultado = []
    
    # La longitud de los textos es igual, así que tomamos la longitud del primer texto
    longitud_texto = len(textos[0])
    
    # Iterar sobre cada posición en los textos
    for i in range(longitud_texto):
        # Contar la frecuencia de cada carácter en la posición i
        contador = Counter(texto[i] for texto in textos)

        # Evaluar el impacto de cada carácter en la posición i
        mejor_caracter = None
        menor_distancia_maxima = float('inf')
        
        for caracter in contador:

            for texto in textos:

                # Generar un texto candidato con el caracter en la posición i
                texto_candidato = texto_resultado + [caracter] + [texto[j] for j in range(i + 1, longitud_texto)]

                # Calcular la distancia para cada texto con el texto candidato
                distancias = [distancia(texto_candidato, texto) for texto in textos]

                distancia_maxima = max(distancias)
            
                if distancia_maxima < menor_distancia_maxima:
                    menor_distancia_maxima = distancia_maxima
                    mejor_caracter = caracter
            
        # Añadir el carácter seleccionado al texto resultado
        texto_resultado.append(mejor_caracter)
    
    # Unir la lista de caracteres en un solo texto
    texto_resultado = ''.join(texto_resultado)
    
    return texto_resultado

# Ejemplo de uso
#textos = ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE"] # Ejemplo donde demuestra que el greedy no es optimo
textos = ["ABBAC", "BBAAC", "CBAAB", "ABCAA", "ACCCC", "BCACB"]
texto_generado = texto_mas_equilibrado(textos)
print(f'El texto mas parecido generado es: "{texto_generado}".')

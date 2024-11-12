from collections import deque  # Importamos esto para crear colas
import heapq  # Importamos heapq para manejar colas 

# Representación del grafo con distancias entre localidades
localidades = {
    "Madrid": [("Alcorcón", 13), ("Villaviciosa de Odón", 22), ("Alcalá de Henares", 35)],
    "Villanueva de la Cañada": [("Villaviciosa de Odón", 11), ("Boadilla del Monte", 7)],
    "Alcorcón": [("Madrid", 13), ("Móstoles", 5)],
    "Móstoles": [("Alcorcón", 5), ("Fuenlabrada", 8)],
    "Fuenlabrada": [("Móstoles", 8), ("Getafe", 10)],
    "Getafe": [("Fuenlabrada", 10), ("Madrid", 16)],
    "Villaviciosa de Odón": [("Madrid", 22), ("Villanueva de la Cañada", 11)],
    "Boadilla del Monte": [("Villanueva de la Cañada", 7), ("Madrid", 15)],
    "Alcalá de Henares": [("Madrid", 35), ("Torrejón de Ardoz", 15)],
    "Torrejón de Ardoz": [("Alcalá de Henares", 15), ("Madrid", 20)],
}

# 1. Función para encontrar la ruta más corta entre dos localidades usando Dijkstra

# Utilizo Dijkstra porque encuentra la ruta más corta en grafos con pesos positivos

def ruta_mas_corta(grafo, inicio, destino):
    distancias = {nodo: float('inf') for nodo in grafo}  # Inicializamos todas las distancias como infinitas
    distancias[inicio] = 0
    predecesores = {inicio: None}  # Para reconstruir el camino, guardamos los predecesores
    cola_prioridad = [(0, inicio)]  # Iniciamos la cola de prioridad con el nodo de inicio

    while cola_prioridad:  
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)  # Extraemos el nodo con menor distancia

        if nodo_actual == destino:  # Si hemos llegado al destino, reconstruimos la ruta
            ruta = []
            while nodo_actual:
                ruta.append(nodo_actual)  # Añadimos cada nodo de la ruta
                nodo_actual = predecesores[nodo_actual]  # Seguimos al predecesor hasta llegar al inicio
            return ruta[::-1], distancias[destino]  # Devolvemos la ruta en orden y la distancia total

        for vecino, peso in grafo[nodo_actual]:  # Exploramos los vecinos del nodo actual
            nueva_distancia = distancia_actual + peso  # Calculamos la nueva distancia
            if nueva_distancia < distancias[vecino]:  # Si es menor, actualizamos la distancia
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = nodo_actual  # Guardamos el predecesor para la ruta
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))  # Añadimos el vecino a la cola

    return None, float('inf')  # Si no encontramos el destino, pues infinito

# Ejemplo de uso del primer método, buscamos de Madrid a Boadilla del Monte
ruta, distancia = ruta_mas_corta(localidades, "Madrid", "Boadilla del Monte")
print("Ruta más corta:", ruta)  
print("Distancia total:", distancia)  

# 2. Función para identificar localidades con conexiones menores a una distancia máxima

def localidades_con_conexiones_cortas(grafo, max_distancia=15):  # Fijamos la distancia máxima a 15 km
    resultado = []
    for localidad, conexiones in grafo.items():  # Revisamos cada localidad
        if all(distancia < max_distancia for _, distancia in conexiones):  # Si todas sus conexiones son menores a 15
            resultado.append(localidad)  # Añadimos la localidad a la lista de resultado
    return resultado 

# Llamamos a la función
localidades_cortas = localidades_con_conexiones_cortas(localidades)
print("Localidades con conexiones menores de 15 km:", localidades_cortas)

# 3. Función para verificar si el grafo es conexo (todas las localidades están conectadas)

def es_conexo(grafo):
    visitados = set()  # Conjunto para llevar un registro de las localidades visitadas

    def dfs(nodo):  # Definimos una función de DFS (búsqueda en profundidad)
        visitados.add(nodo)  # Marcamos el nodo como visitado
        for vecino, _ in grafo[nodo]:  # Revisamos cada vecino del nodo
            if vecino not in visitados:  # Si el vecino no ha sido visitado
                dfs(vecino)  # Llamamos a DFS en el vecino

    nodo_inicial = list(grafo.keys())[0]  # Tomamos cualquier nodo como punto de inicio
    dfs(nodo_inicial)  # Iniciamos DFS desde el nodo inicial
    return len(visitados) == len(grafo)  # Comprobamos si visitamos todas las localidades

# Llamada a la función
conexo = es_conexo(localidades)
print("El grafo es conexo:", conexo)

# 4. Función para encontrar todas las rutas alternativas sin ciclos entre dos localidades

def rutas_alternativas(grafo, inicio, destino):
    rutas = []
    cola = deque([(inicio, [inicio])])  # Usamos una cola con el nodo inicial y la ruta inicial

    while cola:
        nodo_actual, ruta = cola.popleft()  # Extraemos el nodo actual y la ruta hasta él
        if nodo_actual == destino:  # Si llegamos al destino, guardamos la ruta
            rutas.append(ruta)
        else:
            for vecino, _ in grafo[nodo_actual]:  # Revisamos los vecinos del nodo actual
                if vecino not in ruta:  # Si el vecino no está en la ruta actual (para evitar ciclos)
                    cola.append((vecino, ruta + [vecino]))  # Añadimos el vecino y la ruta extendida a la cola

    return rutas 

# Ejemplo de uso, de Madrid a Getafe
rutas = rutas_alternativas(localidades, "Madrid", "Getafe")
print("Rutas alternativas sin ciclos:", rutas)

# 5. Función para encontrar la ruta más larga sin ciclos entre dos localidades

def ruta_mas_larga_sin_ciclos(grafo, inicio, destino):
    def dfs(nodo, ruta, distancia):  # Definimos DFS para explorar todas las rutas posibles
        if nodo == destino:  # Si llegamos al destino, guardamos la ruta y la distancia
            rutas.append((ruta[:], distancia))
            return
        for vecino, peso in grafo[nodo]:  # Revisamos los vecinos del nodo actual
            if vecino not in ruta:  # Solo visitamos nodos no visitados en esta ruta
                ruta.append(vecino)  # Añadimos el vecino a la ruta actual
                dfs(vecino, ruta, distancia + peso)  # Llamamos a DFS en el vecino con distancia actualizada
                ruta.pop()  # Quitamos el nodo después de explorar para volver al estado anterior

    rutas = []
    dfs(inicio, [inicio], 0)  # Iniciamos DFS desde el nodo inicial con distancia 0
    if rutas:
        return max(rutas, key=lambda x: x[1])  # Seleccionamos la ruta con mayor distancia
    return None, 0  # Si no hay rutas, devolvemos None y distancia 0

# Probamos de nuevo de Madrid a Getafe
ruta_larga, distancia_larga = ruta_mas_larga_sin_ciclos(localidades, "Madrid", "Getafe")
print("Ruta más larga:", ruta_larga)
print("Distancia de la ruta más larga:", distancia_larga)
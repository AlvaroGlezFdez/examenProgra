from Comunidad_Madrid import ruta_mas_corta, localidades_con_conexiones_cortas, es_conexo, rutas_alternativas,localidades
from memory_profiler import profile
import timeit

# Definimos las pruebas para cada metodo

@profile
def prueba_ruta_mas_corta():
    ruta, distancia = ruta_mas_corta(localidades, "Madrid", "Boadilla del Monte")
    print("Ruta más corta:", ruta)
    print("Distancia total:", distancia)

@profile
def prueba_localidades_con_conexiones_cortas():
    localidades_cortas = localidades_con_conexiones_cortas(localidades)
    print("Localidades con conexiones menores de 15 km:", localidades_cortas)

@profile
def prueba_es_conexo():
    conexo = es_conexo(localidades)
    print("El grafo es conexo:", conexo)

@profile
def prueba_rutas_alternativas():
    rutas = rutas_alternativas(localidades, "Madrid", "Getafe")
    print("Rutas alternativas sin ciclos:", rutas)

# Medimos el tiempo de ejecución con timeit para cada función y lo ponemos con 6 decimales porque sino me salen 0.0 y es imposible
tiempo_ruta_mas_corta = timeit.timeit('prueba_ruta_mas_corta()', globals=globals(), number=1)
print(f"Tiempo de ejecución para ruta_mas_corta: {tiempo_ruta_mas_corta / 10:.6f} segundos en promedio")

tiempo_localidades_cortas = timeit.timeit('prueba_localidades_con_conexiones_cortas()', globals=globals(), number=1)
print(f"Tiempo de ejecución para localidades_con_conexiones_cortas: {tiempo_localidades_cortas / 10:.6f} segundos en promedio")

tiempo_es_conexo = timeit.timeit('prueba_es_conexo()', globals=globals(), number=1)
print(f"Tiempo de ejecución para es_conexo: {tiempo_es_conexo / 10:.6f} segundos en promedio")

tiempo_rutas_alternativas = timeit.timeit('prueba_rutas_alternativas()', globals=globals(), number=1)
print(f"Tiempo de ejecución para rutas_alternativas: {tiempo_rutas_alternativas / 10:.6f} segundos en promedio")
"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
from tabulate import tabulate
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
default_limit = 1000 
sys.setrecursionlimit(default_limit*10)
import time

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def newController(list_type):
    return controller.newController(list_type)

def printMenu():
    print("Bienvenido")
    print("0- Implementar ordenamientos de contenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar las películas estrenadas en un periodo de tiempo")
    print("3- Listar programas de televisión agregados en un periodo de tiempo")
    print("4- Encontrar contenido donde participa un actor")
    print("5- Encontrar contenido por un género especifico")
    print("6- Encontrar contenido producido en un país")
    print("7- Encontrar contenido con un director involucrado")
    print("8- Listar el TOP (N) de los géneros con más contenido")
    print("9- Listar el TOP (N) de los actores con más participaciones en contenido")
    print("10- Salir")

def loadData(control, tamaño, orden):
    return controller.loadData(control, tamaño, orden)

def printStreamingInfo(n_videos, s1, s2, s3, s4):
    print("Loaded streaming service info:")
    print("Total loaded files: " + str(n_videos) + "\n")
    table = [["Service name", "Count"], ["Amazon", s1], ["Disney", s2], ["Hulu", s3], ["Netflix", s4]]
    print(tabulate(table, tablefmt="grid", colalign=("left",)), "\n")

def printSortResults(delta_time, n_videos, sorted_list, sample):
    d_time = f"{delta_time:.3f}"
    print("Para", n_videos, "elementos, delta tiempo:", str(d_time))
    print("\nLos", sample, "primeros y los últimos", sample, "videos ordenados son:")
    table = [["Show ID", "Stream service", "Type", "Release year", "Title", "Director", "Cast", "Country", "Date added", "Rating", "Duration", "Listed in", "Description"]]
    i = 1 
    while i <= sample: 
        video = lt.getElement(sorted_list, i) 
        table.append([video["show_id"], video["stream_service"], video["type"], video["release_year"], video["title"], video["director"], video["cast"], video["country"], video["date_added"], video["rating"], video["duration"], video["listed_in"], video["description"]])
        i += 1
    i = n_videos - sample + 1
    while i <= n_videos: 
        video = lt.getElement(sorted_list, i) 
        table.append([video["show_id"], video["stream_service"], video["type"], video["release_year"], video["title"], video["director"], video["cast"], video["country"], video["date_added"], video["rating"], video["duration"], video["listed_in"], video["description"]])
        i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[10,18,10,15,10,10,15,10,10,10,10,18,30]), "\n")

def printReq1(a_inicial, a_final, total_peliculas, list_peliculas, sample):
    print("\nHay", total_peliculas, "películas estrenadas entre", a_inicial, "y", a_final)
    print("\nLos", sample, "primeros y los últimos", sample, "videos ordenados son:")
    table = [["Release year", "Title", "Duration", "Stream service", "Director", "Cast"]]
    i = 1 
    while i <= sample: 
        video = lt.getElement(list_peliculas, i) 
        table.append([video["release_year"], video["title"], video["duration"], video["stream_service"], video["director"], video["cast"]])  
        i += 1
    i = total_peliculas - sample + 1
    while i <= total_peliculas: 
        video = lt.getElement(list_peliculas, i) 
        table.append([video["release_year"], video["title"], video["duration"], video["stream_service"], video["director"], video["cast"]])  
        i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[15,10,10,18,10,25]), "\n")

def printReq2(f_inicial, f_final, total_TV, list_TV, sample):
    print("\nHay", total_TV, "shows de TV estrenados entre", f_inicial, "y", f_final)
    print("\nLos", sample, "primeros y los últimos", sample, "videos ordenados son:")
    table = [["Date added", "Title", "Duration", "Release year", "Stream service", "Director", "Cast"]]
    i = 1 
    while i <= sample: 
        video = lt.getElement(list_TV, i) 
        table.append([video["date_added"], video["title"], video["duration"], video["release_year"], video["stream_service"], video["director"], video["cast"]])  
        i += 1
    i = total_TV - sample + 1
    while i <= total_TV: 
        video = lt.getElement(list_TV, i) 
        table.append([video["date_added"], video["title"], video["duration"], video["release_year"], video["stream_service"], video["director"], video["cast"]])  
        i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[10,10,10,15,18,10,25]), "\n")

def printReq3(actor, total_peliculas, total_TV, list_actor, sample):
    total = total_peliculas + total_TV
    print("\nConteo de contenidos donde participó", actor)
    print(tabulate([["Type", "Count"], ["Películas", total_peliculas], ["TV Shows", total_TV]], tablefmt="grid", colalign=("left",)))
    table = [["Type", "Title", "Release year", "Director", "Stream service", "Duration", "Cast", "Country", "Listed in", "Description"]]
    if total <= sample*2 and total > 0:
        print("\nLos", total, "videos ordenados son:")
        for video in lt.iterator(list_actor):
            table.append([video["type"], video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
    elif total > 0:
        print("\nLos", sample, "primeros y los últimos", sample, "videos ordenados son:")
        i = 1 
        while i <= sample: 
            video = lt.getElement(list_actor, i) 
            table.append([video["type"], video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
        i = total - sample + 1
        while i <= total: 
            video = lt.getElement(list_actor, i) 
            table.append([video["type"], video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[10,10,15,10,18,10,25,10,18,30]), "\n")
        
def printReq4(genero, total_peliculas, total_TV, list_genero, sample):
    total = total_peliculas + total_TV
    print(tabulate([["Conteo de contenidos", genero], ["Películas", total_peliculas], ["TV Shows", total_TV]], tablefmt="grid", colalign=("left",)))
    table = [["Type", "Title", "Release year", "Director", "Stream service", "Duration", "Cast", "Country", "Listed in", "Description"]]
    if total <= sample*2 and total > 0:
        print("\nLos", total, "videos ordenados son:")
        for video in lt.iterator(list_genero):
            table.append([video["type"], video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
    elif total > 0:
        print("\nLos", sample, "primeros y los últimos", sample, "videos ordenados son:")
        i = 1 
        while i <= sample: 
            video = lt.getElement(list_genero, i) 
            table.append([video["type"], video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
        i = total - sample + 1
        while i <= total: 
            video = lt.getElement(list_genero, i) 
            table.append([video["type"], video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[10,10,15,10,18,10,25,10,18,30]), "\n")

def printReq5(pais, total_peliculas, total_TV, list_pais, sample):
    total = total_peliculas + total_TV
    print("\nHay", total, "contenidos producidos en", pais)
    print(tabulate([["Type", "Count"], ["Películas", total_peliculas], ["TV Shows", total_TV]], tablefmt="grid", colalign=("left",)))
    table = [["Title", "Release year", "Director", "Stream service", "Duration", "Cast", "Country", "Listed in", "Description"]]
    if total <= sample*2 and total > 0:
        print("\nLos", total, "videos ordenados son:")
        for video in lt.iterator(list_pais):
            table.append([video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
    elif total > 0:
        print("\nLos", sample, "primeros videos ordenados son:") 
        i = 1 
        while i <= sample: 
            video = lt.getElement(list_pais, i) 
            table.append([video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
        print("\nLos", sample, "últimos videos ordenados son:") 
        i = total - sample + 1
        while i <= total: 
            video = lt.getElement(list_pais, i) 
            table.append([video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[10,15,10,18,10,25,10,18,30]), "\n")

def printReq6(director, total_peliculas, total_TV, generos, conteo, dic_servicio, list_director, sample):
    total = total_peliculas + total_TV
    print("\nEn total hay", total, "contenidos de", director)
    print(tabulate([["Type", "Count"], ["Películas", total_peliculas], ["TV Shows", total_TV]], tablefmt="grid", colalign=("left",)), "\n")
    print(tabulate([["Service name", "Count"], ["Amazon Prime", dic_servicio["amazon_prime"]], ["Disney Plus", dic_servicio["disney_plus"]], ["Hulu", dic_servicio["hulu"]], ["Netflix", dic_servicio["netflix"]]], tablefmt="grid", colalign=("left",)), "\n")
    print(tabulate({"Genero":generos["elements"], "Conteo":conteo["elements"]}, headers="keys", tablefmt="grid", colalign=("left",)))
    table = [["Title", "Release year", "Director", "Stream service", "Duration", "Cast", "Country", "Listed in", "Description"]]
    if total <= sample*2 and total > 0:
        print("\nLos", total, "videos ordenados son:")
        for video in lt.iterator(list_director):
            table.append([video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
    elif total > 0:
        print("\nLos", sample, "primeros videos ordenados son:") 
        i = 1 
        while i <= sample: 
            video = lt.getElement(list_director, i) 
            table.append([video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
        print("\nLos", sample, "últimos videos ordenados son:") 
        i = total - sample + 1
        while i <= total: 
            video = lt.getElement(list_director, i) 
            table.append([video["title"], video["release_year"], video["director"], video["stream_service"], video["duration"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[10,15,10,18,10,25,10,18,30]), "\n")

def printReq7(top, top_generos):
    print("\nEn total hay", lt.size(top_generos), "géneros\nEn el top", top, "están:")
    table = [["Género", "Total", "Películas", "TV Shows", "Amazon Prime", "Disney Plus", "Hulu", "Netflix"]]
    i = 1 
    while i <= top: 
        genero = lt.getElement(top_generos, i) 
        table.append([genero["nombre"], genero["total"], genero["Movie"], genero["TV Show"], genero["amazon_prime"], genero["disney_plus"], genero["hulu"], genero["netflix"]])
        i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[25,15,15,15,15,15,15,15]), "\n")

def printReq8(top):
    print("\n")

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()

def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

catalog, control = None, newController("ARRAY_LIST")
lista, tamaño, orden, ord = "Array List", "small", "mg", "Merge"

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0:2]) == 0:
        opcion1 = input("Seleccione un tipo de lista:\n1- ARRAY_LIST o 2- SINGLE_LINKED\n")
        if int(opcion1[0]) == 1:
            control = newController("ARRAY_LIST")
            lista = "Array List"
        elif int(opcion1[0]) == 2:
            control = newController("SINGLE_LINKED")
            lista = "Single Linked"

        opcion2 = input("\nElija un tamaño de muestra: \n1- small \n2- 5pct \n3- 10pct \n4- 20pct \n5- 30pct \n6- 50pct \n7- 80pct \n8- large\n")
        if int(opcion2[0]) == 1:
            tamaño = "small"
        elif int(opcion2[0]) == 2:
            tamaño = "5pct"
        elif int(opcion2[0]) == 3:
            tamaño = "10pct"
        elif int(opcion2[0]) == 4:
            tamaño = "20pct"
        elif int(opcion2[0]) == 5:
            tamaño = "30pct"
        elif int(opcion2[0]) == 6:
            tamaño = "50pct"
        elif int(opcion2[0]) == 7:
            tamaño = "80pct"
        elif int(opcion2[0]) == 8:
            tamaño = "large"
        
        opcion3 = input("\nSeleccione un tipo de ordenamiento:\n1- Insertion, 2- Selection, 3- Shell, 4- Quicksort, 5- Merge\n")
        if int(opcion3[0]) == 1:
            orden = "ie"
            ord = "Insertion"
        elif int(opcion3[0]) == 2:
            orden = "se"
            ord = "Selection"
        elif int(opcion3[0]) == 3:
            orden = "sa"
            ord = "Shell"
        elif int(opcion3[0]) == 4:
            orden = "qck"
            ord = "Quicksort"
        elif int(opcion3[0]) == 5:
            orden = "mg"
            ord = "Merge"
        
        print("Ha configurado su catálogo como", lista, "de", tamaño, "con", ord, "\n")

    elif int(inputs[0:2]) == 1:
        print("Cargando información de los archivos ....")
        import tracemalloc
        tracemalloc.start()
        start_memory = getMemory()
        sorted_list, delta_time, n_videos, s1, s2, s3, s4 = loadData(control, tamaño, orden)
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        printStreamingInfo(n_videos, s1, s2, s3, s4)
        printSortResults(delta_time, n_videos, sorted_list, 3)
        print(f"{delta_memory:.3f}")

    elif int(inputs[0:2]) == 2:
        a_inicial = int(input("\nIndique el año de inicio: "))
        a_final = int(input("Indique el año final del periodo: "))
        t2i= time.time()
        total_peliculas, list_peliculas = controller.listarPeliculasPeriodo(control, a_inicial, a_final)
        t2f=time.time()
        printReq1(a_inicial, a_final, total_peliculas, list_peliculas, 3)
        print ("el tiempo de ejecución fue: " , (t2f-t2i) )

    elif int(inputs[0:2]) == 3:
        f_inicial = input("\nIngrese la fecha inicial (B d, Y): ")
        f_final = input("Ingrese la fecha final (B d, Y): ")
        t3i= time.time()
        total_TV, list_TV = controller.listarTVPeriodo(control, f_inicial, f_final)
        t3f= time.time()
        printReq2(f_inicial, f_final, total_TV, list_TV, 3)
        print ("el tiempo de ejecución fue: " , (t3f-t3i) )
        
    elif int(inputs[0:2]) == 4:
        actor = input("Ingrese el nombre del actor: ")
        
        t4i= time.time()
        total_peliculas, total_TV, list_actor = controller.contenidosActor(control, actor)
        t4f= time.time()
        printReq3(actor, total_peliculas, total_TV, list_actor, 3)
        print ("el tiempo de ejecución fue: " , (t4f-t4i) )

    elif int(inputs[0:2]) == 5:
        genero = input("Ingrese el género a buscar: ")
        t5i= time.time()
        total_peliculas, total_TV, list_genero = controller.contenidosGenero(control, genero)
        t5f= time.time()
        printReq4(genero, total_peliculas, total_TV, list_genero, 3)
        print ("el tiempo de ejecución fue: " , (t5f-t5i) )

    elif int(inputs[0:2]) == 6:
        pais = input("Ingrese el país a consultar: ")
        t6i= time.time()
        total_peliculas, total_TV, list_pais = controller.listarPorPais(control, pais)
        t6f= time.time()
        printReq5(pais, total_peliculas, total_TV, list_pais, 3)
        print ("el tiempo de ejecución fue: " , (t6f-t6i) )

    elif int(inputs[0:2]) == 7:
       director = input("Ingrese el director a buscar: ")
       t7i= time.time()
       total_peliculas, total_TV, generos, conteo, dic_servicio, list_director = controller.contenidoDirector(control, director)
       t7f= time.time()
       printReq6(director, total_peliculas, total_TV, generos, conteo, dic_servicio, list_director, 3)
       print ("el tiempo de ejecución fue: " , (t7f-t7i))

    elif int(inputs[0:2]) == 8:
       top = int(input("Ingrese el top de géneros: "))
       t8i= time.time()
       top_generos = controller.topGeneros(control)
       t8f= time.time()
       printReq7(top, top_generos)
       print ("el tiempo de ejecución fue: " , (t8f-t8i))

    elif int(inputs[0:2]) == 9:
       top = input("Ingrese el top de actores por participación: ")
       datos = controller.topActores(control)
       printReq8(top)

    elif int(inputs[0:2]) == 10:
        sys.exit(0)

    else:
        continue
sys.exit(0)


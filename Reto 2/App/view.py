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

def newController(list_type):
    return controller.newController(list_type)

def printMenu():
    print("Bienvenido")
    print("0- Implementar ordenamientos de contenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar las películas estrenadas en un año")
    print("3- Listar programas de televisión agregados en una fecha")
    print("4- Encontrar contenido donde participa un actor")
    print("5- Encontrar contenido por un género especifico")
    print("6- Encontrar contenido producido en un país")
    print("7- Encontrar contenido con un director involucrado")
    print("8- Listar el TOP (N) de los géneros con más contenido")
    print("9- Listar el TOP (N) de los actores con más participaciones")
    print("10- Salir")

def printStreamingInfo(n_videos, s1, s2, s3, s4):
    print("\nLoaded streaming service info:")
    print("Total loaded files: " + str(n_videos) + "\n")
    table = [["Service name", "Count"], ["Amazon", s1], ["Disney", s2], ["Hulu", s3], ["Netflix", s4]]
    print(tabulate(table, tablefmt="grid", colalign=("left",)), "\n")

def printSortResults(n_videos, sorted_list, sample):
    print("Los", sample, "primeros y los últimos", sample, "videos ordenados son:")
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

def printReq1(año, total_peliculas, list_peliculas, sample):
    print("\nHay", total_peliculas, "películas estrenadas en", año)
    table = [["Release year", "Title", "Duration", "Stream service", "Director", "Cast"]]
    if total_peliculas <= sample*2 and total_peliculas > 0:
        print("\nLos", total_peliculas, "videos ordenados son:")
        for video in lt.iterator(list_peliculas):
            table.append([video["release_year"], video["title"], video["duration"], video["stream_service"], video["director"], video["cast"]])
    elif total_peliculas > 0:
        print("\nLos", sample, "primeros y los últimos", sample, "videos ordenados son:")
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

def printReq2(fecha, total_TV, list_TV, sample):
    print("\nHay", total_TV, "shows de TV estrenados en", fecha)
    table = [["Date added", "Title", "Duration", "Release year", "Stream service", "Director", "Cast"]]
    if total_TV <= sample*2 and total_TV > 0:
        print("\nLos", total_TV, "videos ordenados son:")
        for video in lt.iterator(list_TV):
            table.append([video["date_added"], video["title"], video["duration"], video["release_year"], video["stream_service"], video["director"], video["cast"]])  
    elif total_TV > 0:
        print("\nLos", sample, "primeros y los últimos", sample, "videos ordenados son:")
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
    table = [["Release year", "Title", "Duration", "Director", "Stream service", "Cast", "Country", "Listed in", "Description"]]
    if total <= sample*2 and total > 0:
        print("\nLos", total, "videos ordenados son:")
        for video in lt.iterator(list_actor):
            table.append([video["release_year"], video["title"], video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
    elif total > 0:
        print("\nLos", sample, "primeros y los últimos", sample, "videos ordenados son:")
        i = 1 
        while i <= sample: 
            video = lt.getElement(list_actor, i) 
            table.append([video["release_year"], video["title"], video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
        i = total - sample + 1
        while i <= total: 
            video = lt.getElement(list_actor, i) 
            table.append([video["release_year"], video["title"], video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[10,10,15,10,18,10,25,10,18,30]), "\n")
        
def printReq4(genero, total_peliculas, total_TV, list_genero, sample):
    total = total_peliculas + total_TV
    print(tabulate([["Conteo de contenidos", genero], ["Películas", total_peliculas], ["TV Shows", total_TV]], tablefmt="grid", colalign=("left",)))
    table = [["Release year", "Title", "Duration", "Director", "Stream service", "Cast", "Country", "Listed in", "Description"]]
    if total <= sample*2 and total > 0:
        print("\nLos", total, "videos ordenados son:")
        for video in lt.iterator(list_genero):
            table.append([video["release_year"], video["title"],  video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
    elif total > 0:
        print("\nLos", sample, "primeros y los últimos", sample, "videos ordenados son:")
        i = 1 
        while i <= sample: 
            video = lt.getElement(list_genero, i) 
            table.append([video["release_year"], video["title"],  video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
        i = total - sample + 1
        while i <= total: 
            video = lt.getElement(list_genero, i) 
            table.append([video["release_year"], video["title"],  video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[10,10,15,10,18,10,25,10,18,30]), "\n")

def printReq5(pais, total_peliculas, total_TV, list_pais, sample):
    total = total_peliculas + total_TV
    print("\nHay", total, "contenidos producidos en", pais)
    print(tabulate([["Type", "Count"], ["Películas", total_peliculas], ["TV Shows", total_TV]], tablefmt="grid", colalign=("left",)))
    table = [["Release year", "Title", "Duration", "Director", "Stream service", "Cast", "Country", "Listed in", "Description"]]
    if total <= sample*2 and total > 0:
        print("\nLos", total, "videos ordenados son:")
        for video in lt.iterator(list_pais):
            table.append([video["release_year"], video["title"], video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
    elif total > 0:
        print("\nLos", sample, "primeros videos ordenados son:") 
        i = 1 
        while i <= sample: 
            video = lt.getElement(list_pais, i) 
            table.append([video["release_year"], video["title"], video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
        print("\nLos", sample, "últimos videos ordenados son:") 
        i = total - sample + 1
        while i <= total: 
            video = lt.getElement(list_pais, i) 
            table.append([video["release_year"], video["title"], video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[10,15,10,18,10,25,10,18,30]), "\n")

def printReq6(director, total_peliculas, total_TV, generos, servicios, list_director, sample):
    total = total_peliculas + total_TV
    print("\nEn total hay", total, "contenidos de", director)
    print(tabulate([["Type", "Count"], ["Películas", total_peliculas], ["TV Shows", total_TV]], tablefmt="grid", colalign=("left",)), "\n")
    print(tabulate([["Service name", "Count"], ["Amazon Prime", servicios[0]], ["Disney Plus", servicios[1]], ["Hulu", servicios[2]], ["Netflix", servicios[3]]], tablefmt="grid", colalign=("left",)), "\n")
    table1 = [["Genero", "Conteo"]]
    for gen in lt.iterator(generos):
        table1.append([gen["Genero"], gen["Conteo"]])
    print(tabulate(table1, tablefmt="grid", colalign=("left",)))
    table = [["Release year", "Title", "Duration", "Director", "Stream service", "Cast", "Country", "Listed in", "Description"]]
    if total <= sample*2 and total > 0:
        print("\nLos", total, "videos ordenados son:")
        for video in lt.iterator(list_director):
            table.append([video["release_year"], video["title"], video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
    elif total > 0:
        print("\nLos", sample, "primeros videos ordenados son:") 
        i = 1 
        while i <= sample: 
            video = lt.getElement(list_director, i) 
            table.append([video["release_year"], video["title"], video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
        print("\nLos", sample, "últimos videos ordenados son:") 
        i = total - sample + 1
        while i <= total: 
            video = lt.getElement(list_director, i)
            table.append([video["release_year"], video["title"], video["duration"], video["director"], video["stream_service"], video["cast"], video["country"], video["listed_in"], video["description"]])
            i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[10,15,10,18,10,25,10,18,30]), "\n")

def printReq7(top, top_generos):
    print("\nEn total hay", lt.size(top_generos), "géneros\nEn el top", top, "están:")
    table = [["Ranking", "Género", "Total", "Películas", "TV Shows", "Amazon Prime", "Disney Plus", "Hulu", "Netflix"]]
    i = 1 
    while i <= top: 
        genero = lt.getElement(top_generos, i) 
        table.append([i, genero["genre"], (genero["Movies"] + genero["TV shows"]), genero["Movies"], genero["TV shows"], genero["amazon_prime"], genero["disney_plus"], genero["hulu"], genero["netflix"]])
        i += 1
    print(tabulate(table, tablefmt="grid", colalign=("left",), maxcolwidths=[10,25,15,15,15,15,15,15,15]), "\n")

def printReq8(top, datos):
    print("\n")

def castBoolean(value):
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

def printDelta(delta):
    if len(delta) == 2:
        print("Tiempo [ms]: ", f"{delta[0]:.3f}", "||",
              "Memoria [kB]: ", f"{delta[1]:.3f}", "\n")
    else:
        print("Tiempo [ms]: ", f"{delta[0]:.3f}", "\n")

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
        
        print("\nHa configurado su catálogo como", lista, "de", tamaño, "con", ord, "\n")

    elif int(inputs[0:2]) == 1:
        print("\nCargando información de los archivos ....")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        n_videos, s1, s2, s3, s4, sorted_list, delta = controller.loadData(control, tamaño, orden, mem)
        printStreamingInfo(n_videos, s1, s2, s3, s4)
        printSortResults(n_videos, sorted_list, 3)
        printDelta(delta)

    elif int(inputs[0:2]) == 2:
        año = int(input("\nIndique el año de interés: "))
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total_peliculas, list_peliculas, delta = controller.listarPeliculasPeriodo(control, año, mem)
        printReq1(año, total_peliculas, list_peliculas, 3)
        printDelta(delta)

    elif int(inputs[0:2]) == 3:
        fecha = input("\nIngrese la fecha de interés (B d, Y): ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total_TV, list_TV, delta = controller.listarTVPeriodo(control, fecha, mem)
        printReq2(fecha, total_TV, list_TV, 3)
        printDelta(delta)
        
    elif int(inputs[0:2]) == 4:
        actor = input("Ingrese el nombre del actor: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total_peliculas, total_TV, list_actor, delta = controller.contenidosActor(control, actor, mem)
        printReq3(actor, total_peliculas, total_TV, list_actor, 3)
        printDelta(delta)

    elif int(inputs[0:2]) == 5:
        genero = input("Ingrese el género a buscar: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total_peliculas, total_TV, list_genero, delta = controller.contenidosGenero(control, genero, mem)
        printReq4(genero, total_peliculas, total_TV, list_genero, 3)
        printDelta(delta)

    elif int(inputs[0:2]) == 6:
        pais = input("Ingrese el país a consultar: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total_peliculas, total_TV, list_pais, delta = controller.listarPorPais(control, pais, mem)
        printReq5(pais, total_peliculas, total_TV, list_pais, 3)
        printDelta(delta)

    elif int(inputs[0:2]) == 7:
       director = input("Ingrese el director a buscar: ")
       print("Desea observar el uso de memoria? (True/False)")
       mem = castBoolean(input("Respuesta: "))
       total_peliculas, total_TV, generos, servicios, list_director, delta = controller.contenidoDirector(control, director, mem)
       printReq6(director, total_peliculas, total_TV, generos, servicios, list_director, 3)
       printDelta(delta)

    elif int(inputs[0:2]) == 8:
       top = int(input("Ingrese el top de géneros: "))
       print("Desea observar el uso de memoria? (True/False)")
       mem = castBoolean(input("Respuesta: "))
       top_generos, delta = controller.topGeneros(control, mem)
       printReq7(top, top_generos)
       printDelta(delta)

    elif int(inputs[0:2]) == 9:
       top = input("Ingrese el top de actores por participación: ")
       print("Desea observar el uso de memoria? (True/False)")
       mem = castBoolean(input("Respuesta: "))
       datos, delta = controller.topActores(control, mem)
       printReq8(top, datos)
       printDelta(delta)

    elif int(inputs[0:2]) == 10:
        sys.exit(0)

    else:
        continue
sys.exit(0)

"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time
from datetime import datetime
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import insertionsort as ie
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mg
from DISClib.Algorithms.Sorting import quicksort as qck
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(list_type):
    catalog = {'videos': None, "movies": None, "tv_shows": None}
    catalog['videos'] = lt.newList(list_type)
    catalog["movies"] = lt.newList(list_type)
    catalog["tv_shows"] = lt.newList(list_type)
    return catalog

# Funciones para agregar informacion al catalogo

def addVideo(catalog, video, stream_service):
    video["stream_service"] = stream_service
    lt.addLast(catalog['videos'], video)
    if video["type"] == "Movie":
        lt.addLast(catalog['movies'], video)
    else:
        lt.addLast(catalog['tv_shows'], video)

# Funciones de consulta

def videosSize(catalog):
    return lt.size(catalog['videos'])

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpCarga(video1, video2):
    if int(video1['release_year']) < int(video2['release_year']):
        ord = True
    elif video1['release_year'] == video2['release_year']:
        if video1['title'] < video2['title']:
            ord = True
        else: ord = False
    else: ord = False
    return ord

def cmpReq1y6(movie1, movie2): 
    if int(movie1['release_year']) < int(movie2['release_year']):
        ord = True
    elif movie1['release_year'] == movie2['release_year']:
        if movie1['title'] < movie2['title']:
            ord = True
        elif movie1['title'] == movie2['title']:
            if movie1['duration'] < movie2['duration']:
                ord = True
            else: ord = False
        else: ord = False
    else: ord = False
    return ord
    
def cmpReq2(show1, show2):
    if (len(show1['date_added']) > 0) and (len(show2['date_added']) > 0):
        sh1 = datetime.strptime(show1['date_added'], "%Y-%m-%d")
        sh2 = datetime.strptime(show2['date_added'], "%Y-%m-%d")
        if sh1 < sh2:
            ord = True
        elif sh1 == sh2:
            if show1['title'] < show2['title']:
                ord = True
            elif show1['title'] == show2['title']:
                if show1['duration'] < show2['duration']:
                    ord = True
                else: ord = False
            else: ord = False
        else: ord = False
    else: ord = False
    return ord

def cmpReq2Rango(f_inicial, f_final, show_date):
    añadir = False
    fecha_i = datetime.strptime(f_inicial, "%B %d, %Y")
    fecha_f = datetime.strptime(f_final, "%B %d, %Y")
    s_date = datetime.strptime(show_date, "%Y-%m-%d")
    if fecha_i <= s_date <= fecha_f:
        añadir = True
    return añadir

def cmpReq3(video1, video2):
    if video1['title'] < video2['title']:
        ord = True
    elif video1['title'] == video2['title']:
        if int(video1['release_year']) < int(video2['release_year']):
            ord = True
        elif video1['release_year'] == video2['release_year']:
            if video1['duration'] < video2['duration']:
                ord = True
            else: ord = False
        else: ord = False
    else: ord = False
    return ord

def cmpReq4y5(video1, video2):
    if video1['title'] < video2['title']:
        ord = True
    elif video1['title'] == video2['title']:
        if int(video1['release_year']) < int(video2['release_year']):
            ord = True
        elif video1['release_year'] == video2['release_year']:
            if video1['director'] < video2['director']:
                ord = True
            else: ord = False
        else: ord = False
    else: ord = False
    return ord

def cmpReq7(video1, video2):
    if video1["total"] > video2["total"]:
        ord = True
    elif video1["total"] == video2["total"]:
        if video1["Movie"] > video2["Movie"]:
            ord = True
        elif video1["Movie"] == video2["Movie"]:
            if video1["TV Show"] > video2["TV Show"]:
                ord = True
            else: ord = False
        else: ord = False
    else: ord = False
    return ord

# Funciones de ordenamiento

def sortVideos(catalog, orden):
    start_time = getTime()
    sorted_list = globals()[orden].sort(catalog['videos'], cmpCarga)
    end_time = getTime() 
    delta_time = deltaTime(start_time, end_time)
    mg.sort(catalog["movies"], cmpCarga)
    mg.sort(catalog["tv_shows"], cmpCarga)
    return sorted_list, delta_time

# Requerimientos

def listarPeliculasPeriodo(catalog, a_inicial, a_final):
    list_peliculas = lt.newList("ARRAY_LIST")
    for movie in lt.iterator(catalog["movies"]):
        if a_inicial <= int(movie["release_year"]) <= a_final:
            lt.addLast(list_peliculas, movie)
        elif int(movie["release_year"]) > a_final:
            break
    total_peliculas = lt.size(list_peliculas)
    mg.sort(list_peliculas, cmpReq1y6)
    return total_peliculas, list_peliculas

def listarTVPeriodo(catalog, f_inicial, f_final):
    list_TV = lt.newList("ARRAY_LIST")
    for show in lt.iterator(catalog["tv_shows"]):
        show_date = show["date_added"]
        if len(show_date) > 0 and cmpReq2Rango(f_inicial, f_final, show_date):
            lt.addLast(list_TV, show)
    total_TV = lt.size(list_TV)
    mg.sort(list_TV, cmpReq2)
    return total_TV, list_TV

def contenidosActor(catalog, actor):
    list_actor = lt.newList("ARRAY_LIST")
    for movie in lt.iterator(catalog["movies"]):
        if actor in movie["cast"]:
            lt.addLast(list_actor, movie)
    total_peliculas = lt.size(list_actor)
    for show in lt.iterator(catalog["tv_shows"]):
        if actor in show["cast"]:
            lt.addLast(list_actor, show)
    total_TV = lt.size(list_actor) - total_peliculas
    mg.sort(list_actor, cmpReq3)
    return total_peliculas, total_TV, list_actor

def contenidosGenero(catalog, genero):
    list_genero = lt.newList("ARRAY_LIST")
    for movie in lt.iterator(catalog["movies"]):
        if genero in movie["listed_in"]:
            lt.addLast(list_genero, movie)
    total_peliculas = lt.size(list_genero)
    for show in lt.iterator(catalog["tv_shows"]):
        if genero in show["listed_in"]:
            lt.addLast(list_genero, show)
    total_TV = lt.size(list_genero) - total_peliculas
    mg.sort(list_genero, cmpReq4y5)
    return total_peliculas, total_TV, list_genero

def listarPorPais(catalog, pais):
    list_pais = lt.newList("ARRAY_LIST")
    for movie in lt.iterator(catalog["movies"]):
        if movie["country"] == pais:
            lt.addLast(list_pais, movie)
    total_peliculas = lt.size(list_pais)
    for show in lt.iterator(catalog["tv_shows"]):
        if show["country"] == pais:
            lt.addLast(list_pais, show)
    total_TV = lt.size(list_pais) - total_peliculas
    mg.sort(list_pais, cmpReq4y5)
    return total_peliculas, total_TV, list_pais

def contenidoDirector(catalog, director):
    list_director = lt.newList("ARRAY_LIST")
    generos = lt.newList("ARRAY_LIST")
    conteo = lt.newList("ARRAY_LIST")
    dic_servicio={"amazon_prime":0, "disney_plus":0, "hulu":0, "netflix":0}

    for movie in lt.iterator(catalog["movies"]):
        if director in movie["director"]:
            lt.addLast(list_director, movie)
            m_gen = movie["listed_in"].split(sep=', ')
            for gen in m_gen:
                presente = lt.isPresent(generos, gen)
                if presente == 0:
                    lt.addLast(generos, gen)
                    lt.addLast(conteo, 1)
                else:
                    lt.changeInfo(conteo, presente, lt.getElement(conteo, presente) + 1)
            dic_servicio[movie["stream_service"]]+=1
    total_peliculas = lt.size(list_director)
    for show in lt.iterator(catalog["tv_shows"]):
        if director in show["director"]:
            lt.addLast(list_director, show)
            s_gen = show["listed_in"].split(sep=', ')
            for gen in s_gen:
                presente = lt.isPresent(generos, gen)
                if presente == 0:
                    lt.addLast(generos, gen)
                    lt.addLast(conteo, 1)
                else:
                    lt.changeInfo(conteo, presente, lt.getElement(conteo, presente) + 1)
            dic_servicio[show["stream_service"]]+=1
    total_TV = lt.size(list_director) - total_peliculas
    mg.sort(list_director, cmpReq1y6)
    return total_peliculas, total_TV, generos, conteo, dic_servicio, list_director

def topGeneros(catalog):
    top_generos = lt.newList("ARRAY_LIST")
    generos = lt.newList("ARRAY_LIST")
    for video in lt.iterator(catalog["videos"]):
        v_gen = video["listed_in"].split(sep=', ')
        for gen in v_gen:
            presente = lt.isPresent(generos, gen)
            if presente == 0:
                lt.addLast(generos, gen)
                info_gen = {"nombre":gen, "total":1, "Movie":0, "TV Show":0, "amazon_prime":0, "disney_plus":0, "hulu":0, "netflix":0}
                info_gen[video["type"]] += 1
                info_gen[video["stream_service"]] += 1
                lt.addLast(top_generos, info_gen)
            else:
                genero = lt.getElement(top_generos, presente)
                genero["total"] += 1
                genero[video["type"]] += 1
                genero[video["stream_service"]] += 1
    mg.sort(top_generos, cmpReq7)
    return top_generos

# Funciones para medir tiempos de ejecucion

def getTime():
    return float(time.perf_counter()*1000)

def deltaTime(start, end):
    elapsed = float(end - start)
    return elapsed
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
 """

import config as cf
import model
import csv
import time
import tracemalloc
csv.field_size_limit(2147483647)

# Inicialización del Catálogo

def newController(list_type):
    control = {
        'model': None
    }
    control['model'] = model.newCatalog(list_type)
    return control

# Funciones para la carga de datos

def loadData(control, tamaño, orden, memflag=True):
    catalog = control['model']
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    n_videos, s1, s2, s3, s4 = loadVideos(catalog, tamaño)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    sorted_list = sortVideos(catalog, orden)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return n_videos, s1, s2, s3, s4, sorted_list, (delta_time, delta_memory)
    else:
        return n_videos, s1, s2, s3, s4, sorted_list, (delta_time,)

def loadVideos(catalog, tamaño):
    videosfile1 = cf.data_dir + 'Streaming/amazon_prime_titles-utf8-' + tamaño + '.csv'
    videosfile2 = cf.data_dir + 'Streaming/disney_plus_titles-utf8-' + tamaño + '.csv'
    videosfile3 = cf.data_dir + 'Streaming/hulu_titles-utf8-' + tamaño + '.csv'
    videosfile4 = cf.data_dir + 'Streaming/netflix_titles-utf8-' + tamaño + '.csv'

    input_file1 = csv.DictReader(open(videosfile1, encoding='utf-8'))
    input_file2 = csv.DictReader(open(videosfile2, encoding='utf-8'))
    input_file3 = csv.DictReader(open(videosfile3, encoding='utf-8'))
    input_file4 = csv.DictReader(open(videosfile4, encoding='utf-8'))

    for video in input_file1:
        model.addVideo(catalog, video, "amazon_prime")
    s1 = model.videosSize(catalog)
    for video in input_file2:
        model.addVideo(catalog, video, "disney_plus")
    s2 = model.videosSize(catalog) - s1
    for video in input_file3:
        model.addVideo(catalog, video, "hulu")
    s3 = model.videosSize(catalog) - (s1 + s2)
    for video in input_file4:
        model.addVideo(catalog, video, "netflix")
    s4 = model.videosSize(catalog) - (s1 + s2 + s3)
    return model.videosSize(catalog), s1, s2, s3, s4

# Funciones de ordenamiento

def sortVideos(catalog, orden):
    return model.sortVideos(catalog, orden)

# Requerimientos

def listarPeliculasPeriodo(control, año, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total_peliculas, list_peliculas = model.listarPeliculasPeriodo(control['model'], año)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total_peliculas, list_peliculas, (delta_time, delta_memory)
    else:
        return total_peliculas, list_peliculas, (delta_time,)

def listarTVPeriodo(control, fecha, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total_TV, list_TV = model.listarTVPeriodo(control['model'], fecha)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total_TV, list_TV, (delta_time, delta_memory)
    else:
        return total_TV, list_TV, (delta_time,)

def contenidosActor(control, actor, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total_peliculas, total_TV, list_actor = model.contenidosActor(control['model'], actor)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total_peliculas, total_TV, list_actor, (delta_time, delta_memory)
    else:
        return total_peliculas, total_TV, list_actor, (delta_time,)

def contenidosGenero(control, genero, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total_peliculas, total_TV, list_genero = model.contenidosGenero(control['model'], genero)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total_peliculas, total_TV, list_genero, (delta_time, delta_memory)
    else:
        return total_peliculas, total_TV, list_genero, (delta_time,)

def listarPorPais(control, pais, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total_peliculas, total_TV, list_pais = model.listarPorPais(control['model'], pais)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total_peliculas, total_TV, list_pais, (delta_time, delta_memory)
    else:
        return total_peliculas, total_TV, list_pais, (delta_time,)

def contenidoDirector(control, director, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total_peliculas, total_TV, generos, servicios, list_director = model.contenidoDirector(control['model'], director)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total_peliculas, total_TV, generos, servicios, list_director, (delta_time, delta_memory)
    else:
        return total_peliculas, total_TV, generos, servicios, list_director, (delta_time,)

def topGeneros(control, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    top_generos = model.topGeneros(control['model'])
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return top_generos, (delta_time, delta_memory)
    else:
        return top_generos, (delta_time,)

def topActores(control, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    datos = model.topActores(control['model'])
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return datos, (delta_time, delta_memory)
    else:
        return datos, (delta_time,)

# Funciones para medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

# Funciones para medir la memoria utilizada

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
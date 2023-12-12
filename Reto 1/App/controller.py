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
csv.field_size_limit(2147483647)

# Inicialización del Catálogo

def newController(list_type):
    control = {
        'model': None
    }
    control['model'] = model.newCatalog(list_type)
    return control

# Funciones para la carga de datos

def loadData(control, tamaño, orden):
    catalog = control['model']
    n_videos, s1, s2, s3, s4  = loadVideos(catalog, tamaño)
    sorted_list, delta_time = sortVideos(catalog, orden)
    return sorted_list, delta_time, n_videos, s1, s2, s3, s4

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

def listarPeliculasPeriodo(control, a_inicial, a_final):
    return model.listarPeliculasPeriodo(control['model'], a_inicial, a_final)

def listarTVPeriodo(control, f_inicial, f_final):
    return model.listarTVPeriodo(control['model'], f_inicial, f_final)

def contenidosActor(control, actor):
    return model.contenidosActor(control['model'], actor)

def contenidosGenero(control, genero):
    return model.contenidosGenero(control['model'], genero)

def listarPorPais(control, pais):
    return model.listarPorPais(control['model'], pais)

def contenidoDirector(control, director):
    return model.contenidoDirector(control['model'], director)

def topGeneros(control):
    return model.topGeneros(control['model'])

def topActores(control):
    return model.topActores(control['model'])


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
from datetime import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
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
    catalog = {'videos': None, 
                "movies": None, 
                "tv_shows": None,
                "listed_in": None}
    catalog['videos'] = lt.newList(list_type, cmpCarga)
    catalog['listed_in'] = mp.newMap(500,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=cmpMapAlfabetico)
    catalog['release_year'] = mp.newMap(150,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=cmpMapAlfabetico)
    catalog['date_added'] = mp.newMap(6000,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=cmpMapAlfabetico)
    catalog['cast'] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=cmpMapAlfabetico)
    catalog['country'] = mp.newMap(200,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=cmpMapAlfabetico)
    catalog['director'] = mp.newMap(9000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=cmpMapAlfabetico)
    return catalog

# Funciones para agregar informacion al catalogo

def addVideo(catalog, video, stream_service):
    video["stream_service"] = stream_service
    lt.addLast(catalog['videos'], video)
    if video["type"] == "Movie":
        type = "Movies"
        addVideoYear(catalog['release_year'], video["release_year"], video)
    else:
        type = "TV shows"
        if len(video['date_added']) > 0: 
            addVideoDate(catalog['date_added'], video["date_added"], video)
    v_gen = video["listed_in"].split(sep=', ')
    # Si queremos separar también por &
    #v_gen = (video["listed_in"].replace(" & ", ", ")).split(sep=', ')
    for gen in v_gen:
        addVideoGenre(catalog['listed_in'], gen.strip(), video, type, stream_service)
    if len(video["cast"]) > 0:
        v_cast = video["cast"].split(sep=', ')
        for actor in v_cast:
            addVideoActor(catalog["cast"], actor.strip(), video, type)
    if len(video['country']) > 0:
        v_country = video["country"].split(sep=', ')
        for country in v_country:
            addVideoCountry(catalog["country"], country.strip(), video, type)
    if len(video['director']) > 0:
        v_director = video["director"].split(sep=', ')
        for director in v_director:
            addVideoDirector(catalog["director"], director.strip(), video, type, stream_service)

def addVideoYear(map, year, video):
    exist = mp.contains(map, year)
    if exist:
        entry = mp.get(map, year)
        value = me.getValue(entry)
    else:
        value = newYear(year)
        mp.put(map, year, value)
    lt.addLast(value['videos'], video)

def addVideoDate(map, date, video):
    exist = mp.contains(map, date)
    if exist:
        entry = mp.get(map, date)
        value = me.getValue(entry)
    else:
        value = newDate(date)
        mp.put(map, date, value)
    lt.addLast(value['videos'], video)

def addVideoActor(map, actor, video, type):
    exist = mp.contains(map, actor)
    if exist:
        entry = mp.get(map, actor)
        value = me.getValue(entry)
    else:
        value = newActor(actor)
        mp.put(map, actor, value)
    lt.addLast(value['videos'], video)
    value[type] += 1

def addVideoGenre(map, gen, video, type, service):
    exist = mp.contains(map, gen)
    if exist:
        entry = mp.get(map, gen)
        value = me.getValue(entry)
    else:
        value = newGenre(gen)
        mp.put(map, gen, value)
    lt.addLast(value['videos'], video)
    value[type] += 1
    value[service] += 1

def addVideoCountry(map, country, video, type):
    exist = mp.contains(map, country)
    if exist:
        entry = mp.get(map, country)
        value = me.getValue(entry)
    else:
        value = newCountry(country)
        mp.put(map, country, value)
    lt.addLast(value['videos'], video)
    value[type] += 1

def addVideoDirector(map, director, video, type, service):
    exist = mp.contains(map, director)
    if exist:
        entry = mp.get(map, director)
        value = me.getValue(entry)
    else:
        value = newDirector(director)
        mp.put(map, director, value)
    lt.addLast(value['videos'], video)
    value[type] += 1
    value[service] += 1

# Funciones para creacion de datos

def newYear(year):
    return {'year': str(year), "videos": lt.newList("ARRAY_LIST")}

def newDate(date):
    return {'date': date, "videos": lt.newList("ARRAY_LIST")}

def newActor(actor):
    return {'actor': actor, "videos": lt.newList("ARRAY_LIST"), "Movies": 0, "TV shows": 0}    

def newGenre(gen):
    return {'genre': gen, "videos": lt.newList("ARRAY_LIST"), "Movies": 0, "TV shows": 0, 
            "amazon_prime": 0, "disney_plus": 0, "hulu": 0, "netflix": 0}

def newCountry(country):
    return {'country': country, "videos": lt.newList("ARRAY_LIST"), "Movies": 0, "TV shows": 0}
    
def newDirector(director):
    return {'director': director, "videos": lt.newList("ARRAY_LIST"), "Movies": 0, "TV shows": 0,
            "amazon_prime": 0, "disney_plus": 0, "hulu": 0, "netflix": 0}

# Funciones de consulta

def videosSize(catalog):
    return lt.size(catalog['videos'])

# Funciones de comparación

def cmpCarga(video1, video2):
    if int(video1['release_year']) < int(video2['release_year']):
        ord = True
    elif video1['release_year'] == video2['release_year']:
        if video1['title'] < video2['title']:
            ord = True
        else: ord = False
    else: ord = False
    return ord

def cmpMapAlfabetico(cmp, entry):
    m_entry = me.getKey(entry)
    if cmp == m_entry:
        return 0
    elif cmp > m_entry:
        return 1
    else:
        return -1

def cmpReq1y2(movie1, movie2): 
    if movie1['title'] < movie2['title']:
        ord = True
    elif movie1['title'] == movie2['title']:
        if movie1['duration'] < movie2['duration']:
            ord = True
        else: ord = False
    else: ord = False
    return ord

def cmpReq345y6(movie1, movie2): 
    if int(movie1['release_year']) > int(movie2['release_year']):
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

def cmpReq7(video1, video2):
    if (video1["Movies"]+video1["TV shows"]) > (video2["Movies"]+ video2["TV shows"]):
        ord = True
    elif (video1["Movies"]+video1["TV shows"]) == (video2["Movies"]+ video2["TV shows"]):
        if video1["Movies"] > video2["Movies"]:
            ord = True
        elif video1["Movies"] == video2["Movies"]:
            if video1["TV shows"] > video2["TV shows"]:
                ord = True
            else: ord = False
        else: ord = False
    else: ord = False
    return ord

# Funciones de ordenamiento

def sortVideos(catalog, orden):
    return globals()[orden].sort(catalog['videos'], cmpCarga)

# Requerimientos

def listarPeliculasPeriodo(catalog, año):
    list_peliculas = lt.newList("ARRAY_LIST")
    year = mp.get(catalog['release_year'], str(año))
    if year:
        list_peliculas = me.getValue(year)['videos']
    total_peliculas = lt.size(list_peliculas)
    mg.sort(list_peliculas, cmpReq1y2)
    return total_peliculas, list_peliculas

def listarTVPeriodo(catalog, fecha):
    list_TV = lt.newList("ARRAY_LIST")
    date = mp.get(catalog['date_added'], fecha)
    if date:
        list_TV = me.getValue(date)['videos']
    total_TV = lt.size(list_TV)
    mg.sort(list_TV, cmpReq1y2)
    return total_TV, list_TV

def contenidosActor(catalog, actor):
    list_actor = lt.newList("ARRAY_LIST")
    total_peliculas, total_TV = 0, 0
    actor = mp.get(catalog['cast'], actor)
    if actor:
        value = me.getValue(actor)
        list_actor = value['videos']
        total_peliculas, total_TV = value['Movies'], value['TV shows']
    mg.sort(list_actor, cmpReq345y6)
    return total_peliculas, total_TV, list_actor

def contenidosGenero(catalog, genero):
    list_genero = lt.newList("ARRAY_LIST")
    total_peliculas, total_TV = 0,0
    genero= mp.get(catalog['listed_in'],genero)
    if genero:
        value = me.getValue(genero)
        list_genero = value['videos']
        total_peliculas, total_TV = value['Movies'], value['TV shows']
    mg.sort(list_genero, cmpReq345y6)
    return total_peliculas, total_TV, list_genero

def listarPorPais(catalog, pais):
    list_pais = lt.newList("ARRAY_LIST")
    total_peliculas, total_TV = 0, 0
    country = mp.get(catalog['country'], pais)
    if country:
        value = me.getValue(country)
        list_pais = value['videos']
        total_peliculas, total_TV = value['Movies'], value['TV shows']
    mg.sort(list_pais, cmpReq345y6)
    return total_peliculas, total_TV, list_pais

def contenidoDirector(catalog, director):
    list_director = lt.newList("ARRAY_LIST")
    total_peliculas, total_TV, am, di, hu, ne = 0, 0, 0, 0, 0, 0
    generos = mp.newMap(20, maptype='PROBING', loadfactor=0.5)
    direct = mp.get(catalog['director'], director)
    if direct:
        value = me.getValue(direct)
        list_director = value['videos']
        total_peliculas, total_TV = value['Movies'], value['TV shows']
        am, di, hu, ne = value['amazon_prime'], value['disney_plus'], value['hulu'], value['netflix']
        for video in lt.iterator(list_director):
            v_gen = video["listed_in"].split(sep=', ')
            for gen in v_gen:
                exist = mp.contains(generos, gen)
                if exist:
                    entry = mp.get(generos, gen)
                    value = me.getValue(entry)
                else:
                    value = {"Genero": gen, "Conteo": 0}
                    mp.put(generos, gen, value)
                value["Conteo"] += 1
    mg.sort(list_director, cmpReq345y6)
    return total_peliculas, total_TV, mp.valueSet(generos), (am, di, hu, ne), list_director

def topGeneros(catalog):
    top_generos = mp.valueSet(catalog["listed_in"])
    mg.sort(top_generos, cmpReq7)
    return top_generos

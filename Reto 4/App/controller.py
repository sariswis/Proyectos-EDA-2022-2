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

def newCatalog():
    return model.newCatalog()

# Funciones para la carga de datos

def loadData(catalog, tamaño, mem = True):
    start_time, start_memory = startTimeMemory(mem)
    t_rutas, t_rutas_e, t_exclusiv, t_trasb, t_vertices, t_arcos, rango, estaciones = loadInfo(catalog, tamaño)
    delta_time = endTime(start_time)
    if mem is True:
        delta_memory = endMemory(start_memory)
        return t_rutas, t_rutas_e, t_exclusiv, t_trasb, t_vertices, t_arcos, rango, estaciones, (delta_time, delta_memory)
    else: return t_rutas, t_rutas_e, t_exclusiv, t_trasb, t_vertices, t_arcos, rango, estaciones, (delta_time,)

def loadInfo(catalog, tamaño):
    bus_stops = cf.data_dir + 'Barcelona/bus_stops_bcn-utf8-' + tamaño + '.csv'
    bus_edges = cf.data_dir + 'Barcelona/bus_edges_bcn-utf8-' + tamaño + '.csv'
    input_stops = csv.DictReader(open(bus_stops, encoding='utf-8'))
    input_edges = csv.DictReader(open(bus_edges, encoding='utf-8'))
    print("Cargando estaciones...")
    for stop in input_stops:
        model.processStop(catalog['totals'], catalog['stations'], catalog['stops'], catalog['neighborhoods'], catalog['connections'], catalog['simple'], stop)
    print("Cargando rutas...")
    for edge in input_edges:
        model.processEdge(catalog['totals'], catalog['stops'], catalog['connections'], catalog['simple'], edge)
    return model.totals(catalog['totals'], catalog['stations'], catalog['connections'])

# Requerimientos

def caminoPosible(catalog, origen, destino, mem = True):
    start_time, start_memory = startTimeMemory(mem)
    distancia, ruta = model.caminoPosible(catalog, origen, destino)
    delta_time = endTime(start_time)
    if mem is True:
        delta_memory = endMemory(start_memory)
        return distancia, ruta, (delta_time, delta_memory)
    else: return distancia, ruta, (delta_time,)

def caminoMenosParadas(catalog, origen, destino, mem = True):
    start_time, start_memory = startTimeMemory(mem)
    distancia, ruta = model.caminoMenosParadas(catalog, origen, destino)
    delta_time = endTime(start_time)
    if mem is True:
        delta_memory = endMemory(start_memory)
        return distancia, ruta, (delta_time, delta_memory)
    else: return distancia, ruta, (delta_time,)

def componentesConectados(catalog, mem = True):
    start_time, start_memory = startTimeMemory(mem)
    total, componentes = model.componentesConectados(catalog)
    delta_time = endTime(start_time)
    if mem is True:
        delta_memory = endMemory(start_memory)
        return total, componentes, (delta_time, delta_memory)
    else: return total, componentes, (delta_time,)

def caminoDosPuntos(catalog, lon_origen, lat_origen, lon_destino, lat_destino, mem = True):
    start_time, start_memory = startTimeMemory(mem)
    total, ruta = model.caminoDosPuntos(catalog, lon_origen, lat_origen, lon_destino, lat_destino,)
    delta_time = endTime(start_time)
    if mem is True:
        delta_memory = endMemory(start_memory)
        return total, ruta, (delta_time, delta_memory)
    else: return total, ruta, (delta_time,)

def estacionesAlcanzables(catalog, origen, conexiones, mem = True):
    start_time, start_memory = startTimeMemory(mem)
    reporte, total = model.estacionesAlcanzables(catalog, origen, conexiones)
    delta_time = endTime(start_time)
    if mem is True:
        delta_memory = endMemory(start_memory)
        return reporte, total, (delta_time, delta_memory)
    else: return reporte, total, (delta_time,)

def caminoEstacionVecindario(catalog, origen, vecindario, mem = True):
    start_time, start_memory = startTimeMemory(mem)
    distancia, t_estac, t_trasb, ruta = model.caminoEstacionVecindario(catalog, origen, vecindario)
    delta_time = endTime(start_time)
    if mem is True:
        delta_memory = endMemory(start_memory)
        return distancia, t_estac, t_trasb, ruta, (delta_time, delta_memory)
    else: return distancia, t_estac, t_trasb, ruta, (delta_time,)

def caminoCircular(catalog, origen, mem = True):
    start_time, start_memory = startTimeMemory(mem)
    distancia, t_estac, t_trasb, ruta = model.caminoCircular(catalog, origen)
    delta_time = endTime(start_time)
    if mem is True:
        delta_memory = endMemory(start_memory)
        return distancia, t_estac, t_trasb, ruta, (delta_time, delta_memory)
    else: return distancia, t_estac, t_trasb, ruta, (delta_time,)

# Funciones compartidas

def startTimeMemory(mem):
    start_time = getTime()
    start_memory = None
    if mem is True:
        tracemalloc.start()
        start_memory = getMemory()
    return start_time, start_memory

def endTime(start_time):
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    return delta_time

def endMemory(start_memory):
    stop_memory = getMemory()
    tracemalloc.stop()
    delta_memory = deltaMemory(stop_memory, start_memory)
    return delta_memory

# Funciones de medición

def getTime():
    return float(time.perf_counter()*1000)

def deltaTime(end, start):
    return float(end - start)

def getMemory():
    return tracemalloc.take_snapshot()

def deltaMemory(stop_memory, start_memory):
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    delta_memory = delta_memory/1024.0
    return delta_memory


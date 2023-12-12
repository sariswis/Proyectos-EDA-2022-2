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

def newController():
    return model.newCatalog()

# Funciones para la carga de datos

def loadData(catalog, tamaño, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    s_games, s_categories = loadSpeedruns(catalog, tamaño)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    l_games, l_categories = catalog['Games'], catalog['Categories']
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return s_games, s_categories, l_games, l_categories, (delta_time, delta_memory)
    else:
        return s_games, s_categories, l_games, l_categories, (delta_time,)

def loadSpeedruns(catalog, tamaño):
    game_data = cf.data_dir + 'Speedruns/game_data_utf-8-' + tamaño + '.csv'
    category_data = cf.data_dir + 'Speedruns/category_data_urf-8-' + tamaño + '.csv'
    input_game = csv.DictReader(open(game_data, encoding='utf-8'))
    input_category = csv.DictReader(open(category_data, encoding='utf-8'))
    for game in input_game:
        model.addGame(catalog, game)
    s_games = model.listSize(catalog['Games'])
    for category in input_category:
        model.addCategory(catalog, category)
    s_categories = model.listSize(catalog['Categories'])
    return s_games, s_categories

# Requerimientos

def juegosRecientesPlataforma(control, platf, fecha_i, fecha_f, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total, total_rango, total_fechas, l_dates = model.juegosRecientesPlataforma(control, platf, fecha_i, fecha_f)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total, total_rango, total_fechas, l_dates, (delta_time, delta_memory)
    else:
        return total, total_rango, total_fechas, l_dates, (delta_time,)

def registrosMejorTiempo(control, player, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total_r, n_runs, l_player = model.registrosMejorTiempo(control, player)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total_r, n_runs, l_player, (delta_time, delta_memory)
    else:
        return total_r, n_runs, l_player, (delta_time,)

def registrosDuracionIntentos(control, runs_i, runs_f, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total, total_rango, l_runs = model.registrosDuracionIntentos(control, runs_i, runs_f)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total, total_rango, l_runs, (delta_time, delta_memory)
    else:
        return total, total_rango, l_runs, (delta_time,)

def registrosDuracionFechas(control, fecha_i, fecha_f, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total, total_rango, l_dates = model.registrosDuracionFechas(control, fecha_i, fecha_f)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total, total_rango, l_dates, (delta_time, delta_memory)
    else:
        return total, total_rango, l_dates, (delta_time,)

def registrosRecientesTiempos(control, tiempo_i, tiempo_f, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total, total_rango, l_time = model.registrosRecientesTiempos(control, tiempo_i, tiempo_f)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total, total_rango, l_time, (delta_time, delta_memory)
    else:
        return total, total_rango, l_time, (delta_time,)

def histogramaTiemposAño(control, año_i, año_f, bins, levels, prop, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total_c, total_i, mini, maxi, hist = model.histogramaTiemposAño(control, año_i, año_f, bins, levels, prop)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total_c, total_i, mini, maxi, hist, (delta_time, delta_memory)
    else:
        return total_c, total_i, mini, maxi, hist, (delta_time,)

def juegosMasRentables(control, platf, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    total_g, total_p, unique, l_games = model.juegosMasRentables(control, platf)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total_g, total_p, unique, l_games, (delta_time, delta_memory)
    else:
        return total_g, total_p, unique, l_games, (delta_time,)

def distribRecordsContinente(control, memflag=True):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    data = model.distribRecordsContinente(control, )
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return data, (delta_time, delta_memory)
    else:
        return data, (delta_time,)

# Funciones para medir tiempos de ejecucion

def getTime():
    return float(time.perf_counter()*1000)

def deltaTime(end, start):
    return float(end - start)

# Funciones para medir la memoria utilizada

def getMemory():
    return tracemalloc.take_snapshot()

def deltaMemory(stop_memory, start_memory):
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    delta_memory = delta_memory/1024.0
    return delta_memory

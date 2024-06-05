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
import numpy as np
from datetime import datetime
from statistics import mean
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import mergesort as mg
from DISClib.DataStructures import mapentry as me
assert cf

# Construccion de modelos

def newCatalog():
    catalog = {'Games': lt.newList("ARRAY_LIST"), "Categories": lt.newList("ARRAY_LIST")}
    catalog["Game_Id"] = mp.newMap(1000, maptype='PROBING')
    catalog['Platforms'] = mp.newMap(100, maptype='PROBING')
    catalog['Players_0'] = mp.newMap(30000, maptype='PROBING')
    catalog['Num_Runs'] = om.newMap(omaptype='RBT', comparefunction=cmpMenorMayor)
    catalog['Record_Date_0'] = om.newMap(omaptype='RBT', comparefunction=cmpMayorMenor)
    catalog['Time_0'] = om.newMap(omaptype='RBT', comparefunction=cmpMenorMayor)
    catalog['Years'] = om.newMap(omaptype='RBT', comparefunction=cmpMenorMayor)
    catalog['Platforms_2'] = mp.newMap(100, maptype='PROBING', loadfactor=0.5)
    return catalog

# Funciones para agregar informacion al catalogo

def addGame(catalog, game):
    game['Release_Date'] = datetime.strptime(game['Release_Date'], '%y-%m-%d').strftime('%Y-%m-%d')
    lt.addLast(catalog['Games'], game)
    createIndex(catalog['Game_Id'], game['Game_Id'], game)
    unique = not(", " in game['Platforms'])
    platforms = game['Platforms'].split(sep=', ')
    for platform in platforms:
        updatePlatforms(catalog['Platforms'], platform, game)
        createPlatforms(catalog['Platforms_2'], platform, game, unique)

def addCategory(catalog, category):
    game = me.getValue(mp.get(catalog["Game_Id"], category["Game_Id"]))
    category["Name"], category["Year"], category["Platforms"] = game["Name"], game["Year"], game['Platforms']
    category['Record_Date_0'] = category['Record_Date_0'][0:19].replace("T", " ")
    timeAvg(category, category['Time_0'], category['Time_1'], category['Time_2'])
    lt.addLast(catalog['Categories'], category)
    players = category['Players_0'].split(sep=',')
    for player in players:
        updatePlayers(catalog['Players_0'], player, category)
    updateNumRuns(catalog['Num_Runs'], category['Num_Runs'], category)
    if len(category['Record_Date_0']) > 3: updateRecDate(catalog['Record_Date_0'], category['Record_Date_0'], category)
    updateTime0(catalog['Time_0'], category['Time_0'], category)
    updateYears(catalog['Years'], category['Year'], category)
    if category['Misc'] == "False":
        for platform in category['Platforms']:
            updatePlatforms2(catalog['Platforms_2'], platform, category)

# Funciones para creacion de datos

def createIndex(map, key, game):
    value = {"Name":game['Name'], "Year":game['Release_Date'][0:4], "Platforms":game['Platforms'].split(sep=', ')}
    return mp.put(map, key, value)

def updatePlatforms(map, platform, game):
    if mp.contains(map, platform):
        entry = mp.get(map, platform)
        value = me.getValue(entry)
    else:
        value = {"M_Count":0, "Map":om.newMap(omaptype='RBT', comparefunction=cmpMayorMenor)}
        mp.put(map, platform, value)
    date = datetime.strptime(game['Release_Date'], '%Y-%m-%d')
    entry = om.get(value["Map"], date)
    if entry is None:
        datentry = {"Date":game['Release_Date'], "G_Count":0, "Games":lt.newList("ARRAY_LIST", cmpReq1)}
        om.put(value["Map"], date, datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry["Games"], game)
    datentry["G_Count"] += 1
    value["M_Count"] += 1
    
def updatePlayers(map, player, category):
    if mp.contains(map, player):
        entry = mp.get(map, player)
        value = me.getValue(entry)
    else:
        value = {"R_Count":0, "Num_Runs":0, "Map":om.newMap(omaptype='RBT', comparefunction=cmpMenorMayor)}
        mp.put(map, player, value)
    entry = om.get(value["Map"], float(category['Time_0']))
    if entry is None:
        p_entry = {"T_Count":0, "Records":lt.newList("ARRAY_LIST", cmpReq2)}
        om.put(value["Map"], float(category['Time_0']), p_entry)
    else:
        p_entry = me.getValue(entry)
    lt.addLast(p_entry["Records"], category)
    p_entry["T_Count"] += 1
    value["R_Count"] += 1
    value["Num_Runs"] += int(category['Num_Runs'])
    
def updateNumRuns(map, runs, category):
    entry = om.get(map, int(runs))
    if entry is None:
        datentry = {"Num_Runs":runs, "C_Count":0, "Categories":lt.newList("ARRAY_LIST", cmpReq3)}
        om.put(map, int(runs), datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry["Categories"], category)
    datentry["C_Count"] += 1

def updateRecDate(map, r_date, category):
    date = datetime.strptime(r_date, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, date)
    if entry is None:
        datentry = {"Date":r_date, "C_Count":0, "Categories":lt.newList("ARRAY_LIST", cmpReq4)}
        om.put(map, date, datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry["Categories"], category)
    datentry["C_Count"] += 1

def updateTime0(map, time, category):
    entry = om.get(map, float(time))
    if entry is None:
        datentry = {"Time":time, "C_Count":0, "Categories":lt.newList("ARRAY_LIST", cmpReq5)}
        om.put(map, float(time), datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry["Categories"], category)
    datentry["C_Count"] += 1

def updateYears(map, year, category):
    entry = om.get(map, int(year))
    if entry is None:
        prop = {"Time_0":[], "Time_1":{"Count_1":0, "Times_1":[]}, "Time_2":{"Count_2":0, "Times_2":[]}, "Time_Avg":[], "Num_Runs":[]}
        datentry = {"C_Count":0, "Properties":prop}
        om.put(map, int(year), datentry)
    else:
        datentry = me.getValue(entry)
    datentry["Properties"]["Time_0"].append(float(category["Time_0"]))
    if len(category["Time_1"]) > 1: 
        time_1 = datentry["Properties"]["Time_1"]
        time_1["Times_1"].append(float(category["Time_1"]))
        time_1["Count_1"] += 1
    if len(category["Time_2"]) > 1: 
        time_2 = datentry["Properties"]["Time_2"]
        time_2["Times_2"].append(float(category["Time_2"]))
        time_2["Count_2"] += 1
    datentry["Properties"]["Time_Avg"].append(float(category["Time_Avg"]))
    datentry["Properties"]["Num_Runs"].append(int(category["Num_Runs"])) 
    datentry["C_Count"] += 1

def createPlatforms(map, platform, game, unique):
    if mp.contains(map, platform):
        entry = mp.get(map, platform)
        value = me.getValue(entry)
    else:
        value = {"G_Count":0, "Unique":0, "pt":0, "Map":mp.newMap(120, maptype='PROBING')}
        mp.put(map, platform, value)
    entry = mp.get(value["Map"], game["Game_Id"])
    if entry is None:
        datentry = {"Info_game":game, "gt":0, "B_Time_Avg":[]}
        mp.put(value["Map"], game["Game_Id"], datentry)
        value["G_Count"] += 1
        if unique: value["Unique"] += 1

def updatePlatforms2(map, platform, category):
    value = me.getValue(mp.get(map, platform))
    entry = me.getValue(mp.get(value["Map"], category["Game_Id"]))
    entry["B_Time_Avg"].append(float(category["Time_Avg"]))
    entry["gt"] += 1
    value["pt"] += 1

# Auxiliares

def timeAvg(category, time_0, time_1, time_2):
    t0 = round(float(time_0), 2)
    category["Time_0"] = str(t0)
    times = [t0]
    if len(time_1) > 1:
        t1 = round(float(time_1), 2)
        category["Time_1"] = str(t1)
        times.append(t1)
    if len(time_2) > 1:
        t2 = round(float(time_2), 2) 
        category["Time_2"] = str(t2)
        times.append(t2)
    category["Time_Avg"] = round(mean(times), 2)

def putProperty(map, prop):
    entry = om.get(map, prop)
    if entry is None:
        datentry = {"Value":prop, "Count":0}
        om.put(map, prop, datentry)
    else:
        datentry = me.getValue(entry)
    datentry["Count"] += 1

def getIntervals(mini, maxi, map_prop, hist, bins, levels, prop):
    if prop == "Num_Runs": r, j = 0, 1
    else: r, j = 2, 0.01
    diferen = maxi - mini
    tam_bin = round(diferen / bins, r)
    intervals = [maxi]
    for i in range(0, bins - 1):
        intervals.append(round(intervals[i] - tam_bin, r))
    intervals.append(mini)
    intervals.reverse()
    for i in range(0, bins):
        bin = "(" + str(intervals[i]) + ", " + str(intervals[i + 1]) + "]"
        count = 0
        if i == 0: values = om.values(map_prop, intervals[i], intervals[i + 1])
        else : values = om.values(map_prop, round(intervals[i] + j, r), intervals[i + 1])
        for value in lt.iterator(values):
            count += value["Count"]
        level = round(count / levels)
        lt.addLast(hist, {"Bin":bin, "Count":count, "Level":level})
    return hist

def putInfoGame(map, info_game):
    entry = om.get(map, info_game["Stream_Revenue"])
    if entry is None:
        datentry = lt.newList("ARRAY_LIST")
        om.put(map, info_game["Stream_Revenue"], datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry, info_game)
    
def calculateStreamRevenue(info_game, year, total_runs, b_time_avg, gt, pt):
    if year >= 2018:
        antiguedad = year - 2017
    elif 1998 < year < 2018:
        antiguedad = (-1/5)*year + 404.6
    elif year <= 1998:
        antiguedad = 5
    popularity = np.emath.log(total_runs)
    time_avg = mean(b_time_avg)
    revenue = 0
    for t_avg in b_time_avg:
        revenue += (popularity*(t_avg/60))/antiguedad
    market_share = gt/pt
    stream_revenue = revenue*market_share
    info_game["Time_Avg"], info_game["Market_Share"] = time_avg, market_share
    info_game["Stream_Revenue"] = stream_revenue

# Funciones de consulta

def listSize(list):
    return lt.size(list)

# Funciones de comparación

def cmpMayorMenor(t1, t2):
    if (t1 == t2): return 0
    elif (t1 < t2): return 1
    else: return -1

def cmpMenorMayor(t1, t2):
    if (t1 == t2): return 0
    elif (t1 > t2): return 1
    else: return -1

def cmpReq1(game1, game2):
    if game1['Abbreviation'] < game2['Abbreviation']:
        ord = True
    elif game1['Abbreviation'] == game2['Abbreviation']:
        if game1['Name'] < game2['Name']:
            ord = True
        else: ord = False
    else: ord = False
    return ord

def cmpReq2(cat1, cat2):
    if len(cat1['Record_Date_0']) > 1 and len(cat2['Record_Date_0']) > 1:
        r1 = datetime.strptime(cat1['Record_Date_0'], '%Y-%m-%d %H:%M:%S')
        r2 = datetime.strptime(cat2['Record_Date_0'], '%Y-%m-%d %H:%M:%S')
        if r1 > r2:
            ord = True
        elif r1 == r2:
            if cat1['Name'] < cat2['Name']:
                ord = True
            else: ord = False
        else: ord = False
    else: ord = False
    return ord 

def cmpReq3(cat1, cat2):
    if len(cat1['Record_Date_0']) > 1 and len(cat2['Record_Date_0']) > 1:
        r1 = datetime.strptime(cat1['Record_Date_0'], '%Y-%m-%d %H:%M:%S')
        r2 = datetime.strptime(cat2['Record_Date_0'], '%Y-%m-%d %H:%M:%S')
        if float(cat1['Time_0']) < float(cat2['Time_0']): #Esta poniendo los más rápidos primero
            ord = True
        elif cat1['Time_0'] == cat2['Time_0']:
            if r1 > r2:
                ord = True
            elif r1 == r2:
                if cat1['Name'] < cat2['Name']:
                    ord = True
                else: ord = False
            else: ord = False
        else: ord = False
    else: ord = False
    return ord

def cmpReq4(cat1, cat2):
    if float(cat1['Time_0']) > float(cat2['Time_0']): #Esta poniendo los más lentos primero
        ord = True
    elif cat1['Time_0'] == cat2['Time_0']:
        if int(cat1['Num_Runs']) > int(cat2['Num_Runs']): #Esta poniendo los más primero
            ord = True
        elif cat1['Num_Runs'] == cat2['Num_Runs']:
            if cat1['Name'] < cat2['Name']:
                ord = True
            else: ord = False
        else: ord = False
    else: ord = False
    return ord

def cmpReq5(cat1, cat2):
    if len(cat1['Record_Date_0']) > 1 and len(cat2['Record_Date_0']) > 1:
        r1 = datetime.strptime(cat1['Record_Date_0'], '%Y-%m-%d %H:%M:%S')
        r2 = datetime.strptime(cat2['Record_Date_0'], '%Y-%m-%d %H:%M:%S')
        if r1 > r2:
            ord = True
        elif r1 == r2:
            if int(cat1['Num_Runs']) > int(cat2['Num_Runs']): #Esta poniendo los más primero
                ord = True
            elif cat1['Num_Runs'] == cat2['Num_Runs']:
                if cat1['Name'] < cat2['Name']:
                    ord = True
                else: ord = False
            else: ord = False
        else: ord = False
    else: ord = False
    return ord

# Requerimientos

def juegosRecientesPlataforma(catalog, platform, fecha_i, fecha_f):
    total, total_rango, total_fechas, l_dates = 0, 0, 0, lt.newList("ARRAY_LIST")
    inicial = datetime.strptime(fecha_i, '%Y-%m-%d')
    final = datetime.strptime(fecha_f, '%Y-%m-%d')
    plat = mp.get(catalog['Platforms'], platform)
    if plat:
        info_plat =  me.getValue(plat)
        total = info_plat["M_Count"]
        dates = om.values(info_plat["Map"], final, inicial)
        total_fechas = listSize(dates)
        for date in lt.iterator(dates):
            if date["G_Count"] > 1: mg.sort(date["Games"], cmpReq1)
            lt.addLast(l_dates, date)
            total_rango += date["G_Count"]
    return total, total_rango, total_fechas, l_dates

def registrosMejorTiempo(catalog, player):
    total_r, n_runs, l_player = 0, 0, lt.newList("ARRAY_LIST")
    play = mp.get(catalog['Players_0'], player)
    if play:
        info_play =  me.getValue(play)
        total_r, n_runs = info_play["R_Count"], info_play["Num_Runs"]
        records = om.valueSet(info_play["Map"])
        total_r = listSize(records)
        for record in lt.iterator(records):
            if record["T_Count"] > 1: mg.sort(record["Records"], cmpReq2)
            for r in lt.iterator(record["Records"]):
                lt.addLast(l_player, r)
    return total_r, n_runs, l_player

def registrosDuracionIntentos(catalog, runs_i, runs_f):
    total, l_time = 0, lt.newList("ARRAY_LIST")
    registros = om.values(catalog['Num_Runs'], float(runs_i), float(runs_f))
    total_rango = listSize(registros)
    for registro in lt.iterator(registros):
        if registro["C_Count"] > 1: mg.sort(registro["Categories"], cmpReq3)
        lt.addLast(l_time, registro)
        total += registro["C_Count"]
    return total, total_rango, l_time

def registrosDuracionFechas(catalog, fecha_i, fecha_f):
    total, l_time = 0, lt.newList("ARRAY_LIST")
    inicial = datetime.strptime(fecha_i, '%Y-%m-%d %H:%M:%S')
    final = datetime.strptime(fecha_f, '%Y-%m-%d %H:%M:%S')
    times = om.values(catalog["Record_Date_0"], final, inicial)
    total_rango = listSize(times)
    for time in lt.iterator(times):
        if time["C_Count"] > 1: mg.sort(time["Categories"], cmpReq4)
        lt.addLast(l_time, time)
        total += time["C_Count"]
    return total, total_rango, l_time

def registrosRecientesTiempos(catalog, tiempo_i, tiempo_f):
    total, l_time = 0, lt.newList("ARRAY_LIST")
    times = om.values(catalog['Time_0'], float(tiempo_i), float(tiempo_f))
    total_rango = listSize(times)
    for time in lt.iterator(times):
        if time["C_Count"] > 1: mg.sort(time["Categories"], cmpReq5)
        lt.addLast(l_time, time)
        total += time["C_Count"]
    return total, total_rango, l_time

def histogramaTiemposAño(catalog, año_i, año_f, bins, levels, prop):
    total_c, total_i, hist = 0, 0, lt.newList("ARRAY_LIST")
    map_prop = om.newMap(omaptype='BST', comparefunction=cmpMenorMayor)
    years = om.values(catalog['Years'], int(año_i), int(año_f))
    for year in lt.iterator(years):
        total_c += year["C_Count"]
        properties = year["Properties"][prop]
        if prop == ("Time_1" or "Time_2"):
            total_i += properties["Count_1"]
            properties = properties["Times_1"]
        else: total_i = total_c
        for property in properties:
            putProperty(map_prop, property)
    mini, maxi = om.minKey(map_prop), om.maxKey(map_prop)
    hist = getIntervals(mini, maxi, map_prop, hist, int(bins), int(levels), prop)
    return total_c, total_i, mini, maxi, hist

def juegosMasRentables(catalog, platform):
    total_g, total_p, l_games = 0, 0, lt.newList("ARRAY_LIST")
    map_games = om.newMap(omaptype='BST', comparefunction=cmpMayorMenor)
    plat = mp.get(catalog['Platforms_2'], platform)
    if plat:
        info_plat =  me.getValue(plat)
        total_g, total_p, unique = info_plat["G_Count"], info_plat["pt"], info_plat["Unique"]
        dict_games = mp.valueSet(info_plat["Map"])
        for dict_game in lt.iterator(dict_games):
            info_game, gt, b_time_avg = dict_game["Info_game"], dict_game["gt"], dict_game["B_Time_Avg"]
            if len(b_time_avg) > 0:
                year = int(me.getValue(mp.get(catalog["Game_Id"], info_game["Game_Id"]))["Year"])
                total_runs = int(info_game["Total_Runs"])
                calculateStreamRevenue(info_game, year, total_runs, b_time_avg, gt, total_p)
                putInfoGame(map_games, info_game)
        games = om.valueSet(map_games)
        for game in lt.iterator(games):
            for g in lt.iterator(game):
                lt.addLast(l_games, g)
    return total_g, total_p, unique, l_games

def distribRecordsContinente(catalog):

    return
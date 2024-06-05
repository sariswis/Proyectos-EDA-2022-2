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

def printMenu():
    print("*******************************************")
    print("Bienvenido")
    print("0- Crear catálogo")
    print("1- Cargar información en el catálogo")
    print("2- Los videojuegos en un rango para una plataforma")
    print("3- 5 registros con menor tiempo para un jugador")
    print("4- Registros de más veloces en un rango de intentos")
    print("5- Registros de más lentos en un rango de fechas")
    print("6- Registros más recientes en un rango de tiempos récord")
    print("7- Histograma de tiempos para un rango de años")
    print("8- Top N de videojuegos más rentables para transmitir")
    print("9- Distribución de récords por continente")
    print("10- Salir")
    print("*******************************************")

def printLoad(s_games, s_categories, l_games, l_categories, sample):
    print("\nTotal videoguegos cargados:", s_games, "\nTotal registros cargados:", s_categories)
    print("\nLos primeros y últimos", sample, "juegos ordenados son:")
    table_g = [["Game_Id", "Name", "Genres", "Platforms", "Total_Runs", "Release_Date"]]
    i = 1 
    while i <= sample: 
        game = lt.getElement(l_games, i) 
        table_g.append([game["Game_Id"], game["Name"], game["Genres"], game["Platforms"], game["Total_Runs"], game["Release_Date"]])
        i += 1
    i = s_games - sample + 1
    while i <= s_games: 
        game = lt.getElement(l_games, i) 
        table_g.append([game["Game_Id"], game["Name"], game["Genres"], game["Platforms"], game["Total_Runs"], game["Release_Date"]])
        i += 1
    print(tabulate(table_g, tablefmt="grid", colalign=("left",), maxcolwidths=[7,15,15,30,10,15]))
    print("\nLos primeros y últimos", sample, "registros ordenados son:")
    table_c = [["Game_Id", "Name", "Category", "Subcategory", "Players_0", "Country_0", "Time_0", "Record_Date_0"]]
    i = 1 
    while i <= sample: 
        category = lt.getElement(l_categories, i) 
        table_c.append([category["Game_Id"], category["Name"], category["Category"], category["Subcategory"], category["Players_0"], category["Country_0"], category["Time_0"], category["Record_Date_0"]])
        i += 1
    i = s_categories - sample + 1
    while i <= s_categories: 
        category = lt.getElement(l_categories, i) 
        table_c.append([category["Game_Id"], category["Name"], category["Category"], category["Subcategory"], category["Players_0"], category["Country_0"], category["Time_0"], category["Record_Date_0"]])
        i += 1
    print(tabulate(table_c, tablefmt="grid", colalign=("left",), maxcolwidths=[7,15,12,12,10,10,10,25]), "\n")

def printReq1(total, total_rango, total_fechas, l_dates, platf, sample):
    print("\nTotal videojuegos en", platf + ":", total, "\nTotal videojuegos en rango:", total_rango, "\nTotal fechas en rango:", total_fechas)
    table, table2 = [["Release Date", "Count", "Details"]], [["Release Date", "Count", "Details"]]
    if 0 < total_rango <= sample*2:
        print("\nLos", total_rango, "juegos más recientes son:")
        for date in lt.iterator(l_dates):
            table_g = [["Name", "Abbreviation", "Genres", "Platforms", "Total_Runs"]]
            for game in lt.iterator(date["Games"]):
                table_g.append([game["Name"], game["Abbreviation"], game["Genres"], game["Platforms"], game["Total_Runs"]])
            table.append([date["Date"], date["G_Count"], tabulate(table_g, tablefmt="grid", maxcolwidths=[15,15,10,20,10])])
    elif total_rango > 0:
        print("\nLos", sample*2, "juegos más recientes son:")
        i = 1 
        while i <= sample:
            date = lt.getElement(l_dates, i)
            table_g = [["Name", "Abbreviation", "Genres", "Platforms", "Total_Runs"]]
            for game in lt.iterator(date["Games"]):
                table_g.append([game["Name"], game["Abbreviation"], game["Genres"], game["Platforms"], game["Total_Runs"]])
            table.append([date["Date"], date["G_Count"], tabulate(table_g, tablefmt="grid", maxcolwidths=[15,15,10,20,10])])
            i += 1
        i = total_fechas - sample + 1
        while i <= total_fechas: 
            date = lt.getElement(l_dates, i)
            table_g = [["Name", "Abbreviation", "Genres", "Platforms", "Total_Runs"]]
            for game in lt.iterator(date["Games"]): 
                table_g.append([game["Name"], game["Abbreviation"], game["Genres"], game["Platforms"], game["Total_Runs"]])
            table2.append([date["Date"], date["G_Count"], tabulate(table_g, tablefmt="grid", maxcolwidths=[15,15,10,20,10])])
            i += 1
    print(tabulate(table, tablefmt="grid", maxcolwidths=[15,10]), "\n")
    if len(table2) > 1: print(tabulate(table2, tablefmt="grid", maxcolwidths=[15,10]), "\n")

def printReq2(total_r, n_runs, l_player, player, sample):
    print("\nRegistros de", player, "con el mejor tiempo:", total_r, "\nNúmero de intentos realizados:", n_runs)
    table = [["Time_0", "Record_Date_0", "Name", "Players_0", "Country_0", "Num_Runs", "Category", "Subcategory"]]
    i = 0 
    for category in lt.iterator(l_player):
        table.append([category["Time_0"], category["Record_Date_0"], category["Name"], category["Players_0"], category["Country_0"], category["Num_Runs"], category["Category"], category["Subcategory"]])
        i += 1
        if i == sample: break
    print(tabulate(table, tablefmt="grid", maxcolwidths=[10,25,15,10,10,9,12,12]), "\n")

def printReq3(total, total_rango, l_runs, runs_i, runs_f, sample):
    print("\nRegistros entre", runs_i, "y", runs_f + ":", total)
    table, table2 = [["Num_Runs", "Count", "Details"]], [["Num_Runs", "Count", "Details"]]
    if 0 < total_rango <= sample*2:
        print("\nLos", total, "registros ordenados son:")
        for run in lt.iterator(l_runs):
            table_c = [["Time_0", "Record_Date_0", "Name", "Category", "Subcategory", "Players_0", "Country_0"]]
            j = 1
            for category in lt.iterator(run["Categories"]):
                if (j <= sample) or ((run["C_Count"] - sample + 1) <= j <= run["C_Count"]): 
                    table_c.append([category["Time_0"], category["Record_Date_0"], category["Name"], category["Category"], category["Subcategory"], category["Players_0"], category["Country_0"]])
                j += 1
            table.append([run["Num_Runs"], run["C_Count"], tabulate(table_c, tablefmt="grid", maxcolwidths=[9,25,15,12,12,10,10])])
    elif total_rango > 0:
        print("\nLos", sample*2, "registros ordenados son:")
        i = 1 
        while i <= sample:
            run = lt.getElement(l_runs, i)
            table_c = [["Time_0", "Record_Date_0", "Name", "Category", "Subcategory", "Players_0", "Country_0"]]
            j = 1
            for category in lt.iterator(run["Categories"]):
                if (j <= sample) or ((run["C_Count"] - sample + 1) <= j <= run["C_Count"]): 
                    table_c.append([category["Time_0"], category["Record_Date_0"], category["Name"], category["Category"], category["Subcategory"], category["Players_0"], category["Country_0"]])
                j += 1
            table.append([run["Num_Runs"], run["C_Count"], tabulate(table_c, tablefmt="grid", maxcolwidths=[9,25,15,12,12,10,10])])
            i += 1
        i = total_rango - sample + 1
        while i <= total_rango: 
            run = lt.getElement(l_runs, i)
            table_c = [["Time_0", "Record_Date_0", "Name", "Category", "Subcategory", "Players_0", "Country_0"]]
            j = 1
            for category in lt.iterator(run["Categories"]):
                if (j <= sample) or ((run["C_Count"] - sample + 1) <= j <= run["C_Count"]): 
                    table_c.append([category["Time_0"], category["Record_Date_0"], category["Name"], category["Category"], category["Subcategory"], category["Players_0"], category["Country_0"]])
                j += 1
            table2.append([run["Num_Runs"], run["C_Count"], tabulate(table_c, tablefmt="grid", maxcolwidths=[9,25,15,12,12,10,10])])
            i += 1
    print(tabulate(table, tablefmt="grid", maxcolwidths=[10,10]), "\n")
    if len(table2) > 1: print(tabulate(table2, tablefmt="grid", maxcolwidths=[10,10]), "\n")

def printReq4(total, total_rango, l_dates, fecha_i, fecha_f, sample):
    print("\nRegistros entre", fecha_i, "y", fecha_f + ":", total)
    table, table2 = [["Record_Date_0", "Count", "Details"]], [["Record_Date_0", "Count", "Details"]]
    if 0 < total_rango <= sample*2:
        print("\nLos", total, "registros ordenados son:")
        for date in lt.iterator(l_dates):
            table_c = [["Time_0", "Num_Runs", "Name", "Category", "Subcategory", "Players_0", "Country_0"]]
            for category in lt.iterator(date["Categories"]):
                table_c.append([category["Time_0"], category["Num_Runs"], category["Name"], category["Category"], category["Subcategory"], category["Players_0"], category["Country_0"]])
            table.append([date["Date"], date["C_Count"], tabulate(table_c, tablefmt="grid", maxcolwidths=[10,9,15,12,12,10,10])])
    elif total_rango > 0:
        print("\nLos", sample*2, "registros ordenados son:")
        i = 1 
        while i <= sample:
            date = lt.getElement(l_dates, i)
            table_c = [["Time_0", "Num_Runs", "Name", "Category", "Subcategory", "Players_0", "Country_0"]]
            for category in lt.iterator(date["Categories"]):
                table_c.append([category["Time_0"], category["Num_Runs"], category["Name"], category["Category"], category["Subcategory"], category["Players_0"], category["Country_0"]])
            table.append([date["Date"], date["C_Count"], tabulate(table_c, tablefmt="grid", maxcolwidths=[10,9,15,12,12,10,10])])
            i += 1
        i = total_rango - sample + 1
        while i <= total_rango: 
            date = lt.getElement(l_dates, i)
            table_c = [["Time_0", "Num_Runs", "Name", "Category", "Subcategory", "Players_0", "Country_0"]]
            for category in lt.iterator(date["Categories"]):
                table_c.append([category["Time_0"], category["Num_Runs"], category["Name"], category["Category"], category["Subcategory"], category["Players_0"], category["Country_0"]])
            table2.append([date["Date"], date["C_Count"], tabulate(table_c, tablefmt="grid", maxcolwidths=[10,9,15,12,12,10,10])])
            i += 1
    print(tabulate(table, tablefmt="grid", maxcolwidths=[25,10]), "\n")
    if len(table2) > 1: print(tabulate(table2, tablefmt="grid", maxcolwidths=[25,10]), "\n")

def printReq5(total, total_rango, l_time, tiempo_i, tiempo_f, sample):
    print("\nRegistros entre", tiempo_i, "y", tiempo_f + ":", total)
    table, table2 = [["Time_0", "Count", "Details"]],  [["Time_0", "Count", "Details"]]
    if 0 < total_rango <= sample*2:
        print("\nLos", total, "registros ordenados son:")
        for time in lt.iterator(l_time):
            table_c = [["Record_Date_0", "Num_Runs", "Name", "Category", "Subcategory", "Players_0", "Country_0"]]
            for category in lt.iterator(time["Categories"]):
                table_c.append([category["Record_Date_0"], category["Num_Runs"], category["Name"], category["Category"], category["Subcategory"], category["Players_0"], category["Country_0"]])
            table.append([time["Time"], time["C_Count"], tabulate(table_c, tablefmt="grid", maxcolwidths=[25,9,15,12,12,10,10])])
    elif total_rango > 0:
        print("\nLos", sample*2, "registros ordenados son:")
        i = 1 
        while i <= sample:
            time = lt.getElement(l_time, i)
            table_c = [["Record_Date_0", "Num_Runs", "Name", "Category", "Subcategory", "Players_0", "Country_0"]]
            for category in lt.iterator(time["Categories"]):
                table_c.append([category["Record_Date_0"], category["Num_Runs"], category["Name"], category["Category"], category["Subcategory"], category["Players_0"], category["Country_0"]])
            table.append([time["Time"], time["C_Count"], tabulate(table_c, tablefmt="grid", maxcolwidths=[25,9,15,12,12,10,10])])
            i += 1
        i = total_rango - sample + 1
        while i <= total_rango: 
            time = lt.getElement(l_time, i)
            table_c = [["Record_Date_0", "Num_Runs", "Name", "Category", "Subcategory", "Players_0", "Country_0"]]
            for category in lt.iterator(time["Categories"]):
                table_c.append([category["Record_Date_0"], category["Num_Runs"], category["Name"], category["Category"], category["Subcategory"], category["Players_0"], category["Country_0"]])
            table2.append([time["Time"], time["C_Count"], tabulate(table_c, tablefmt="grid", maxcolwidths=[25,9,15,12,12,10,10])])
            i += 1
    print(tabulate(table, tablefmt="grid", maxcolwidths=[10,10]), "\n")
    if len(table2) > 1: print(tabulate(table2, tablefmt="grid", maxcolwidths=[10,10]), "\n")

def printReq6(total_c, total_i, mini, maxi, hist, bins, levels, prop):
    print("\nRegistros consultados:", total_c, "\nRegistros incluidos en el conteo:", total_i)
    print("Mínimo valor:", mini, "\nMáximo valor:", maxi)
    print("Histograma de", prop, "con", bins, "bins y nivel", levels)
    table = [["Bin", "Count", "Lvl", "Marks"]]
    for row in lt.iterator(hist):
        table.append([row["Bin"], row["Count"], row["Level"], row["Level"]*"*"])
    print(tabulate(table, tablefmt="grid"))
    print("NOTA: Cada '*' representa", levels, "intentos.")

def printReq7(total_g, total_p, unique, l_games, platf, top):
    print("Récords en", platf + ":", total_p, "\nCantidad de juegos en plataforma:", total_g, "\nJuegos únicos en plataforma:", unique)
    print("\nLos", top, "juegos ordenados son:")
    table = [["N°", "Name", "Release_Date", "Platforms", "Genres", "Stream_Revenue", "Market_Share", "Time_Avg", "Total_Runs"]]
    i = 1
    for game in lt.iterator(l_games):
        table.append([i, game["Name"], game["Release_Date"], game["Platforms"], game["Genres"], round(game["Stream_Revenue"], 2), round(game["Market_Share"], 2), round(game["Time_Avg"], 2), game["Total_Runs"]])
        i += 1
        if i == int(top) + 1: break
    print(tabulate(table, tablefmt="grid", maxcolwidths=[5,15,15,20,15,15,15,10,10]))    

def printReq8():
    print()

def castBoolean(value):
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

def printDelta(delta):
    if len(delta) == 2:
        print("Tiempo [ms]: ", f"{delta[0]:.3f}", "||", "Memoria [kB]: ", f"{delta[1]:.3f}", "\n")
    else:
        print("Tiempo [ms]: ", f"{delta[0]:.3f}", "\n")

control, tamaño = controller.newController(), "small"

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input("Seleccione una opción para continuar\n> ")
    inp = int(inputs[0:2])
    if inp == 0:
        option = input("\nElija un tamaño de muestra: \n1- small \n2- 5pct \n3- 10pct \n4- 20pct \n5- 30pct \n6- 50pct \n7- 80pct \n8- large\n")
        opt = int(option[0])
        if opt == 2: tamaño = "5pct"
        elif opt == 3: tamaño = "10pct"
        elif opt == 4: tamaño = "20pct"
        elif opt == 5: tamaño = "30pct"
        elif opt == 6: tamaño = "50pct"
        elif opt == 7: tamaño = "80pct"
        elif opt == 8: tamaño = "large"
        print("\nHa elegido ", tamaño, "\n")

    elif inp == 1:
        print("Cargando información de los archivos...")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        s_games, s_categories, l_games, l_categories, delta = controller.loadData(control, tamaño, mem)
        printLoad(s_games, s_categories, l_games, l_categories, 3)
        printDelta(delta)

    elif inp == 2:
        platf = input("Plataforma a buscar: ")
        fecha_i = input("Límite inferior: ")
        fecha_f = input("Límite superior: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total, total_rango, total_fechas, l_dates, delta = controller.juegosRecientesPlataforma(control, platf, fecha_i, fecha_f, mem)
        printReq1(total, total_rango, total_fechas, l_dates, platf, 3)
        printDelta(delta)

    elif inp == 3:
        player = input("Nombre del jugador: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total_r, n_runs, l_player, delta = controller.registrosMejorTiempo(control, player, mem)
        printReq2(total_r, n_runs, l_player, player, 5)
        printDelta(delta)

    elif inp == 4:
        runs_i = input("Límite inferior: ")
        runs_f = input("Límite superior: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total, total_rango, l_runs, delta = controller.registrosDuracionIntentos(control, runs_i, runs_f, mem)
        printReq3(total, total_rango, l_runs, runs_i, runs_f, 3)
        printDelta(delta)

    elif inp == 5:
        fecha_i = input("Límite inferior: ")
        fecha_f = input("Límite superior: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total, total_rango, l_dates, delta = controller.registrosDuracionFechas(control, fecha_i, fecha_f, mem)
        printReq4(total, total_rango, l_dates, fecha_i, fecha_f, 3)
        printDelta(delta)

    elif inp == 6:
        tiempo_i = input("Límite inferior: ")
        tiempo_f = input("Límite superior: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total, total_rango, l_time, delta = controller.registrosRecientesTiempos(control, tiempo_i, tiempo_f, mem)
        printReq5(total, total_rango, l_time, tiempo_i, tiempo_f, 3)
        printDelta(delta)

    elif inp == 7:
        año_i = input("Límite inferior: ")
        año_f = input("Límite superior: ")
        bins = input("Segmentos (N): ")
        levels = input("Niveles (x): ")
        print("Elija una opción: Time_0, Time_1, Time_2, Time_Avg o Num_Runs")
        prop = input("Propiedad: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total_c, total_i, mini, maxi, hist, delta = controller.histogramaTiemposAño(control, año_i, año_f, bins, levels, prop, mem)
        printReq6(total_c, total_i, mini, maxi, hist, bins, levels, prop)
        printDelta(delta)

    elif inp == 8:
        platf = input("Plataforma a buscar: ")
        top = input("Top (N): ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total_g, total_p, unique, l_games, delta = controller.juegosMasRentables(control, platf, mem)
        printReq7(total_g, total_p, unique, l_games, platf, top)
        printDelta(delta)

    elif inp == 9:
        
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        data, delta = controller.distribRecordsContinente(control, mem)
        printReq8()
        printDelta(delta)

    elif inp == 10:
        sys.exit(0)

    else:
        continue

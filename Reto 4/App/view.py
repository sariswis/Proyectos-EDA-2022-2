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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
assert cf
from tabulate import tabulate
sys.setrecursionlimit(10000000)

def printMenu():
    print("*******************************************")
    print("Bienvenido")
    print("0- Crear catálogo")
    print("1- Cargar información en el catálogo")
    print("2- Camino posible entre estaciones")
    print("3- Camino con menos paradas entre estaciones")
    print("4- Componentes conectados de la Red de rutas")
    print("5- Camino con menor distancia entre dos puntos")
    print("6- Estaciones alcanzables desde origen a conexiones")
    print("7- Camino con menor distancia entre origen y vecindario")
    print("8- Posible camino circular desde origen")
    print("9- Salir")
    print("*******************************************")

def printLoad(t_rutas, t_rutas_e, t_exclusiv, t_trasb, t_vertices, t_arcos, rango, estaciones, sample):
    print("\nEstaciones exclusivas:", t_exclusiv, "\nEstaciones de transbordo:", t_trasb, "\nTotal estaciones:", t_exclusiv + t_trasb)
    print("\nTotal de rutas BUS-ID:", t_rutas, "\nRutas exclusivas:", t_rutas_e, "\nRutas compartidas:", t_arcos - t_rutas_e, "\nTotal de rutas:", t_arcos)
    print("\nTotal de vértices:", t_vertices, "\nTotal de arcos:", t_arcos, "\nRango:", rango)
    print("\nLas primeras", sample, "y últimas estaciones son:")
    table = [["Id", "Longitude", "Latitude", "Neighborhood", "In degree", "Out degree"]]
    i = 0
    for estacion in lt.iterator(estaciones['exclusivas']):
        table.append([estacion['Id'], estacion['Longitude'], estacion['Latitude'], estacion['Neighborhood_Name'], estacion['In degree'], estacion['Out degree']])
        i += 1
        if i == sample: break
    total = lt.size(estaciones['transbordos'])
    i = total - sample + 1
    while i <= total:
        estacion = lt.getElement(estaciones['transbordos'], i)
        table.append([estacion['Id'], estacion['Longitude'], estacion['Latitude'], estacion['Neighborhood_Name'], estacion['In degree'], estacion['Out degree']])
        i += 1
    print(tabulate(table, tablefmt="grid", maxcolwidths=[10,10,10,50,10,10]), "\n")
    
def print12(origen, destino, distancia, ruta):
    if distancia == 0: conteo = True
    else: conteo = False
    if ruta is not None:
        t_estac, t_trasb = st.size(ruta) + 1, 0
        table = [['i', "Origen", "Destino", "Distancia"]]
        i = 1
        while (not st.isEmpty(ruta)):
            estacion = st.pop(ruta)
            table.append([i, estacion['vertexA'], estacion['vertexB'], estacion['weight']])
            if estacion['vertexA'][0:2] == 'T-': t_trasb += 1
            if conteo: distancia += estacion['weight']
            i += 1
        print("\nDistancia total:", distancia, "\nTotal de estaciones:", t_estac)
        print("Total de estaciones exclusivas:", t_estac-t_trasb,"\nTotal de transbordos:", t_trasb)
        print("La ruta entre", origen, "y", destino, "es:")
        print(tabulate(table, tablefmt="grid", maxcolwidths=[10,10,20]), "\n")
    else:
        print('No hay camino')

def print3(total, componentes, sample, sub_sample):
    print("Total SCC:", total)
    table = [["Id", "Conteo", "Estaciones"]]
    i = 0
    for componente in lt.iterator(componentes):
        table2 = []
        j = 0
        for estacion in lt.iterator(componente['Estaciones']):
            if (j <= sub_sample) or ((componente['Conteo'] - sub_sample + 1) <= j <= componente['Conteo']):
                table2.append([estacion])
            j += 1
        table.append([componente['Id'], componente['Conteo'], tabulate(table2, tablefmt="grid", maxcolwidths=[10])])
        i += 1
        if i == sample: break
    print(tabulate(table, tablefmt="grid", maxcolwidths=[10,10]), "\n")

def print4(total, ruta):
    if ruta is not None:
        t_estac, t_trasb, d_ruta = st.size(ruta) - 1, 0, 0
        table = [['i', "Origen", "Destino", "Distancia"]]
        i = 1
        while (not st.isEmpty(ruta)):
            estacion = st.pop(ruta)
            table.append([i, estacion['vertexA'], estacion['vertexB'], estacion['weight']])
            if estacion['vertexA'][0:2] == 'T-': t_trasb += 1
            if estacion['vertexA'] == 'Origen': d_origen = estacion['weight']
            elif estacion['vertexB'] == 'Destino': d_destino = estacion['weight']
            else: d_ruta += estacion['weight']
            i += 1
        print("\nDistancia total:", total, "\nDistancia del origen a la estación:", d_origen) 
        print("Distancia entre estaciones:", d_ruta, "\nDistancia de la estación al destino:", d_destino) 
        print("Total de estaciones:", t_estac, "\nTotal de estaciones exclusivas:", t_estac-t_trasb, "\nTotal de transbordos:", t_trasb)
        print("La ruta entre los dos puntos es:")
        print(tabulate(table, tablefmt="grid", maxcolwidths=[10,10,20]), "\n")
    else:
        print('No hay camino')

def print5(origen, reporte, total):
    i, t_trasb = 1, 0
    table = [['i', 'Conexiones', 'Id', 'Latitude', 'Longitude', 'DistTo']]
    for estacion in lt.iterator(reporte):
        table.append([i, estacion['Conexiones'], estacion['Id'], estacion['Latitude'], estacion['Longitude'], estacion['DistTo']])
        if estacion['Id'][0:2] == 'T-': t_trasb += 1
        i += 1
    print('\nSe encontraron', total, 'estaciones alcanzables desde', origen)
    print("Total de estaciones exclusivas:", total-t_trasb,"\nTotal de estaciones de transbordo:", t_trasb)
    print(tabulate(table, tablefmt="grid"), "\n")

def print6(origen, vecindario, distancia, t_estac, t_trasb, ruta):
    print('\nDistancia total:', distancia, '\nTotal de estaciones:', t_estac)
    print("Total de estaciones exclusivas:", t_estac-t_trasb,"\nTotal de transbordos:", t_trasb)
    print('La ruta entre', origen, 'y', vecindario, 'es:')
    i = 1
    table = [['i', "Origen", 'Barrio Origen', "Destino", 'Barrio Destino', "Distancia"]]
    for estacion in lt.iterator(ruta):
        table.append([i, estacion['vertexA'], estacion['Barrio Origen'], estacion['vertexB'], estacion['Barrio Destino'], estacion['weight']])
        i += 1
    print(tabulate(table, tablefmt="grid"), "\n")

def print7(origen, distancia, t_estac, t_trasb, ruta):
    table = [['i', "Origen", "Destino", "Distancia"]]
    i = 1
    for estacion in lt.iterator(ruta):
        table.append([i, estacion['vertexA'], estacion['vertexB'], estacion['weight']])
        if estacion['vertexA'][0:2] == 'T-': t_trasb += 1
        distancia += estacion['weight']
        i += 1
        t_estac += 1
    if distancia > 0: rta = 'Sí'
    else: rta = 'No'
    print('\n' + rta, 'hay un camino circular desde', origen, '\nDistancia total:', distancia) 
    print('Total de estaciones:', t_estac, "\nTotal de estaciones exclusivas:", t_estac-t_trasb, "\nTotal de transbordos:", t_trasb)
    print(tabulate(table, tablefmt="grid"), "\n")

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

catalog, tamaño = controller.newCatalog(), "large"

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
        if opt == 1: tamaño = "small"
        elif opt == 2: tamaño = "5pct"
        elif opt == 3: tamaño = "10pct"
        elif opt == 4: tamaño = "20pct"
        elif opt == 5: tamaño = "30pct"
        elif opt == 6: tamaño = "50pct"
        elif opt == 7: tamaño = "80pct"
        else: tamaño = "large"
        print("\nHa elegido ", tamaño, "\n")

    elif inp == 1:
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        t_rutas, t_rutas_e, t_exclusiv, t_trasb, t_vertices, t_arcos, rango, estaciones, delta = controller.loadData(catalog, tamaño, mem)
        printLoad(t_rutas, t_rutas_e, t_exclusiv, t_trasb, t_vertices, t_arcos, rango, estaciones, 5)
        printDelta(delta)

    elif inp == 2:
        origen = input("Estación origen: ")
        destino = input("Estación destino: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        distancia, ruta, delta = controller.caminoPosible(catalog, origen, destino, mem)
        print12(origen, destino, distancia, ruta)
        printDelta(delta)

    elif inp == 3:
        origen = input("Estación origen: ")
        destino = input("Estación destino: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        distancia, ruta, delta = controller.caminoMenosParadas(catalog, origen, destino, mem)
        print12(origen, destino, distancia, ruta)
        printDelta(delta)

    elif inp == 4:
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total, componentes, delta = controller.componentesConectados(catalog, mem)
        print3(total, componentes, 5, 3)
        printDelta(delta)

    elif inp == 5:
        lon_origen = input("Longitud de origen: ")
        lat_origen = input("Latitud de origen: ")
        lon_destino = input("Longitud del destino: ")
        lat_destino = input("Latitud del destino: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        total, ruta, delta = controller.caminoDosPuntos(catalog, lon_origen, lat_origen, lon_destino, lat_destino, mem)
        print4(total, ruta)
        printDelta(delta)

    elif inp == 6:
        origen = input("Estación origen: ")
        conexiones = int(input("Número de conexiones: "))
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        reporte, total, delta = controller.estacionesAlcanzables(catalog, origen, conexiones, mem)
        print5(origen, reporte, total)
        printDelta(delta)

    elif inp == 7:
        origen = input("Estación origen: ")
        vecindario = input("Vecindario: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        distancia, t_estac, t_trasb, ruta, delta = controller.caminoEstacionVecindario(catalog, origen, vecindario, mem)
        print6(origen, vecindario, distancia, t_estac, t_trasb, ruta)
        printDelta(delta)

    elif inp == 8:
        origen = input("Estación origen: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = castBoolean(input("Respuesta: "))
        distancia, t_estac, t_trasb, ruta, delta = controller.caminoCircular(catalog, origen, mem)
        print7(origen, distancia, t_estac, t_trasb, ruta)
        printDelta(delta)

    elif inp == 9:
        sys.exit(0)

    else:
        continue


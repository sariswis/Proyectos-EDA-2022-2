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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr
from DISClib.ADT import stack as st
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mg
from DISClib.Algorithms.Graphs import scc as ssc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import cycles as cy
from haversine import Unit, haversine
assert cf

# Construccion de modelos

def newCatalog():
    catalog = {}
    catalog['totals'] = {'rutas':[], 'exclusivas':0, 'transbordos':0, 'rutas_e':0, 'latitudes':[], 'longitudes':[]}
    catalog['stations'] = {'exclusivas':lt.newList('ARRAY_LIST'), 'transbordos':lt.newList('ARRAY_LIST')}
    catalog['stops'] = mp.newMap(numelements=5730, maptype='PROBING')
    catalog['neighborhoods'] = mp.newMap(numelements=74, maptype='PROBING')
    catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST', directed=True, size=5730)
    catalog['simple'] = gr.newGraph(datastructure='ADJ_LIST', directed=True, size=5730)
    return catalog

# Funciones para agregar informacion al catalogo

def processStop(totals, stations, stops, neighborhoods, connections, simple, stop):
    vertex = stop['Code'] + stop['Bus_Stop'].replace('BUS', "")
    addTotals(totals, stop, stop['Bus_Stop'])
    addStop(stops, stations, neighborhoods, vertex, stop, True)
    if not gr.containsVertex(connections, vertex):
        gr.insertVertex(connections, vertex)
        gr.insertVertex(simple, vertex)
    if stop['Transbordo'] == 'S':
        trasb = 'T-' + stop['Code']
        if not gr.containsVertex(connections, trasb):
            gr.insertVertex(connections, trasb)
            gr.insertVertex(simple, trasb)
            totals['transbordos'] += 1
        addEdge(connections, vertex, trasb, 0)
        addEdge(simple, vertex, trasb, 1)
        addStop(stops, stations, neighborhoods, trasb, stop, False)
    else: totals['exclusivas'] += 1

def processEdge(totals, stops, connections, simple, edge):
    origin = edge['Code'] + edge['Bus_Stop'].replace('BUS', "")
    destination = edge['Code_Destiny'] + edge['Bus_Stop'].replace('BUS', "")
    exist_orig, exist_dest = mp.get(stops, origin), mp.get(stops, destination)
    i_origin, i_destination = me.getValue(exist_orig), me.getValue(exist_dest)
    l_origin, l_destination = (i_origin['Latitude'], i_origin['Longitude']), (i_destination['Latitude'], i_destination['Longitude'])
    distance = haversine(l_origin, l_destination)
    addEdge(connections, origin, destination, distance)
    addEdge(simple, origin, destination, 1)
    totals['rutas_e'] += 1

def addStop(stops, stations, neighborhoods, vertex, stop, bool):
    stop_info = {'Id':vertex, 'Longitude':float(stop['Longitude']), 'Latitude':float(stop['Latitude']), 'Neighborhood_Name':stop['Neighborhood_Name'], "Transbordo":stop['Transbordo']}
    mp.put(stops, vertex, stop_info)
    if bool:
        lt.addLast(stations['exclusivas'], stop_info)
        entry = mp.get(neighborhoods, stop['Neighborhood_Name'])
        if entry is None:
            value = lt.newList('ARRAY_LIST')
            mp.put(neighborhoods, stop['Neighborhood_Name'], value)
        else:
            value = me.getValue(entry)
        lt.addLast(value, vertex)
    else: lt.addLast(stations['transbordos'], stop_info)

def addEdge(graph, origin, destination, distance):
    edge = gr.getEdge(graph, origin, destination)
    if edge is None:
        gr.addEdge(graph, origin, destination, distance)
        gr.addEdge(graph, destination, origin, distance)

def addTotals(totals, stop, ruta):
    totals['latitudes'].append(stop['Latitude'])
    totals['longitudes'].append(stop['Longitude'])
    if ruta not in totals['rutas']: totals['rutas'].append(ruta) 

def addSCC(idscc, components, estacion):
    component = me.getValue(mp.get(idscc, estacion))
    entry = mp.get(components, component)
    if entry is None:
        value = {'Id':component, 'Conteo':0, 'Estaciones':lt.newList('ARRAY_LIST')}
        mp.put(components, component, value)
    else:
        value = me.getValue(entry)
    lt.addLast(value['Estaciones'], estacion)
    value['Conteo'] += 1

def addPoints(stops, connections, lon_origen, lat_origen, lon_destino, lat_destino):
    distances_o, distances_d = om.newMap(omaptype='BST'), om.newMap(omaptype='BST')
    l_origin, l_destination = (float(lat_origen), float(lon_origen)), (float(lat_destino), float(lon_destino))
    vertices = gr.vertices(connections)
    for vertice in lt.iterator(vertices):
        i_vertice = me.getValue(mp.get(stops, vertice))
        l_vertice = (i_vertice['Latitude'], i_vertice['Longitude'])
        d_o = haversine(l_origin, l_vertice)
        d_d = haversine(l_vertice, l_destination)
        addDistance(distances_o, d_o, vertice)
        addDistance(distances_d, d_d, vertice)
    gr.insertVertex(connections, "Origen")
    gr.insertVertex(connections, "Destino")
    min_dist_o, min_dist_d = om.minKey(distances_o), om.minKey(distances_d)
    min_vert_o, min_vert_d = me.getValue(om.get(distances_o, min_dist_o)), me.getValue(om.get(distances_d, min_dist_d))
    for vertice in lt.iterator(min_vert_o):
        gr.addEdge(connections, "Origen", vertice, min_dist_o)
    for vertice in lt.iterator(min_vert_d):
        gr.addEdge(connections, vertice, "Destino", min_dist_d)

def addDistance(map, distance, vertice):
    entry = om.get(map, distance)
    if entry is None:
        value = lt.newList('ARRAY_LIST')
        om.put(map, distance, value)
    else:
        value = me.getValue(entry)
    lt.addLast(value, vertice)

def cleanPoints(connections):
    gr.removeVertex(connections, "Origen")
    gr.removeVertex(connections, "Destino")

def addAdyacents(stops, connections, reporte, vertice, anterior, estaciones, i, num, dist):
    if i <= num: 
        adyacentes = gr.adjacents(connections, vertice)
        for adyac in lt.iterator(adyacentes):
            if adyac != anterior:
                info = me.getValue(mp.get(stops, adyac))
                dist += gr.getEdge(connections, vertice, adyac)['weight']
                estacion = {'Conexiones':i, 'Id':adyac, 'Latitude':info['Latitude'], 'Longitude':info['Longitude'], 'DistTo':dist}
                lt.addLast(reporte, estacion)
                mp.put(estaciones, adyac, None)
                addAdyacents(stops, connections, reporte, adyac, vertice, estaciones, i+1, num, dist)

# Funciones de comparación

def orderSCC(c1, c2):
    if c1['Conteo'] > c2['Conteo']: 
        ord = True
    elif c1['Conteo'] == c2['Conteo']:
        if c1['Id'] < c2['Id']: 
            ord = True
        else:
            ord = False
    else: ord = False
    return ord

# Requerimientos

def caminoPosible(catalog, origen, destino):
    distancia, ruta = 0, lt.newList('ARRAY_LIST')
    search = bfs.BreadhtFisrtSearch(catalog['connections'], origen)
    if bfs.hasPathTo(search, destino):
        stops = bfs.pathTo(search, destino)
        i, total = 1, lt.size(stops)
        while i < total:
            vertexA, vertexB = lt.getElement(stops, i), lt.getElement(stops, i + 1)
            estacion = gr.getEdge(catalog['connections'], vertexB, vertexA)
            lt.addLast(ruta, estacion)
            i += 1
    return distancia, ruta

def caminoMenosParadas(catalog, origen, destino):
    distancia, ruta = 0, lt.newList('ARRAY_LIST')
    search = djk.Dijkstra(catalog['simple'], origen)
    if djk.hasPathTo(search, destino):
        stops = djk.pathTo(search, destino)
        for stop in lt.iterator(stops):
            estacion = gr.getEdge(catalog['connections'], stop['vertexA'], stop['vertexB'])
            lt.addLast(ruta, estacion)
    return distancia, ruta

def componentesConectados(catalog):
    d_componentes = mp.newMap(numelements=5730, maptype='PROBING')
    rta = ssc.KosarajuSCC(catalog['connections'])
    total = ssc.connectedComponents(rta)
    catalog['SCC stations'] = rta["idscc"]
    idscc = mp.keySet(rta["idscc"])
    for estacion in lt.iterator(idscc):
        addSCC(rta["idscc"], d_componentes, estacion)
    componentes = mg.sort(mp.valueSet(d_componentes), orderSCC)
    catalog['Components'] = d_componentes
    return total, componentes

def caminoDosPuntos(catalog, lon_origen, lat_origen, lon_destino, lat_destino):
    total, ruta = 0, lt.newList('ARRAY_LIST')
    addPoints(catalog['stops'], catalog['connections'], lon_origen, lat_origen, lon_destino, lat_destino)
    search = djk.Dijkstra(catalog['connections'], 'Origen')
    if djk.hasPathTo(search, 'Destino'):
        ruta = djk.pathTo(search, 'Destino')
        total = djk.distTo(search, 'Destino')
    cleanPoints(catalog['connections'])
    return total, ruta

def estacionesAlcanzables(catalog, origen, conexiones):
    reporte = lt.newList("ARRAY_LIST")
    estaciones = mp.newMap(numelements=20, maptype='PROBING')
    addAdyacents(catalog['stops'], catalog['connections'], reporte, origen, None, estaciones, 1, conexiones, 0)
    total = mp.size(estaciones)
    return reporte, total

def caminoEstacionVecindario(catalog, origen, vecindario):
    distancia, t_estac, t_trasb, ruta, distances = 0, 1, 0, lt.newList("ARRAY_LIST"), om.newMap(omaptype='BST')
    neighborhood = mp.get(catalog['neighborhoods'], vecindario)
    if neighborhood:
        search = djk.Dijkstra(catalog['connections'], origen)
        estaciones = me.getValue(neighborhood)
        for estacion in lt.iterator(estaciones):
            if djk.hasPathTo(search, estacion):
                addDistance(distances, djk.distTo(search, estacion), estacion) 
        distancia = om.minKey(distances)      
        menor_estacion = lt.firstElement(me.getValue(om.get(distances, distancia)))
        camino = djk.pathTo(search, menor_estacion)
        while (not st.isEmpty(camino)):
            estacion = st.pop(camino)
            estacion['Barrio Origen'] = me.getValue(mp.get(catalog['stops'], estacion['vertexA']))['Neighborhood_Name']
            estacion['Barrio Destino'] = me.getValue(mp.get(catalog['stops'], estacion['vertexB']))['Neighborhood_Name']
            if estacion['Barrio Origen'] != vecindario:
                if estacion['vertexA'][0:2] == 'T-': t_trasb += 1 
                lt.addLast(ruta, estacion)
                t_estac += 1
    return distancia, t_estac, t_trasb, ruta

def caminoCircular(catalog, origen):
    distancia, t_estac, t_trasb, ruta = 0, 1, 0, lt.newList('ARRAY_LIST')
    scc = gr.newGraph(datastructure='ADJ_LIST', directed=True, size=5760)
    num_scc = me.getValue(mp.get(catalog['SCC stations'], origen))
    estac_scc = me.getValue(mp.get(catalog['Components'], num_scc))['Estaciones']
    print('Creando grafo SCC...')
    for estacion in lt.iterator(estac_scc):
        if not gr.containsVertex(scc, estacion): gr.insertVertex(scc, estacion)
        edges = gr.adjacentEdges(catalog['connections'], estacion)
        for edge in lt.iterator(edges):
            adyac, peso = edge['vertexB'], edge['weight']
            if lt.isPresent(estac_scc, adyac):
                if not gr.containsVertex(scc, adyac): gr.insertVertex(scc, adyac)
                gr.addEdge(scc, estacion, adyac, peso)
    print('Hallando camino circular...')
    search1 = bfs.BreadhtFisrtSearch(scc, origen)
    vertices = gr.vertices(scc)
    mayor_s, mayor_v, path1 = 0, None, None
    for vertice in lt.iterator(vertices):
        path = bfs.pathTo(search1, vertice)
        stops = lt.size(path)
        if stops > mayor_s:
            mayor_v = vertice
            mayor_s = stops
            path1 = path
    search2 = bfs.BreadhtFisrtSearch(scc, mayor_v)
    path2 = bfs.pathTo(search2, origen)
    print('Construyendo camino...')
    i, total = 1, lt.size(path2)
    while i < total:
        vertexA, vertexB = lt.getElement(path2, i), lt.getElement(path2, i + 1)
        estacion = gr.getEdge(scc, vertexA, vertexB)
        lt.addLast(ruta, estacion)
        i += 1
    i, total = 1, lt.size(path1)
    while i < total:
        vertexA, vertexB = lt.getElement(path1, i), lt.getElement(path1, i + 1)
        estacion = gr.getEdge(scc, vertexA, vertexB)
        lt.addLast(ruta, estacion)
        i += 1
    return distancia, t_estac, t_trasb, ruta

# Consulta 

def totals(totals, estaciones, conexiones):
    t_rutas, t_rutas_e = len(totals['rutas']), totals['rutas_e']
    t_exclusiv, t_trasb = totals['exclusivas'], totals['transbordos']
    t_vertices, t_arcos = gr.numVertices(conexiones), gr.numEdges(conexiones)
    min_lat, max_lat = str(min(totals['latitudes'])), str(max(totals['latitudes']))
    min_lon, max_lon = str(min(totals['longitudes'])), str(max(totals['longitudes']))
    rango = "Latitud [" + min_lat + ", " + max_lat + "] Longitud [" + min_lon + ", " + max_lon + "]"
    for estacion in lt.iterator(estaciones['exclusivas']):
        estacion['In degree'] = gr.indegree(conexiones, estacion['Id'])
        estacion['Out degree'] = gr.outdegree(conexiones, estacion['Id'])
    for estacion in lt.iterator(estaciones['transbordos']):
        estacion['In degree'] = gr.indegree(conexiones, estacion['Id'])
        estacion['Out degree'] = gr.outdegree(conexiones, estacion['Id'])
    return t_rutas, t_rutas_e, t_exclusiv, t_trasb, t_vertices, t_arcos, rango, estaciones
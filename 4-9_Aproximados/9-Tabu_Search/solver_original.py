#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

import math
import networkx as nx
import matplotlib.pyplot as mpl
import random
import copy
from Cola import Cola

Point = namedtuple("Point", ['x', 'y'])

def calcula_dis_circuito(circuito, points):
    n = len(circuito)

    distancia = length(points[circuito[0]], points[circuito[-1]])
    for i in range(0, n-1):
        distancia += length(points[circuito[i]], points[circuito[i+1]])

    return distancia

def crea_grafo_completo(points):
    g = nx.Graph()
    nodeCount = len(points)

    for i in range(0, nodeCount):
        g.add_node(i)

    for i in range(0, nodeCount - 1):
        for j in range(i + 1, nodeCount):
            distancia = length(points[i], points[j])
            g.add_edge(i, j, weight=distancia)

    #nx.draw_networkx(g)
    #mpl.show()

    return g

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def christofides(g, points):
    n = g.number_of_nodes()

    S = nx.MultiGraph()
    T = nx.minimum_spanning_tree(g);
    S.add_nodes_from(T.nodes)
    S.add_edges_from(T.edges)

    nbunch = []
    for i in range(0, n):
        if T.degree(i) % 2 == 1:
            nbunch.append(i)

    M = nx.Graph()
    M.add_nodes_from(nbunch)

    for i in range(0, len(nbunch)-1):
        for j in range(i+1, len(nbunch)):
            M.add_edge(nbunch[i],nbunch[j], weight=-(length(points[nbunch[i]], points[nbunch[j]])))

    aristas = nx.max_weight_matching(M, maxcardinality = True)

    for arista in aristas:
        S.add_edge(arista[0], arista[1], weight=length(points[arista[0]], points[arista[1]]))

    aristas = [u for u, v in nx.eulerian_circuit(S)]
    circuito = []

    for arista in aristas:
        if arista not in circuito:
            circuito.append(arista)

    return circuito

def tabu_search(circuito, points):
    aristas = []
    vauxiliar = circuito
    n = len(vauxiliar)

    dis_circuito = calcula_dis_circuito(circuito, points)
    mejor_dis_circuito = dis_circuito
    mejor_circuito = copy.deepcopy(vauxiliar)

    lista_tabu = Cola(n)
    contador = 0
    max_iters = 150
    iter = 0

    while iter < max_iters:
        iter += 1
        divisor = random.randint(1, n-2)
        aux1 = vauxiliar[:divisor]
        aux2 = vauxiliar[divisor:]
        aux2.extend(aux1)

        vauxiliar = aux2

        mejor_par = []
        mayor_mejora = -math.inf
        for i in range(0, n-3):
            for j in range(i+2, n-1):
                rp1 = length(points[vauxiliar[i]], points[vauxiliar[i+1]])
                rp2 = length(points[vauxiliar[j]], points[vauxiliar[j+1]])

                rr = length(points[vauxiliar[i]], points[vauxiliar[j]])
                pp = length(points[vauxiliar[i+1]], points[vauxiliar[j+1]])

                mejora = (rp1 + rp2) - (rr + pp)

                if mejora > mayor_mejora:
                    if not lista_tabu.buscar((vauxiliar[i], vauxiliar[j])):
                        mayor_mejora = mejora
                        mejor_par = [i, j]
                        aristas = (vauxiliar[i], vauxiliar[j])

        lista_tabu.insertar(aristas)

        aux_cir1 = vauxiliar[:mejor_par[0]+1]
        aux_cir2 = vauxiliar[mejor_par[0]+1:mejor_par[1]+1]
        aux_cir2.reverse()

        aux_cir1.extend(aux_cir2)

        aux_cir3 = vauxiliar[mejor_par[1]+1:]
        aux_cir1.extend(aux_cir3)

        vauxiliar = aux_cir1
        dis_circuito = dis_circuito - mayor_mejora

        if dis_circuito < mejor_dis_circuito:
            mejor_dis_circuito = dis_circuito
            mejor_circuito = copy.deepcopy(vauxiliar)
            contador = 0
        else:
            contador += 1

        if contador == 10:
            break

    return mejor_circuito

def solve_it(input_data):

    lines = input_data.split('\n')
    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    completo = crea_grafo_completo(points)
    cir_christofides = christofides(completo, points)
    cir_tabu = tabu_search(cir_christofides, points)

    coste_tabu = calcula_dis_circuito(cir_tabu, points)

    output_data = '%.2f' % coste_tabu + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, cir_tabu))

    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

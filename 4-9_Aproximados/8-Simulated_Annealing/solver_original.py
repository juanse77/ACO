#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

import math
import networkx as nx
import matplotlib.pyplot as mpl
import random
import copy

import numpy as np

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

def simulatedAnnealing(data,points):
    vauxiliar = data
    circuito = copy.deepcopy(data)

    alfa = 0.995
    n = len(data)

    max_length_arista = 0
    for i in range(0, n-1):
        distancia_arista = length(points[data[i]], points[data[i+1]])

        if distancia_arista > max_length_arista:
            max_length_arista = distancia_arista

    delta = max_length_arista/10

    T = -(delta)/np.log(0.9)
    T_medio1 = -(delta)/np.log(0.40)
    T_medio2 = -(delta) / np.log(0.25)
    T_minimo = -(delta)/np.log(1E-20)

    #print("T: " + str(T))
    #print("T_medio1: " + str(T_medio1))
    #print("T_medio2: " + str(T_medio2))
    #print("T_minimo: " + str(T_minimo))

    max_iter = int(n/8)+1

    while T > T_minimo:

        divisor = random.randint(1,n-2)
        aux1 = vauxiliar[:divisor]
        aux2 = vauxiliar[divisor:]
        aux2.extend(aux1)

        vauxiliar = aux2

        iteraciones = 0

        if T < T_medio1:
            max_iter = n*8

        if T < T_medio2:
            max_iter = n*15

        acumulado = 0
        while iteraciones < max_iter:

            v1 = random.randint(0, n-4)
            v2 = random.randint(v1+2, n-2)

            rr = length(points[vauxiliar[v1]], points[vauxiliar[v2]])
            pp = length(points[vauxiliar[v1+1]], points[vauxiliar[v2+1]])
            rp1 = length(points[vauxiliar[v1]],  points[vauxiliar[v1+1]])
            rp2 = length(points[vauxiliar[v2]], points[vauxiliar[v2+1]])

            delta = (rp1+rp2) - (rr+pp)

            if( delta > 0):
                aux_nuevo = vauxiliar[:v1+1]
                aux_nuevo2 = vauxiliar[v1+1:v2+1]
                aux_nuevo2.reverse()
                aux_nuevo.extend(aux_nuevo2)
                aux_nuevo3 = vauxiliar[v2+1:]
                aux_nuevo.extend(aux_nuevo3)

                vauxiliar = aux_nuevo
                acumulado -= delta

                if acumulado < 0:
                    acumulado = 0
                    circuito = copy.deepcopy(vauxiliar)

            else:

                u = random.random()
                umbral = math.exp(delta/T)

                if(u < umbral):
                    aux_nuevo = vauxiliar[:v1+1]
                    aux_nuevo2 = vauxiliar[v1+1:v2+1]
                    aux_nuevo2.reverse()
                    aux_nuevo.extend(aux_nuevo2)
                    aux_nuevo3 = vauxiliar[v2+1:]
                    aux_nuevo.extend(aux_nuevo3)

                    vauxiliar = aux_nuevo
                    acumulado += delta

            iteraciones = iteraciones + 1

        T = T*alfa

    return circuito

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
    cir_annealing = simulatedAnnealing(cir_christofides, points)

    coste_annealing = calcula_dis_circuito(cir_annealing, points)

    output_data = '%.2f' % coste_annealing + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, cir_annealing))

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

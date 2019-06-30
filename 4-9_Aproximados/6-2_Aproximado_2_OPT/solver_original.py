#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

import math
import networkx as nx
import matplotlib.pyplot as mpl
import random

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

def approximation2(g):

    T = nx.minimum_spanning_tree(g)
    circuit = list(nx.dfs_preorder_nodes(T, 0))

    return circuit

def opt2(aux_cir, points):
    n = len(points)
    circuito = aux_cir

    mejora = True
    while mejora:
        mejora = False

        divisor = random.randint(1, n - 2)

        aux1 = circuito[:divisor]
        aux2 = circuito[divisor:]
        aux2.extend(aux1)

        circuito = aux2

        for i in range(0, n-3):
            for j in range(i+2, n-1):

                length1 = length(points[circuito[i]], points[circuito[i+1]])
                length2 = length(points[circuito[j]], points[circuito[j+1]])

                aux_length1 = length(points[circuito[i]], points[circuito[j]])
                aux_length2 = length(points[circuito[i+1]], points[circuito[j+1]])

                if length1 + length2 > aux_length1 + aux_length2:
                    #mejora += (length1 + length2) - (aux_length1 + aux_length2)
                    mejora = True

                    aux_cir1 = circuito[:i+1]
                    aux_cir2 = circuito[i+1:j+1]
                    aux_cir2.reverse()

                    aux_cir1.extend(aux_cir2)

                    aux_cir3 = circuito[j+1:]
                    aux_cir1.extend(aux_cir3)

                    circuito = aux_cir1
        #print("Mejora: " + str(mejora))

    #nx.draw_networkx(h_grafo)
    #mpl.show()

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
    cir_aprox2 = approximation2(completo)

    cir_opt2_aprox2 = opt2(cir_aprox2, points)

    coste_opt2_aprox2 = calcula_dis_circuito(cir_opt2_aprox2, points)

    output_data = '%.2f' % coste_opt2_aprox2 + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, cir_opt2_aprox2))

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

#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

import math
import networkx as nx
import matplotlib.pyplot as mpl
import random
import copy
from Cola import Cola

import numpy as np

Point = namedtuple("Point", ['x', 'y'])

def comprueba_diferentes(circuito):
    for i in range(0, len(circuito)):
        for j in range(0, len(circuito)):
            if i == j:
                continue
            if circuito[i] == circuito[j]:
                print("Elementos repetidos: i=" + str(i) + " j=" + str(j))

def calcula_dis_circuito(circuito, points):
    n = len(circuito)

    distancia = length(points[circuito[0]], points[circuito[-1]])
    for i in range(0, n-1):
        distancia += length(points[circuito[i]], points[circuito[i+1]])

    return distancia

def crea_grafo_hamiltoniano(circuito, points):
    g = nx.DiGraph()
    n = len(points)

    for i in range(0, n):
        g.add_node(circuito[i])

    for i in range(0, n-1):
        g.add_edge(i, i+1, weight=length(points[circuito[i]], points[circuito[i+1]]))

    g.add_edge(n-1, 0, weight=length(points[circuito[n-1]], points[circuito[0]]))

    #nx.draw_networkx(g)
    #mpl.show()
    return g

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

def opt_2(cir_chr, points):
    n = len(points)
    circuito = cir_chr

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
        mayor_mejora = -400
        for i in range(0, n-3):
            for j in range(i+2, n-1):
                rp1 = length(points[vauxiliar[i]], points[vauxiliar[i+1]])
                rp2 = length(points[vauxiliar[j]], points[vauxiliar[j+1]])

                rr = length(points[vauxiliar[i]], points[vauxiliar[j]])
                pp = length(points[vauxiliar[i+1]], points[vauxiliar[j+1]])

                mejora = (rp1 + rp2) - (rr + pp)

                if mejora > mayor_mejora:
                    if not lista_tabu.buscar([vauxiliar[i], vauxiliar[j]]) and not lista_tabu.buscar([vauxiliar[i+1], vauxiliar[j+1]]):
                        mayor_mejora = mejora
                        mejor_par = [i, j]
                        aristas = [[vauxiliar[i], vauxiliar[j]], [vauxiliar[i+1], vauxiliar[j+1]]]

        lista_tabu.insertar(aristas[0])
        lista_tabu.insertar(aristas[1])

        #print(mejor_par[0])
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

    print("T: " + str(T))
    print("T_medio1: " + str(T_medio1))
    print("T_medio2: " + str(T_medio2))
    print("T_minimo: " + str(T_minimo))

    contador = 0
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
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    completo = crea_grafo_completo(points)
    cir_aprox2 = approximation2(completo)
    cir_christofides = christofides(completo, points)

    #haml_christofides = crea_grafo_hamiltoniano(cir_christofides, points)

    #nx.draw_networkx(haml_christofides)
    #mpl.show()

    cir_opt2_aprox2 = opt_2(cir_aprox2, points)
    cir_opt2_christofides = opt_2(cir_christofides, points)
    #cir_annealing = simulatedAnnealing(cir_christofides, points)
    cir_tabu = tabu_search(cir_christofides, points)

    #haml_christofides = crea_grafo_hamiltoniano(cir_opt2_christofides, points)

    #nx.draw_networkx(haml_christofides)
    #mpl.show()

    # calculate the length of the tour
    coste_aprox2 = calcula_dis_circuito(cir_aprox2, points)
    coste_christofides = calcula_dis_circuito(cir_christofides, points)
    coste_opt2_aprox2 = calcula_dis_circuito(cir_opt2_aprox2, points)
    coste_opt2_christofides = calcula_dis_circuito(cir_opt2_christofides, points)
    #coste_annealing = calcula_dis_circuito(cir_annealing, points)
    coste_tabu = calcula_dis_circuito(cir_tabu, points)

    # prepare the solution in the specified output format
    output_data = "2-Aproximación:\n"
    output_data += '%.2f' % coste_aprox2 + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, cir_aprox2))

    output_data += "\n2-OPT 2-Aproximación:\n"
    output_data += '%.2f' % coste_opt2_aprox2 + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, cir_opt2_aprox2))

    output_data += "\nChristofides:\n"
    output_data += '%.2f' % coste_christofides + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, cir_christofides))

    output_data += "\n2-OPT Christofides:\n"
    output_data += '%.2f' % coste_opt2_christofides + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, cir_opt2_christofides))

    #output_data += "\nSimulated Annealing:\n"
    #output_data += '%.2f' % coste_annealing + ' ' + str(0) + '\n'
    #output_data += ' '.join(map(str, cir_annealing))

    output_data += "\nTabu Search:\n"
    output_data += '%.2f' % coste_tabu + ' ' + str(0) + '\n'
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

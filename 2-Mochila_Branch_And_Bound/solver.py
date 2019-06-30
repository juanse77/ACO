#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from copy import copy, deepcopy
import numpy as np
from time import time
import Pila

def calcular_bound(items, valor_acumulado, espacio, profundidad):
    weight = 0
    bound = valor_acumulado
    for i in range(profundidad, len(items)):
        if weight + items[i].weight <= espacio:
            weight += items[i].weight
            bound += items[i].value
        else:
            diferencia = espacio - weight
            bound += items[i].density * diferencia
            break
    return bound

def solve_it(input_data):
    Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])
    Nodo = namedtuple("Nodo", ['index', 'value', 'room', 'bound', 'taken'])

    tiempo1 = time()

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), float(parts[0]) / float(parts[1])))

    taken = []
    taken_optimo = []

    items.sort(key=lambda c: c.density, reverse=True)

    for item in items:
        taken.append([item.index, 0])

    taken_optimo = deepcopy(taken)

    bound = calcular_bound(items, 0, capacity, 0)
    pila = Pila.Pila()
    pila.incluir(Nodo(0, 0, capacity, bound, 1))

    max_beneficio = 0

    while not pila.estaVacia():
        nodo = pila.extraer()

        if nodo.taken == 0:
            taken[nodo.index - 1][1] = 0

        elif nodo.value > max_beneficio:

            for i in range(0, nodo.index):
                taken_optimo[i][1] = taken[i][1]

            for i in range(nodo.index, len(items)):
                taken_optimo[i][1] = 0

            max_beneficio = nodo.value

        if nodo.index < len(items):

            aux_bound = calcular_bound(items, nodo.value, nodo.room, nodo.index)

            if aux_bound > max_beneficio:
                pila.incluir(Nodo(nodo.index + 1, nodo.value, nodo.room, aux_bound, 0))

            if nodo.room >= items[nodo.index].weight:

                value = items[nodo.index].value + nodo.value
                taken[nodo.index][1] = 1
                pila.incluir(Nodo(nodo.index + 1, value, nodo.room - items[nodo.index].weight, nodo.bound, 1))

    taken_optimo.sort(key=lambda c: c[0])
    taken_optimo_ordenado = np.array(taken_optimo)
    tiempo2 = time()

    output_data = str(max_beneficio) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken_optimo_ordenado[:,1])) + '\n'
    output_data += str(tiempo2 - tiempo1)
    return output_data


def solve_it_greedy(input_data):
    Item = namedtuple("Item", ['index', 'value', 'weight', 'valor_neto'])
    # Modify this code to run your optimization algorithm
    tiempo1 = time()
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1]), float(parts[0]) / float(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0] * len(items)

    items.sort(key=lambda c: c.valor_neto, reverse=True)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    tiempo2 = time()

    # prepare the solution in the specified output format
    output_data = 'Algoritmo ávido:\n'
    output_data += str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken)) + '\n'
    output_data += 'Tiempo: ' + str(tiempo2 - tiempo1)
    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        #print(solve_it_greedy(input_data))
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')


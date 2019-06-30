#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from time import time
from copy import copy, deepcopy
from typing import List

Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(int(i - 1), int(parts[0]), int(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    tiempo1 = time()
    taken = [0] * len(items)

    V = [0] * (item_count + 1)
    for i in range(0, item_count + 1):
        V[i] = [0] * (capacity + 1)

    for item in items:
        for w in range(0, capacity + 1):
            if item.weight <= w:
                if item.value + V[item.index][w - item.weight] > V[item.index][w]:
                    V[item.index + 1][w] = item.value + V[item.index][w - item.weight]

                else:
                    V[item.index + 1][w] = V[item.index][w]

            else:
                V[item.index + 1][w] = V[item.index][w]

    i = item_count
    k = capacity

    while i > 0 and k > 0:
        if V[i][k] != V[i-1][k]:
            taken[i-1] = 1
            k = k - items[i-1].weight
        i = i - 1

    tiempo2 = time()

    # prepare the solution in the specified output format
    output_data = str(V[item_count][capacity]) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    output_data += '\n' + str(tiempo2 - tiempo1)

    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))

    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')


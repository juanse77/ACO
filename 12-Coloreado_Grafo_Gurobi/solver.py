#!/usr/bin/python
# -*- coding: utf-8 -*-
from gurobipy import *

def solve_it(input_data):
    m = Model("Colores")
    
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    
    v = [i for i in range(node_count)]
    c = m.addVars(node_count, node_count, vtype=GRB.BINARY, name="colores")
    
    for i in range(node_count):
        m.addConstr(quicksum(c.select(i,'*')), GRB.EQUAL, 1)
    
    for edge in edges:
        for j in range(node_count):
            m.addConstr((c[edge[0], j] + c[edge[1], j]) <= 1)
    
    suma = 0
    for i in range(node_count):
        for j in range(node_count):
            suma += v[j] * c[i,j]
    
    m.Params.timeLimit = 900
    m.Params.CliqueCuts = 0
    
    m.setObjective(suma, GRB.MINIMIZE)
    m.optimize()
    
    solution = []
    max_color = 0
    for i in range(node_count):
        for j in range(node_count):
            if c[i,j].x != 0:
                solution.append(j)
                if max_color < j:
                    max_color = j
    
    output_data = str(max_color+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')


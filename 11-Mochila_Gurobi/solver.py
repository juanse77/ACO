#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from gurobipy import *
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):

    lines = input_data.split('\n')    
    m =Model("mochila")
    
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    v_taken = m.addVars(item_count, vtype=GRB.BINARY, name="v_taken")
    
    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    m.addConstr(quicksum([v_taken[i]*items[i].weight for i in range(item_count)])<= capacity)

    m.Params.MIPGap = 0    
    m.setObjective(quicksum([v_taken[i]*items[i].value for i in range(item_count)]),GRB.MAXIMIZE)    
    m.optimize()
    
    taken= [int (v_taken[i].x) for i in range (item_count)]
    value = sum([v_taken[i].x * items[i].value for i in range (item_count)])
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
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


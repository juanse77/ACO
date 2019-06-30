#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymzn
import os
import json
from time import time

def solve_it(input_data):

    tiempo1 = time()
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = ""

    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges+=parts[0]+","+parts[1]
        if i != edge_count:
            edges+= "|"

    print(os.getcwd()+"/fichero.dzn")
    file = open(os.getcwd()+'/fichero.dzn','w')
    file.write("nNodos="+str(node_count)+";\n")
    file.write("nAristas="+str(edge_count)+ ";\n")
    file.write("aristas=[|"+str(edges)+ "|];")
    file.close()
    s = pymzn.minizinc('graf_color.mzn','fichero.dzn', output_mode='json')

    solucion_array = json.loads(s[0])
    num_colors = max(solucion_array['resultado'])

    tiempo2 = time()

    output_data = str(num_colors) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solucion_array['resultado']))
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')


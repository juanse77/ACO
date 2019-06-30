#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
from gurobipy import *

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    m = Model("fl")

    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    almacenes = m.addVars(facility_count, vtype=GRB.BINARY, name="almacenes")
    asignaciones = m.addVars(facility_count, customer_count, vtype=GRB.BINARY, name="asignaciones")
    
    coste_transporte_total = []
    for i in range(facility_count):
        coste_transporte_almacen = []
        for j in range(customer_count):
            m.addConstr(asignaciones[i,j] <= almacenes[i])
            coste_transporte_almacen.append(length(facilities[i].location, customers[j].location))  
        
        coste_transporte_total.append(coste_transporte_almacen)
    
    for i in range(customer_count):
        m.addConstr(quicksum(asignaciones.select('*',i)), GRB.EQUAL, 1)
        
    for i in range(facility_count):
        m.addConstr(facilities[i].capacity - 
                    quicksum([asignaciones[i, j] * customers[j].demand 
                         for j in range(customer_count)]) >= 0)
    
    obj = 0
    for i in range(facility_count):
        obj += facilities[i].setup_cost * almacenes[i]
        for j in range(customer_count):
            obj += coste_transporte_total[i][j] * asignaciones[i,j]
    
    m.Params.timeLimit = 900 
    m.setObjective(obj, GRB.MINIMIZE)
    m.optimize()
        
    solution = []
    coste = sum([f.setup_cost*almacenes[f.index].x for f in facilities])
    for i in range(facility_count):
        for j in range(customer_count):
            if asignaciones[i,j].x == 1:
                coste += length(customers[j].location, facilities[i].location)
                solution.append(i)
    
    output_data = '%.2f' % coste + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')


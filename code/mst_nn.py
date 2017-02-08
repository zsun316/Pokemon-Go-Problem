# Nearest neighbor algorithm and Minimum Spanning Tree algorithm
from collections import deque
from tspparse    import *
from numpy       import array
from computeMST import *
import networkx as nx
import os
import sys
import string

def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)

def calc_distance(tsp, city1_index, city2_index):
    """Calculate distance between cities by their (one-based) indices"""
    cities = tsp["CITIES"]
    return distance(cities[city1_index - 1], cities[city2_index - 1])

def path_length(tsp,path):
    """Find the length of a path of cities given as a list"""
    if len(path) == 1:
        return 0
    else:
        start_node = path.pop()
        next_node  = path[-1]
        return calc_distance(tsp,start_node,next_node) + path_length(tsp,path)

def tour_from_path(path):
    """Append the first city in a path to the end in order to obtain a tour"""
    path.append(path[0])
    return path

def graph_prepare(tsp):
    G = nx.Graph()
    cities = set(range(1,tsp["DIMENSION"] + 1))
    for i in range(1,len(cities)):
        for j in range(i+1,len(cities)+1):
            u = int(i)
            v = int(j)
            weightedge = calc_distance(tsp, i, j)
            G.add_edge(u, v, weight = round(float(weightedge),4))
    return G

def eulerian_prepare(tsp):
    G_now = graph_prepare(tsp)
    #mst = nx.minimum_spanning_tree(G_now, weight = 'weight')
    mst = kruskal_mst(G_now)
    mst_double = mst.to_directed()
    eul = nx.eulerian_circuit(mst_double)
    return eul

def nearest_neighbor(tsp,untraveled_cities,current_city):
    """Given a set of city keys, find the key corresponding to the
closest city"""
    distance_to_current_city = lambda city: calc_distance(tsp,current_city,city)
    return min(untraveled_cities, key = distance_to_current_city)

def nearest_neighbor_tour(tsp):
    """Construct a tour through all cities in a TSP by following the nearest
neighbor heuristic"""
    nearest_neighbor_path = [1]
    current_city          = 1
    cities_to_travel      = set(range(2, tsp["DIMENSION"] + 1))

    while cities_to_travel:
        current_city = nearest_neighbor(tsp,cities_to_travel,current_city)
        nearest_neighbor_path.append(current_city)
        cities_to_travel.remove(current_city)
        
    #print(tour_from_path(nearest_neighbor_path))
    return tour_from_path(nearest_neighbor_path)

def minimum_spanning_tree_tour(tsp):
    """Construct a tour through all cities in a TSP by following minimum spanning
tree approximation"""
    eul = eulerian_prepare(tsp)
    mst_path_temp = [u for u,v in eul]
    #if tsp["NAME"] == "Atlanta":
    #    print(mst_path_temp)
    mst_path = list(dedupe(mst_path_temp))
    return tour_from_path(mst_path)


def calc_nearest_neighbor_tour(tsp):       
    return path_length(tsp,nearest_neighbor_tour(tsp))

def calc_minimum_spanning_tree_tour(tsp):
    return path_length(tsp,minimum_spanning_tree_tour(tsp))

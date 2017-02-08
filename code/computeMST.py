#MST algorithm used for tsp
from __future__ import division
import math
import random
import networkx as nx

class ArrayUnionFind:
    def __init__(self, S):
        self.group = dict((s,s) for s in S) 
        self.size = dict((s,1) for s in S) 
        self.items = dict((s,[s]) for s in S) 
        
def make_union_find(S):
    """Create a union-find data structure"""
    return ArrayUnionFind(S)
    
def find(UF, s):
    """Return the id for the group containing s"""
    return UF.group[s]

def union(UF, a,b):
    """Union the two sets a and b"""
    assert a in UF.items and b in UF.items
    if UF.size[a] > UF.size[b]:
        a,b = b,a
    for s in UF.items[a]:
        UF.group[s] = b
        UF.items[b].append(s)
    UF.size[b] += UF.size[a]
    del UF.size[a]
    del UF.items[a]

def kruskal_mst(G):
    """Return a minimum spanning tree using kruskal's algorithm"""
    Edges = [(u, v, G[u][v]['weight']) for u,v in G.edges()]
    #Edges.sort(cmp=lambda x,y: cmp(x[2],y[2]))
    Edges.sort(key=lambda edges: edges[2])

    UF = make_union_find(G.nodes())  

    mst = [] 
    for u,v,d in Edges:
        setu = find(UF, u)
        setv = find(UF, v)
        if setu != setv:
            mst.append((u,v,G[u][v]['weight']))
            union(UF, setu, setv)
    Mst = nx.Graph()
    Mst.add_weighted_edges_from(mst)
    return Mst

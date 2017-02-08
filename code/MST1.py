# MST used for Branch and Bound algorithm
rank = dict()
parent = dict()

def makeset(vertice):
    parent[vertice] = vertice
    rank[vertice] = 0

def find(vertice):
    if parent[vertice] == vertice:
        return parent[vertice]
    else:
        return find(parent[vertice])

def union(vertice1, vertice2):
    root1 = find(vertice1)
    root2 = find(vertice2)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
            if rank[root1] == rank[root2]:
               rank[root2] += 1

#parseEdges
def parseEdges(list, distancematrix):
    vertices = set()
    edges = []
    if len(list) == 0: return vertices,edges
    for i in range(0,len(list)):
        vertices.add(int(list[i]))
        for j in range(i, len(list)):
            edges.append({'u': int(list[i]), 'v' : int(list[j]), 'weight' : float(distancematrix[list[i], list[j]])})
    return vertices,edges

def getTotalEdge(n, distancematrix):
    edges = []
    for i in range(0,n):
        for j in range(i, n):
            edges.append({'u': int(i), 'v' : int(j), 'weight' : float(distancematrix[i, j])})
    return edges

def getEdge(list, edges):
    tempSet = set(list)
    result = []
    for each in edges:
        if (each['u'] in tempSet) & (each['v'] in tempSet): result.append(each)
    return result

def weight(s):
    return s['weight']

def sortedges(edges):
    return sorted(edges, key = weight)

# computeMST
def computeMST(vertices, edges):
    edges = sortedges(edges)
    MST = 0
    for each in vertices:
        makeset(each)
    for each in edges:
        u = each['u']
        v = each['v']
        weight1 = each['weight']
        if find(u) != find(v):
            union(u, v)
            MST += weight1
    return MST
    
    

def findLbAB(a, list, distancematrix):
    min = float("inf")
    for i in range(0, len(list)):
        if distancematrix[a, list[i]] < min: min = distancematrix[a, list[i]]
    return min

def calPartLen(list, distancematrix):
    sum = 0
    for i in range(0, len(list) - 1):
        sum += distancematrix[list[i], list[i + 1]]
    return sum
    
def calTotalLen(list, distancematrix):
    sum = distancematrix[list[0], list[-1]]
    for i in range(0, len(list) - 1):
        sum += distancematrix[list[i], list[i + 1]]
    return sum


def calMst(list1, list2,edges,distancematrix):
    tempV = set(list2)
    tempE = getEdge(list2, edges)
    MST = computeMST(tempV,tempE)
    if len(list1) == 0: lb = MST
    elif len(list2) == 0: lb = calTotalLen(list1, distancematrix)
    else: lb = calPartLen(list1, distancematrix) + MST + \
         findLbAB(list1[0], list2, distancematrix) + findLbAB(list1[-1], list2, distancematrix)
    return lb
    

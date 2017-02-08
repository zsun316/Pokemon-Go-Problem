#Branch and Bound algorithm
import math
import numpy as np
import time
import sys
from heapq import *
from hc import *
from MST1 import *
import glob


def readData(tspfile):
    data = []
    count = 0
    for line in open(tspfile,'r'):
            #skip line
            if(count <= 4):
                pass
            else:
                if(line.split()[0] == "EOF"):
                    break
                index = int(line.split()[0])
                x = float(line.split()[1])
                y = float(line.split()[2])
                data.append([x,y])
            count += 1
    return np.array(data)

def computeDistanceMatrix(data):
    inf = float("inf")
    nnode = data.shape[0]
    distancemetric = np.zeros((nnode,nnode))
    for i in range(nnode):
        ix = data[i,0]
        iy = data[i,1]
        for j in range(nnode):
            if j != i:
                jx = data[j,0]
                jy = data[j,1]
                distancemetric[i,j] = math.sqrt((ix - jx)**2 + (iy - jy)**2)
            else:
                distancemetric[i,i] = inf 
    return distancemetric



def getLowerBoundbyReduction(distancematrix,tempList1): 
    distancematrix1 = np.copy(distancematrix)
    inf = float("inf")
    pathsum = 0
    if len(tempList1)!=0 and len(tempList1)!=1:
        for i in range(len(tempList1)-1):
            pathsum = pathsum+distancematrix1[tempList1[i],tempList1[i+1]]
            distancematrix1[tempList1[i+1],tempList1[i]] = inf
        distancematrix1=np.delete(distancematrix1,tempList1[:-1],0)
        distancematrix1=np.delete(distancematrix1,tempList1[1:],1)
    rowmin = distancematrix1.min(axis = 1)
    temprowsum = rowmin.sum()
    distancematrix1 -= np.array([rowmin]).T
    colmin = distancematrix1.min(axis = 0)
    tempcolsum = colmin.sum()
    ndata = distancematrix.shape[0]
    return tempcolsum+temprowsum+pathsum    

     

def outputSol(tofile,optpath,optdist,distancematrix,cityname,cutoff):
    with open(tofile,'w') as f:
        f.write("%d" %optdist)
        f.write('\n')
        for i in range(len(optpath) - 1):
            f.write("%d %d %d" %(optpath[i],optpath[i+1],distancematrix[optpath[i],optpath[i+1]]))
            f.write('\n')
        
        f.write("%d %d %d" %(optpath[len(optpath)-1],optpath[0],distancematrix[optpath[len(optpath)-1],optpath[0]]))
    return



 

def dfs(list1, list2, edges, distancematrix,lbmethod,cuttime,ftracefile):
    global best
    global bestpath
    global start_time

    total_time = (time.time() - start_time)
    if total_time > cuttime:
        return
    tempheapq = []
    
    
    for i in range(0, len(list2)):
        tempList1 = list(list1)
        tempList1.append(list2[i])
        tempList2 = list2[:i] + list2[i+1 :]

        if lbmethod == 'Matrix':
            lb = getLowerBoundbyReduction(distancematrix,tempList1)
        else:
            lb = calMst(tempList1, tempList2, edges, distancematrix)
        
        heappush(tempheapq,(lb,tempList1,tempList2))

        
    while len(tempheapq)!=0:
        (tempLb, tempList1, tempList2) = heappop(tempheapq)
        if tempLb > best:
            return 
        if len(tempList2) == 0:
            best = tempLb 
            bestpath = tempList1
            total_time = (time.time() - start_time)
            ftracefile.write("%0.5f %d\n" %(total_time,best))
            return       
        dfs(tempList1, tempList2, edges, distancematrix,lbmethod,cuttime,ftracefile)

    return 


def TSP(tsppath,isInitialize,lbmethod,cuttime,ftracefile):
    global best
    global start_time
    global bestpath
    data=readData(tsppath)
    distancematrix = computeDistanceMatrix(data)
    n = distancematrix.shape[0]
    edges = getTotalEdge(n, distancematrix)
    
    if isInitialize: 
        hc = []
        iniSol = initsol(len(data))
        randSol(iniSol)
        move = True
        while move == True:
            move = False
            move = doNeigbhour(iniSol, data, move)
            hc.append(calTotalDis(iniSol, data))
        best = hc[-1]
    else:
        best = float("inf")

    start_time = time.time()
    dfs([0],range(1,n), edges, distancematrix,lbmethod,cuttime,ftracefile)
    ftracefile.close()
    
           
    return distancematrix
    
        


def bnbmain(cuttime,tsppath,cityname):
    global best, bestpath, start_time
    # run the experiments
    isInitialize = 0
    lbmethod = 'MST'

    tofiletrace = cityname+'_BnB_'+str(int(cuttime))+'.trace'
    
    ftracefile = open(tofiletrace,'w') 
    
    

    distancematrix=TSP(tsppath,isInitialize,lbmethod,cuttime,ftracefile)
    total_time = (time.time() - start_time)
   
    
    tofile = cityname+'_BnB_'+str(int(cuttime))+'.sol'
    outputSol(tofile,bestpath,best,distancematrix,cityname,600)



    total_time = (time.time() - start_time)
    return int(best)

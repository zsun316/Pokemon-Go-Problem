# Hill climbing algorithm
import math
import random as rd
#import matplotlib.pyplot as plt
import numpy as np
import time
import sys

def readData(tspfile, data):
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

def calTwoPoint(data, i, j):
    ix = data[i][0]
    iy = data[i][1]
    jx = data[j][0]
    jy = data[j][1]
    return math.sqrt((ix - jx)**2 + (iy - jy)**2)

def initsol(num):
    sol = []
    for i in range(num):
        sol.append(i)
    return sol

def swap(array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp

def randSol(sol):
    length = len(sol)
    for i in range(0, length - 1):
        tempRand = rd.randint(i + 1, length - 1)
        swap(sol, i, tempRand)

def calTotalDis(sol, data):
    length = len(sol)
    distance = calTwoPoint(data, sol[0], sol[length - 1])
    for i in range(length - 1):
        distance += calTwoPoint(data, sol[i], sol[i + 1])
    return distance

def chooseNeighbor(sol, b, d):
    reverse = []
    for i in range(d, b - 1, -1):
        reverse.append(sol[i])
    for i in range(b, d + 1):
        sol[i] = reverse[i - b]


def doNeigbhour(sol, data, move):
    length = len(sol)
    step = 1
    while step < length**2:
        firstRd = rd.randint(0, length - 1)
        secondRd = rd.randint(0, length - 1)
        a = min(firstRd, secondRd)
        c = max(firstRd, secondRd)
        if c - a <= 2: continue
        b = a + 1
        d = c - 1
        sa = sol[a]
        sb = sol[b]
        sd = sol[d]
        sc = sol[c]
        dE = calTwoPoint(data, sa, sb) + calTwoPoint(data, sd, sc) - \
             (calTwoPoint(data, sa, sd) + calTwoPoint(data,sb, sc))
        step += 1
        if dE > 0:
            chooseNeighbor(sol, b, d)
            move = True
            break
    return move

def output(sol,dist,filename,cutoff,data,seed):
    solfile = open(filename+'_LS1_'+str(cutoff)+'_'+seed+'.sol','w')
    solfile.write("%d" %dist)
    solfile.write('\n')
    count = 0
    while count < len(sol)- 1:
        solfile.write("%d %d %d" %(sol[count], sol[count+1], calTwoPoint(data, sol[count], sol[count+1])))
        solfile.write('\n')
        count += 1
    solfile.write("%d %d %d" %(sol[count], sol[0], calTwoPoint(data, sol[count], sol[0])))
    solfile.close()




def hcmain(rdseed, cutofftime,filename,filepath):

    opt_operator = {'Roanoke':655454,'Toronto':1176151,'Atlanta':2003763,'Boston':893536,'Cincinnati':277952,
                    'Denver':100431,'NYC':1555060,'Philadelphia':1395981,'Champaign':52643,'UKansasState':62962,
                    'UMissouri':132709, 'SanFrancisco':810196}
    startTime = time.time()
    data = []
    plot = []
    #filename = sys.argv[1]
    readData(filepath,data)
    #print filename
    opt = opt_operator.get(filename)
    #print opt
    rd.seed(rdseed)
    tracefile = open(filename+'_LS1_'+str(cutofftime)+'_'+rdseed+'.trace','w')
    iniSol = initsol(len(data))
    randSol(iniSol)
    move = True
    while move == True:
        move = False
        move = doNeigbhour(iniSol, data, move)
        dist = calTotalDis(iniSol, data)
  #      quality = int(((dist - opt)/float(opt))*100)
        tracefile.write("%0.5f %d\n" %(time.time()-startTime, dist))

        plot.append(dist)

    total_time = (time.time() - startTime) * 1000
    #print iniSol
    tracefile.close()
    output(iniSol,plot[-1],filename,cutofftime,data,rdseed)
    print plot[-1]
    print total_time
    return int(dist)

##if __name__ == '__main__':
##    hcmain()

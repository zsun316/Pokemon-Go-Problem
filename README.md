# Pokemon-Go-Problem

## Description
> Our pokemon go problem is a traveling salesman problem, which is that given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city. We apply five algorithms to solve the problem: branch and bound, simulated annealing, hill climbing, approximation with minimum spanning tree and nearest neighbor.

## Requirement: 
Numpy, networkx 

## Overall Structure
> mst_nn.py(NN and MST), sa.py, hc.py, bnb_od.py are 5 implemented algortihms. <br>
> main.py is the main function used for calling algorithms. <br>
> argparser.py is used for parsing parameter in command line. <br>

## Running method: 
Open terminal in 'code' folder. Statement scheme is:  <br>
`$ python main.py [-MST|-Heur|-LS1|-LS2|-BnB] -t [time] -rs [number of random seed] PATH [file name/location`

## Take 'Atlanta.tsp' as an example
All data files are in DATA folder:
### MST: 
`$ python main.py -MST -t 600 DATA/Atlanta.tsp`
### Nearest Neighbor: 
`$ python main.py -Heur -t 600 DATA/Atlanta.tsp`
### Branch and Bound: 
`$ python main.py -BnB -t 600 DATA/Atlanta.tsp`
### Hill climbing: 
`$ python main.py -LS1 -t 600 -rs 1 DATA/Atlanta.tsp`
### Simulated annealing: 
`$ python main.py -LS2 -t 600 -rs 1 DATA/Atlanta.tsp`

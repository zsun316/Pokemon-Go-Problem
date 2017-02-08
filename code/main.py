#python2.7
#main function used to call 5 algorithms
import time
import os

from argparser  import parser
from tspparse   import read_tsp_file
from mst_nn import *

from glob    import iglob
from os.path import *
from hc import *
from sa import *
from bnb_od import *

opt_operator = {'Roanoke':655454,'Toronto':1176151,'Atlanta':2003763,'Boston':893536,'Cincinnati':277952,
                'Denver':100431,'NYC':1555060,'Philadelphia':1395981,'Champaign':52643,'UKansasState':62962,
                'UMissouri':132709, 'SanFrancisco':810196}

def glean_tsp_files(path_arg_list):
    for path_arg in path_arg_list:

        if isdir(path_arg):
            for filepath in iglob(join(path_arg,"*.tsp")):
                yield filepath

        elif isfile(path_arg) & str(path_arg).endswith(".tsp"):
            yield path_arg

        elif isfile(path_arg) & (not path_arg.endswith(".tsp")):
            print("Can't open file ``{0}'': not a .tsp file".format(path_arg))

        elif exists(path_arg):
            print("Path {0} is neither a file nor a directory".format(path_arg))

        else:
            print("Path {0} does not exist".format(path_arg))

def print_results_from_tsp_path(call_args, tsp_path):
    time_start1 = time.time()
    tsp = read_tsp_file(tsp_path)
    print("TSP Problem:              {}".format(tsp["NAME"]))
    print("PATH:                     {}".format(tsp_path))

    if call_args.upper_bound_time:
        cutoff = float(call_args.upper_bound_time)
        cutoff = int(cutoff)
    
    if call_args.need_nearest_neighbor:
        print("NEAREST NEIGHBOR LENGTH:  {}"
             . format(calc_nearest_neighbor_tour(tsp)))
        
        output1 = open(str(tsp["NAME"])+str("_")+str("NN")+str("_") + str(cutoff)+str(".sol"), "w")
        best_result = path_length(tsp,nearest_neighbor_tour(tsp))
        output1.write(str(best_result) + " " + "\n")

##        output3 = open("relerr_NN.sol", "a")
##        output3.write(str(tsp["NAME"]) + " " + str((best_result - opt_operator[tsp["NAME"]])/float(opt_operator[tsp["NAME"]])) + " " "\n")

        e_list = tour_from_path(nearest_neighbor_tour(tsp))
        
        for i in range(len(e_list)-2):
            source = e_list[i]
            target = e_list[i+1]
            edge_now = calc_distance(tsp, source, target)
            output1.write(str(source) + " " + str(target) + " " + str(edge_now) + "\n")
        time_end = time.time()
        this_time = time_end - time_start1
        
        output2 = open(str(tsp["NAME"])+str("_")+str("NN")+str("_") + str(cutoff)+str(".trace"), "w")
        output2.write(str(round(this_time,4)) + " " + str(best_result) + "\n")
        
    if call_args.need_minimum_spanning_tree:
        print("MINIMUM SPANNING TREE LENGTH: {}"
             . format(calc_minimum_spanning_tree_tour(tsp)))
        
        output1 = open(str(tsp["NAME"])+str("_")+str("MST")+str("_") + str(cutoff)+str(".sol"), "w")
        best_result = path_length(tsp,minimum_spanning_tree_tour(tsp))
        output1.write(str(best_result) + " " + "\n")

##        output3 = open("relerr_MST.sol", "a")
##        output3.write(str(tsp["NAME"]) + " " + str(100 * (best_result - opt_operator[tsp["NAME"]])/opt_operator[tsp["NAME"]]) + "%" + " " + "\n")
        
        e_list = tour_from_path(minimum_spanning_tree_tour(tsp))
        
        for i in range(len(e_list)-2):
            source = e_list[i]
            target = e_list[i+1]
            edge_now = calc_distance(tsp, source, target)
            output1.write(str(source) + " " + str(target) + " " + str(edge_now) + "\n")
        time_end = time.time()
        this_time = time_end - time_start1

        output2 = open(str(tsp["NAME"])+str("_")+str("MST")+str("_") + str(cutoff)+str(".trace"), "w")
        output2.write(str(round(this_time,4)) + " " + str(best_result) + "\n")
    
    if call_args.num_of_randomseed:
        rdseed = call_args.num_of_randomseed
        
    if call_args.hill_climbing:
        print("HILL CLIMBING LENTH: {}"
             . format(hcmain(rdseed, cutoff, tsp["NAME"], tsp_path)))

    if call_args.simulated_annealing:
        print("SIMULATED ANNEALING LENGTH: {}"
             . format(samain(rdseed, cutoff, tsp["NAME"], tsp_path)))

    if call_args.branch_and_bound:
        filename = str(tsp["NAME"]) + str(".tsp")
        print("BRANCH AND BOUND LENGTH: {}"
             . format(bnbmain(cutoff, tsp_path,tsp["NAME"])))
        
    print("")
    del(tsp)

def main():
    call_args = parser.parse_args()
    for tsp_path in glean_tsp_files(call_args.tsp_queue):
        print_results_from_tsp_path(call_args,tsp_path)

if __name__ == "__main__":
    main()

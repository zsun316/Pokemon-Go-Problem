#Parse input parameters to main.py
import argparse

parser = argparse.ArgumentParser(
      description = "Parse TSP files and calculate paths using algorithms.")

parser.add_argument (
      "-Heur"
    , "--nearest"
    , action  = "store_true"
    , dest    = "need_nearest_neighbor"
    , default = False
    , help    = "calculate distance traveled by nearest neighbor heuristic"
    )

parser.add_argument (
      "-MST"
    , "--minimum"
    , action  = "store_true"
    , dest    = "need_minimum_spanning_tree"
    , default = False
    , help    = "calculate distance traveled by minimum spanning tree"
    )

parser.add_argument (
      "-LS1"
    , "--hill"
    , action  = "store_true"
    , dest    = "hill_climbing"
    , default = False
    , help    = "calculate distance traveled by hill climbing"
    )

parser.add_argument (
      "-LS2"
    , "--simulated"
    , action  = "store_true"
    , dest    = "simulated_annealing"
    , default = False
    , help    = "calculate distance traveled by simulated_annealing"
    )

parser.add_argument (
      "-BnB"
    , "--BranchBound"
    , action  = "store_true"
    , dest    = "branch_and_bound"
    , default = False
    , help    = "calculate distance traveled by branch_and_bound"
    )

parser.add_argument(
      "-t"
      "--time"
    , action  = "store"
    , dest    = "upper_bound_time"
    , help    = "Set upper bound running time"
    )

parser.add_argument(
      "-rs"
      "--seed"
    , action  = "store"
    , dest    = "num_of_randomseed"
    , help    = "Set number of random seed"
    )

parser.add_argument (
      "tsp_queue"
    , nargs   = "+"
    , metavar = "PATH"
    , help    = "Path to directory or .tsp file. If PATH is a directory, run "
                "on all .tsp files in the directory."
    )

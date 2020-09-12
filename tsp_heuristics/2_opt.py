import numpy as np
from utils import tour_cost
from itertools import combinations
import time

def two_opt(cost, tour, iterations):
    opt_tour = tour.copy()
    for _ in range(iterations):
        for i in range(len(opt_tour)):
            for j in range(i + 2, len(opt_tour)-1):
                if cost[opt_tour[i], opt_tour[i+1]] + cost[opt_tour[j], opt_tour[j+1]] > cost[opt_tour[i], opt_tour[j]] + cost[opt_tour[i+1], opt_tour[j+1]]:
                    opt_tour[i+1:j+1] = reversed(opt_tour[i+1:j+1])
    
        if tour_cost(cost, opt_tour) < tour_cost(cost, tour):
                    tour = opt_tour
    return tour


if __name__ == "__main__":
    
    # node_array = np.random.random_integers(0,high=10,size=(10,2))

    start_time = time.clock()
    # adj_matrix = distance_matrix(node_array, node_array, p=2)

    # cost = np.random.random_integers(0,high=100,size=(100,100))
    cost = np.array([[ 0, 32, 53, 51, 84, 72, 76, 33, 33, 64],
                     [32,  0, 21, 29, 76, 40, 43, 41, 36, 37],
                     [53, 21,  0, 23, 72, 19, 23, 52, 46, 22],
                     [51, 29, 23,  0, 50, 35, 39, 36, 30, 14],
                     [84, 76, 72, 50,  0, 79, 83, 51, 51, 53],
                     [72, 40, 19, 35, 79,  0,  4, 69, 63, 26],
                     [76, 43, 23, 39, 83,  4,  0, 74, 67, 30],
                     [33, 41, 52, 36, 51, 69, 74,  0,  6, 50],
                     [33, 36, 46, 30, 51, 63, 67,  6,  0, 44],
                     [64, 37, 22, 14, 53, 26, 30,  50, 44, 0]])
    
    tour = [i for i in range(len(cost))]
    tour.extend([tour[0]])
    print('Original Tour:', tour)
    print('Original Tour Cost:', tour_cost(cost, tour))
    iterations = 1
    opt2_tour = two_opt(cost, tour, iterations)
    print('2-opt Tour:', opt2_tour)
    print('2-opt Tour Cost:', tour_cost(cost, opt2_tour))
   
	
    print('Computation Time:',(time.clock() - start_time))
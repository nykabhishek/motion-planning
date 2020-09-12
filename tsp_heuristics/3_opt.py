import numpy as np
from utils import tour_cost
from itertools import combinations
import time


def opt_3(cost, tour, iterations):
    opt_tour = tour.copy()
    for _ in range(iterations):
        for i in range(len(opt_tour) - 1):
            for j in range(i + 2, len(opt_tour) - 1):
                for k in range(j + 2, len(opt_tour) - 1):
                    way = 0
                    current = cost[opt_tour[i], opt_tour[i+1]] + cost[opt_tour[j], opt_tour[j+1]] + cost[opt_tour[k], opt_tour[k+1]]
                    if current >  cost[opt_tour[i], opt_tour[i+1]] + cost[opt_tour[j], opt_tour[k]] + cost[opt_tour[j+1], opt_tour[k+1]]:
                        current = cost[opt_tour[i], opt_tour[i+1]] + cost[opt_tour[j], opt_tour[k]] + cost[opt_tour[j+1], opt_tour[k+1]]
                        way = 1
                    if current >  cost[opt_tour[i], opt_tour[j]] + cost[opt_tour[i+1], opt_tour[j+1]] + cost[opt_tour[k], opt_tour[k+1]]:
                        current = cost[opt_tour[i], opt_tour[j]] + cost[opt_tour[i+1], opt_tour[j+1]] + cost[opt_tour[k], opt_tour[k+1]]
                        way = 2
                    if current >  cost[opt_tour[i], opt_tour[j]] + cost[opt_tour[i+1], opt_tour[k]] + cost[opt_tour[j+1], opt_tour[k+1]]:
                        current = cost[opt_tour[i], opt_tour[j]] + cost[opt_tour[i+1], opt_tour[k]] + cost[opt_tour[j+1], opt_tour[k+1]]
                        way = 3
                    if current >  cost[opt_tour[i], opt_tour[j+1]] + cost[opt_tour[k], opt_tour[i+1]] + cost[opt_tour[j], opt_tour[k+1]]:
                        current = cost[opt_tour[i], opt_tour[j+1]] + cost[opt_tour[k], opt_tour[i+1]] + cost[opt_tour[j], opt_tour[k+1]]
                        way = 4
                    if current >  cost[opt_tour[i], opt_tour[j+1]] + cost[opt_tour[k], opt_tour[j]] + cost[opt_tour[i+1], opt_tour[k+1]]:
                        current = cost[opt_tour[i], opt_tour[j+1]] + cost[opt_tour[k], opt_tour[j]] + cost[opt_tour[i+1], opt_tour[k+1]]
                        way = 5
                    if current >  cost[opt_tour[i], opt_tour[k]] + cost[opt_tour[j+1], opt_tour[i+1]] + cost[opt_tour[j], opt_tour[k+1]]:
                        current = cost[opt_tour[i], opt_tour[k]] + cost[opt_tour[j+1], opt_tour[i+1]] + cost[opt_tour[j], opt_tour[k+1]]
                        way = 6
                    if current >  cost[opt_tour[i], opt_tour[k]] + cost[opt_tour[j+1], opt_tour[j]] + cost[opt_tour[i+1], opt_tour[k+1]]:
                        current = cost[opt_tour[i], opt_tour[k]] + cost[opt_tour[j+1], opt_tour[j]] + cost[opt_tour[i+1], opt_tour[k+1]]
                        way = 7
                    
                    if way == 1:
                        opt_tour[j+1:k+1] = reversed(opt_tour[j+1:k+1])
                    elif way == 2:
                        opt_tour[i+1:j+1]= reversed(opt_tour[i+1:j+1])
                    elif way == 3: 
                        opt_tour[i+1:j+1],opt_tour[j+1:k+1] = reversed(opt_tour[i+1:j+1]),reversed(opt_tour[j+1:k+1])
                    elif way == 4:
                        opt_tour = opt_tour[:i+1] + opt_tour[j+1:k+1] + opt_tour[i+1:j+1] + opt_tour[k+1:]      
                    elif way == 5:
                        temp = opt_tour[:i+1] + opt_tour[j+1:k+1]
                        temp += reversed(opt_tour[i+1:j+1])
                        temp += opt_tour[k+1:]
                        opt_tour = temp
                    elif way == 6:
                        temp = opt_tour[:i+1]
                        temp += reversed(opt_tour[j+1:k+1])
                        temp += opt_tour[i+1:j+1]
                        temp += opt_tour[k+1:]
                        opt_tour = temp
                    elif way == 7:
                        temp = opt_tour[:i+1]
                        temp += reversed(opt_tour[j+1:k+1])
                        temp += reversed(opt_tour[i+1:j+1])
                        temp += opt_tour[k+1:]
                        opt_tour = temp

        if tour_cost(cost, opt_tour) < tour_cost(cost, tour):
                    tour = opt_tour
    
    return tour

# def opt_3(cost, tour):

#     while True:
#         # generate all two adjacent substrings of path
#         for i, j, k in combinations(tour, 3):
#             # yield path
#             dist = cost[i-1,i] + cost[j-1,j] + cost[k-1,k]
        
#             # modify those substrings to be shortest
#             if dist > cost[tour[i-1], tour[j-1]] + cost[i, j] + cost[k-1, k]:
#                 path[i:j] = reversed(path[i:j])
#             elif dist > cost[i-1, i] + cost[j-1, k-1] + cost[j, k]:
#                 path[j:k] = reversed(path[j:k])
#             elif dist > cost[k, i] + cost[j-1, j] + cost[k-1, i-1]:
#                 path[i:k] = reversed(path[i:k])
#             elif dist > cost[i-1, j] + cost[k-1, i] + cost[j-1, k]:
#                 path[i:k] = path[j:k] + path[i:j]
        
#         # short circuit if no changed made
#         post = locs.cost(path)
#         if pre == post:
#             return
#         else:
#             pre = post
    
#     return path

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
    opt3_tour = opt_3(cost, tour, iterations)
    print('3-opt Tour:', opt3_tour)
    print('3-opt Tour Cost:', tour_cost(cost, opt3_tour))
	
    print('Computation Time:',(time.clock() - start_time))
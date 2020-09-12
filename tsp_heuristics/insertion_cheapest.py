import time
import numpy as np
from utils import tour_cost
import random

# def cheapest_insertion_beta(cost_matrix, depot):
#     tour=[]
#     tour.append(depot)
#     if depot == len(cost_matrix)-1:
#         tour.append(depot-1)
#     else:
#         tour.append(depot+1)
#     tour.append(depot)
#     for i in range(0, len(cost_matrix)):
#         # i=i+1
#         if i not in tour:
#             ind=None
#             dist=1e6
#             for j in range(len(tour)-1):
#                 if dist>cost_matrix[tour[j]][i]+cost_matrix[i][tour[j+1]]-cost_matrix[tour[j]][tour[j+1]]:
#                     dist=cost_matrix[tour[j]][i]+cost_matrix[i][tour[j+1]]-cost_matrix[tour[j]][tour[j+1]]
#                     position=j
#             p=[]
#             for k in range(len(tour)):
#                 p.append(tour[k])
#                 if k==position:
#                     p.append(i)
#             tour=p
#     return tour

def cheapest_insertion(cost_matrix, depot, unvisited):
    tour=[depot, depot]
    unvisited.remove(depot)

    # for i in unvisited:
    while len(unvisited) > 0:
        
        dist = 1e6

        for city in unvisited:
            position=None
            for j in range(len(tour)-1):
                d_ = cost_matrix[tour[j]][city]+cost_matrix[city][tour[j+1]]-cost_matrix[tour[j]][tour[j+1]]
                if dist > d_:
                    dist = d_
                    cheapest_city = city
                    position=j+1

        tour.insert(position, cheapest_city)
        unvisited.remove(cheapest_city)


    return tour

if __name__ == "__main__":

    start_time = time.process_time()
    # adj_matrix = distance_matrix(node_array, node_array, p=2)

    # cost_matrix = np.random.random_integers(0,high=100,size=(5,5))
    # print(cost_matrix)
    cost_matrix = np.array([[ 0, 32, 53, 51, 84, 72, 76, 33, 39, 64],
                            [32,  0, 21, 29, 76, 40, 43, 41, 36, 37],
                            [53, 21,  0, 23, 72, 19, 23, 52, 46, 22],
                            [51, 29, 23,  0, 50, 35, 39, 36, 30, 14],
                            [84, 76, 72, 50,  0, 79, 83, 51, 51, 53],
                            [72, 40, 19, 35, 79,  0,  4, 69, 63, 26],
                            [76, 43, 23, 39, 83,  4,  0, 74, 67, 30],
                            [33, 41, 52, 36, 51, 69, 74,  0,  6, 50],
                            [39, 36, 46, 30, 51, 63, 67,  6,  0, 44],
                            [64, 37, 22, 14, 53, 26, 30, 50, 44, 0]])

    # cost = np.array([[ 0, 32, 53, 51, 84, 72, 76, 33, 33, 64],
    #                         [32,  0, 21, 29, 76, 40, 43, 41, 36, 37],
    #                         [53, 21,  0, 23, 72, 19, 23, 52, 46, 22],
    #                         [51, 29, 23,  0, 50, 35, 39, 36, 30, 14],
    #                         [84, 76, 72, 50,  0, 79, 83, 51, 51, 53],
    #                         [72, 40, 19, 35, 79,  0,  4, 69, 63, 26],
    #                         [76, 43, 23, 39, 83,  4,  0, 74, 67, 30],
    #                         [33, 41, 52, 36, 51, 69, 74,  0,  6, 50],
    #                         [33, 36, 46, 30, 51, 63, 67,  6,  0, 44],
    #                         [64, 37, 22, 14, 53, 26, 30, 50, 44, 0]])
    tour = [i for i in range(len(cost_matrix))]
    tour.extend([tour[0]])
    depot = 0
    print('Original Tour:', tour)
    print('Original Tour Cost:', tour_cost(cost_matrix, tour))
    # insertion_tour = cheapest_insertion(cost_matrix, depot)
    unvisited = [i for i in range(len(cost_matrix))]
    insertion_tour = cheapest_insertion(cost_matrix, depot, unvisited)
    insertion_cost = tour_cost(cost_matrix, insertion_tour)
    print('Cheapest Insertion Tour:', insertion_tour)
    print('Cheapest Insertion Tour Cost:', insertion_cost)
	
    print('Computation Time:',(time.process_time() - start_time))
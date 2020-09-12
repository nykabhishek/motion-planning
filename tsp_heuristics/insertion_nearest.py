import time
import numpy as np
from utils import tour_cost

def nearest_city(cost_matrix_, visited_, unvisited_):
    # distances = cost_matrix
    min_length = 1e6
    for city_A in visited_:
        for city_B in unvisited_:
            if city_B not in visited_:
                d = cost_matrix_[city_A, city_B]
                # print(d)
                if  d < min_length:
                    min_length = d
                    nearest_city = city_B

    return nearest_city

def nearest_insertion(cost_matrix, depot, unvisited):

    tour=[depot, depot]
    unvisited.remove(depot)

    while len(unvisited) > 0:

        city = nearest_city(cost_matrix, tour, unvisited)

        if city not in tour:
            dist=1e6
            position=None
            # print('1')
            for j in range(len(tour)-1):
                d_ = cost_matrix[tour[j]][city]+cost_matrix[city][tour[j+1]]-cost_matrix[tour[j]][tour[j+1]]
                if dist > d_:
                    dist = d_
                    position=j+1
                    
            tour.insert(position, city)
            unvisited.remove(city)

    return tour
                    
     
if __name__ == "__main__":

    start_time = time.process_time()
    # adj_matrix = distance_matrix(node_array, node_array, p=2)

    # cost_matrix = np.random.random_integers(0,high=100,size=(5,5))
    # print(cost_matrix)
    cost_matrix = np.array([[ 0, 32, 53, 51, 84, 72, 76, 33, 33, 64],
                            [32,  0, 21, 29, 76, 40, 43, 41, 36, 37],
                            [53, 21,  0, 23, 72, 19, 23, 52, 46, 22],
                            [51, 29, 23,  0, 50, 35, 39, 36, 30, 14],
                            [84, 76, 72, 50,  0, 79, 83, 51, 51, 53],
                            [72, 40, 19, 35, 79,  0,  4, 69, 63, 26],
                            [76, 43, 23, 39, 83,  4,  0, 74, 67, 30],
                            [33, 41, 52, 36, 51, 69, 74,  0,  6, 50],
                            [33, 36, 46, 30, 51, 63, 67,  6,  0, 44],
                            [64, 37, 22, 14, 53, 26, 30, 50, 44, 0]])

    cost = np.array([[ 0, 32, 53, 51, 84, 72, 76, 33, 33, 64],
                            [32,  0, 21, 29, 76, 40, 43, 41, 36, 37],
                            [53, 21,  0, 23, 72, 19, 23, 52, 46, 22],
                            [51, 29, 23,  0, 50, 35, 39, 36, 30, 14],
                            [84, 76, 72, 50,  0, 79, 83, 51, 51, 53],
                            [72, 40, 19, 35, 79,  0,  4, 69, 63, 26],
                            [76, 43, 23, 39, 83,  4,  0, 74, 67, 30],
                            [33, 41, 52, 36, 51, 69, 74,  0,  6, 50],
                            [33, 36, 46, 30, 51, 63, 67,  6,  0, 44],
                            [64, 37, 22, 14, 53, 26, 30, 50, 44, 0]])
    tour = [i for i in range(len(cost_matrix))]
    tour.extend([tour[0]])
    depot = 0
    print('Original Tour:', tour)
    print('Original Tour Cost:', tour_cost(cost_matrix, tour))
    unvisited = [i for i in range(len(cost_matrix))]
    insertion_tour = nearest_insertion(cost_matrix, depot, unvisited)
    insertion_cost = tour_cost(cost, insertion_tour)
    print('Nearest Insertion Tour:', insertion_tour)
    print('Nearest Insertion Tour Cost:', insertion_cost)
	
    print('Computation Time:',(time.process_time() - start_time))
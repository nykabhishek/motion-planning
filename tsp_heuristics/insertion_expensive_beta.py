import time
import numpy as np
from utils import tour_cost

def cheapest_insertion(cost_matrix, depot):
    tour=[]
    tour.append(0)
    tour.append(1)
    tour.append(2)
    tour.append(0)
    for i in range(1, len(cost_matrix)):
        # i=i+1
        if i not in tour:
            ind=None
            dist=-1e6
            for j in range(len(tour)-1):
                if dist<cost_matrix[tour[j]][i]+cost_matrix[i][tour[j+1]]-cost_matrix[tour[j]][tour[j+1]]:
                    dist=cost_matrix[tour[j]][i]+cost_matrix[i][tour[j+1]]-cost_matrix[tour[j]][tour[j+1]]
                    ind=j
            p=[]
            for k in range(len(tour)):
                p.append(tour[k])
                if k==ind:
                    p.append(i)
            tour=p
    return tour


if __name__ == "__main__":

    start_time = time.clock()
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
    depot = 9
    print('Original Tour:', tour)
    print('Original Tour Cost:', tour_cost(cost_matrix, tour))
    insertion_tour = cheapest_insertion(cost_matrix, depot)
    insertion_cost = tour_cost(cost, insertion_tour)
    print('Nearest Neighbour Tour:', insertion_tour)
    print('Nearest Neighbour Tour Cost:', insertion_cost)
	
    print('Computation Time:',(time.clock() - start_time))
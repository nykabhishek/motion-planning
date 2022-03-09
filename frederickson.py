import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
import time
from itertools import chain
from tsp_heuristics.christofides import Christofides

def frederickson(adj_matrix, vehicles, depot):
    tsp_tour, tsp_nodes, tsp_cost = Christofides(adj_matrix)

    depot_index = tsp_nodes.index(depot)
    
    ordered_tsp_nodes = [i for i in tsp_nodes if tsp_nodes.index(i)>depot_index-1]
    ordered_tsp_nodes.extend([i for i in tsp_nodes if tsp_nodes.index(i)<depot_index])
    print(ordered_tsp_nodes)

    inter_city_cost = np.zeros(len(ordered_tsp_nodes))
    for i in range(len(ordered_tsp_nodes)):
        inter_city_cost[i] = adj_matrix[depot, ordered_tsp_nodes[i]]
    
    c_max = max(inter_city_cost)
    L = tsp_cost

    print(c_max)

    break_indices = np.full(vehicles-1, [depot])
    path_cost = 0
  
    # for i in range(vehicles-2):
    j=0
    for i in range(len(ordered_tsp_nodes)):
        path_cost = path_cost + adj_matrix[ordered_tsp_nodes[i], ordered_tsp_nodes[i+1]]
        if(path_cost > (((j+1)/vehicles)*(L-2*c_max))+c_max):
            break_indices[j] = i
            j = j+1
            if (j==(vehicles-1)):
                break
    
    veh_tours = []
    start = 0
    end = 0
    for k in range(vehicles):
        if k==0:
            end = break_indices[k]
            tour = list(chain(ordered_tsp_nodes[start:end], [ordered_tsp_nodes[0]]))
            print(tour)
            veh_tours.append(tour)
            start = end
        elif k>0 and k<vehicles-1:
            end = break_indices[k]
            tour = list(chain([ordered_tsp_nodes[0]], ordered_tsp_nodes[start:end], [ordered_tsp_nodes[0]]))
            print(tour)
            veh_tours.append(tour)
            start = end
        elif k>vehicles-2:
            end = len(ordered_tsp_nodes)
            tour = list(chain([ordered_tsp_nodes[0]], ordered_tsp_nodes[start:end], [ordered_tsp_nodes[0]]))
            print(tour)
            veh_tours.append(tour)



if __name__ == "__main__":
    
    # node_array = np.random.random_integers(0,high=10,size=(10,2))
    node_array = np.array([ [0,0],
                            [1,1],
                            [4,0],
                            [5,2],
                            [10,10],
                            [2,8],
                            [8,4],
                            [7,9],
                            [5,8],
                            [3,7]])

    start_time = time.clock()
    # adj_matrix = distance_matrix(node_array, node_array, p=2)

    adj_matrix = np.random.random_integers(0,high=100,size=(100,100))


    vehicles = 7
    depot = 9
    tsp_tours = frederickson(adj_matrix, vehicles, depot)
	
    print('Computation Time:',(time.clock() - start_time))

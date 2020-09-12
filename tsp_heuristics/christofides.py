import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
import time

def Christofides(adj_matrix):
    
    G = nx.from_numpy_array(adj_matrix)

    mst_G = nx.minimum_spanning_tree(G)

    odd_deg_nodes = [node for (node, val) in mst_G.degree() if val%2==1 ]

    odd_deg_nodes_ix = np.ix_(odd_deg_nodes, odd_deg_nodes)
    G_ = nx.from_numpy_array(-1 * adj_matrix[odd_deg_nodes_ix])

    min_weight_matching = nx.max_weight_matching(G_, maxcardinality=True)
    min_weight_matching_edges = [edge for edge in min_weight_matching]

    euler_multigraph = nx.MultiGraph(mst_G)
    for edge in min_weight_matching:
        euler_multigraph.add_edge(odd_deg_nodes[edge[0]], odd_deg_nodes[edge[1]],
                                  weight=adj_matrix[odd_deg_nodes[edge[0]]][odd_deg_nodes[edge[1]]])

    # nx.draw(euler_multigraph, with_labels=True, font_weight='bold')
    # plt.show()

    multi_visit_nodes = [node for (node, val) in euler_multigraph.degree() if val>2 ]

    eulerian_walk = nx.eulerian_path(euler_multigraph)
    eulerian_walk_nodes = [v for (u,v) in nx.eulerian_path(euler_multigraph)]
    
    for node in multi_visit_nodes:
        indices = [i for i, x in enumerate(eulerian_walk_nodes) if x == node]
        for j in range(1, len(indices)):
            del eulerian_walk_nodes[indices[j]]


    tsp_tour_cost = 0
    tsp_tour = nx.DiGraph()
    for i in range(len(eulerian_walk_nodes)):
        if i<len(eulerian_walk_nodes)-1:
            tsp_tour.add_edge(eulerian_walk_nodes[i],eulerian_walk_nodes[i+1],weight = adj_matrix[eulerian_walk_nodes[i], eulerian_walk_nodes[i+1]])
            tsp_tour_cost = tsp_tour_cost + adj_matrix[eulerian_walk_nodes[i], eulerian_walk_nodes[i+1]] 
        else:
            tsp_tour.add_edge(eulerian_walk_nodes[i],eulerian_walk_nodes[0],weight = adj_matrix[eulerian_walk_nodes[i], eulerian_walk_nodes[0]])
            tsp_tour_cost = tsp_tour_cost + adj_matrix[eulerian_walk_nodes[i], eulerian_walk_nodes[0]]

    return tsp_tour, eulerian_walk_nodes, tsp_tour_cost

if __name__ == "__main__":
    
    # node_array = np.random.random_integers(0,high=100,size=(10,2))

    cost_matrix = np.array([[ 0, 32, 53, 51, 84, 72, 76, 33, 33, 64],
                            [32,  0, 21, 29, 76, 40, 43, 41, 36, 37],
                            [53, 21,  0, 23, 72, 19, 23, 52, 46, 22],
                            [51, 29, 23,  0, 50, 35, 39, 36, 30, 14],
                            [84, 76, 72, 50,  0, 79, 83, 51, 51, 53],
                            [72, 40, 19, 35, 79,  0,  4, 69, 63, 26],
                            [76, 43, 23, 39, 83,  4,  0, 74, 67, 30],
                            [33, 41, 52, 36, 51, 69, 74,  0,  6, 50],
                            [33, 36, 46, 30, 51, 63, 67,  6,  0, 44],
                            [64, 37, 22, 14, 53, 26, 30,  50, 44, 0]])

    start_time = time.clock()
    # adj_matrix = distance_matrix(node_array, node_array, p=2)

    
    tsp_tour, eulerian_walk_nodes, tsp_tour_cost = Christofides(cost_matrix)
	
    print('Computation Time:',(time.clock() - start_time))
    # print('Adjacency Weight Matrix:', adj_matrix)
    print('TSP tour =',eulerian_walk_nodes)
    print('TSP Tour Cost:',tsp_tour_cost)
    
    nx.draw(tsp_tour, with_labels=True, font_weight='bold')
    plt.show()
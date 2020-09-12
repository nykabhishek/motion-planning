import numpy as np

def tour_cost(cost_, tour):
    cost=0
    for i in range(len(tour)-1):
        cost = cost+(cost_[tour[i], tour[i+1]])
    return cost

def nearest_unvisited(cost_matrix, city):
    costs = cost_matrix
    # for i in range(cost_matrix):
    #     # if i not in to_be_visited:
    #         costs.delete(i)

    costs[:,city] = 1e6   
    nearest_city = np.argmin(costs[city])
    return nearest_city
import numpy as np

def tour_cost(cost_, tour):
    cost=0
    for i in range(len(tour)-1):
        cost = cost+(cost_[tour[i], tour[i+1]])
    return cost

def nearest_unvisited(cost_matrix, city):
    costs = cost_matrix.copy()
    costs[:,city] = np.inf
    nearest_city = np.argmin(costs[city])
    return nearest_city
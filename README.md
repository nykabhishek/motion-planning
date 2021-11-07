# motion-planning

Heuristics and algorithms for the Travelling Salesman Problem (TSP) and Vehicle Routing Problem.

## Insertion Heuristics
- Cheapest Insertion
- Nearest Insertion
- Farthest Insertion

## Local Optimizers
- 2-opt
- 3-opt

## Greedy Heuristics
- Nearest Neighbour

## TSP Approximation Heuristics
- Christophedes (A factor of 3/2 of the optimal solution length)

    **Steps of algorithm:**

    1. Find a minimum spanning tree **(T)**
    2. Find vertexes in **T** with odd degree **(O)**
    3. Find minimum weight matching **(M)** edges to **T**
    4. Build an Eulerian circuit using the edges of **M** and **T**
    5. Make a Hamiltonian circuit by skipping repeated vertexes


## MinMax VRP Heuristics
- Fredericksons approximations

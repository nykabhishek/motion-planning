# motion-planning

[![CodeFactor](https://www.codefactor.io/repository/github/nykabhishek/motion-planning/badge)](https://www.codefactor.io/repository/github/nykabhishek/motion-planning)

A Python library of construction heuristics, local-search optimisers, and approximation algorithms for the **Travelling Salesman Problem (TSP)** and **multi-vehicle routing (mTSP/VRP)**.

---

## Table of contents

- [Algorithms](#algorithms)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running the tests](#running-the-tests)
- [Data](#data)

---

## Algorithms

### Construction heuristics

These build an initial tour from scratch.

| Algorithm | Module | Function | Complexity |
|---|---|---|---|
| Nearest Neighbour | `tsp_heuristics/nearest_neighbour.py` | `nn(cost_matrix, depot)` | O(n²) |
| Nearest Insertion | `tsp_heuristics/insertion_nearest.py` | `nearest_insertion(cost_matrix, depot, unvisited)` | O(n²) |
| Cheapest Insertion | `tsp_heuristics/insertion_cheapest.py` | `cheapest_insertion(cost_matrix, depot, unvisited)` | O(n²) |
| Farthest Insertion | `tsp_heuristics/insertion_farthest.py` | `farthest_insertion(cost_matrix, depot, unvisited)` | O(n²) |

**Nearest Neighbour** — greedily travels to the closest unvisited city at each step. Fast but can produce poor tours when the last few cities are far apart.

**Nearest Insertion** — maintains a partial tour and repeatedly finds the unvisited city closest to any city already in the tour, inserting it at the cheapest position.

**Cheapest Insertion** — at each step finds the unvisited city whose cheapest insertion cost across all positions in the current tour is globally minimal.

**Farthest Insertion** — similar to cheapest insertion but always picks the unvisited city *farthest* from the current tour, which tends to build a better outer boundary first.

---

### Local-search optimisers

These improve an existing tour by exploring neighbourhood swaps.

| Algorithm | Module | Function | Complexity per iteration |
|---|---|---|---|
| 2-opt | `tsp_heuristics/2_opt.py` | `two_opt(cost, tour, iterations)` | O(n²) |
| 3-opt | `tsp_heuristics/3_opt.py` | `opt_3(cost, tour, iterations)` | O(n³) |

**2-opt** — repeatedly removes two edges and reconnects the tour in the only other valid way. Continues for the specified number of full passes over all edge pairs.

**3-opt** — considers all triples of edges and all seven non-trivial reconnection patterns (ways 1–7). Selects the single best improvement per triple and applies it. Subsumes all 2-opt moves.

---

### TSP approximation

| Algorithm | Module | Function | Approximation ratio |
|---|---|---|---|
| Christofides | `tsp_heuristics/christofides.py` | `Christofides(adj_matrix)` | ≤ 3/2 optimal |

**Christofides algorithm** — guarantees a tour within 3/2 of the optimal length on metric instances. Steps:

1. Compute a minimum spanning tree **T** of the graph.
2. Collect the odd-degree vertices **O** of **T**.
3. Find a minimum-weight perfect matching **M** on the subgraph induced by **O**.
4. Combine **T** and **M** into an Eulerian multigraph and find an Eulerian circuit.
5. Shortcut repeated vertices to obtain a Hamiltonian cycle.

Returns `(tour_graph, node_list, tour_cost)`.

---

### Multi-vehicle routing (mTSP)

| Algorithm | Module | Function |
|---|---|---|
| Frederickson's heuristic | `frederickson.py` | `frederickson(adj_matrix, vehicles, depot)` |

**Frederickson's heuristic** — solves the *minmax* mTSP: distributes a Christofides TSP tour among `vehicles` agents so the longest individual route is minimised. Returns a list of per-vehicle tours, each starting and ending at `depot`.

---

## Project structure

```
motion-planning/
├── frederickson.py              # Frederickson minmax mTSP heuristic
├── tsp_heuristics/
│   ├── utils.py                 # tour_cost(), nearest_unvisited()
│   ├── nearest_neighbour.py     # Nearest Neighbour construction
│   ├── insertion_nearest.py     # Nearest Insertion construction
│   ├── insertion_cheapest.py    # Cheapest Insertion construction
│   ├── insertion_farthest.py    # Farthest Insertion construction
│   ├── insertion_expensive_beta.py  # Experimental most-expensive insertion
│   ├── 2_opt.py                 # 2-opt local search
│   ├── 3_opt.py                 # 3-opt local search
│   ├── christofides.py          # Christofides approximation algorithm
│   └── LKH_solver.py            # Lin-Kernighan-Helsgott solver wrapper
├── tests/
│   └── test_algorithms.py       # Unit tests (22 tests across all algorithms)
├── requirements.txt             # Python dependencies with minimum version bounds
└── data/
    ├── TSP_data/                # Standard TSPLIB benchmark instances
    └── mTSP/minmax/             # Multi-vehicle benchmark instances
```

---

## Requirements

- Python ≥ 3.8
- numpy ≥ 1.21
- networkx ≥ 2.6
- scipy ≥ 1.7
- matplotlib ≥ 3.4

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/nykabhishek/motion-planning.git
cd motion-planning
pip install -r requirements.txt
```

No package installation is required — the modules are imported directly.

---

## Usage

All algorithms accept a **cost matrix** as a 2-D NumPy array where `cost[i, j]` is the travel cost from city `i` to city `j`. For metric TSP the matrix should be symmetric with zeros on the diagonal.

### Nearest Neighbour

```python
import numpy as np
import sys
sys.path.insert(0, 'tsp_heuristics')

from nearest_neighbour import nn
from utils import tour_cost

cost = np.array([
    [ 0, 32, 53, 51],
    [32,  0, 21, 29],
    [53, 21,  0, 23],
    [51, 29, 23,  0],
])

tour = nn(cost, depot=0)          # e.g. [0, 1, 2, 3, 0]
print(tour_cost(cost, tour))
```

### Insertion heuristics

```python
from insertion_cheapest import cheapest_insertion
from insertion_nearest import nearest_insertion
from insertion_farthest import farthest_insertion

tour = cheapest_insertion(cost, depot=0, unvisited=list(range(len(cost))))
tour = nearest_insertion(cost,  depot=0, unvisited=list(range(len(cost))))
tour = farthest_insertion(cost, depot=0, unvisited=list(range(len(cost))))
```

> **Note:** all insertion functions modify `unvisited` in-place. Pass a fresh copy for each call.

### 2-opt and 3-opt improvement

```python
from nearest_neighbour import nn
from two_opt_module import two_opt   # loaded via importlib for the digit-prefixed filename
import importlib.util, os

def load(path, attr):
    spec = importlib.util.spec_from_file_location(path, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, attr)

two_opt = load('tsp_heuristics/2_opt.py', 'two_opt')
opt_3   = load('tsp_heuristics/3_opt.py', 'opt_3')

initial = nn(cost, depot=0)
improved_2opt = two_opt(cost, initial, iterations=10)
improved_3opt = opt_3(cost, initial, iterations=5)
```

### Christofides

```python
import sys
sys.path.insert(0, 'tsp_heuristics')
from christofides import Christofides

tour_graph, node_order, total_cost = Christofides(cost)
print('Tour:', node_order)
print('Cost:', total_cost)
```

### Frederickson multi-vehicle routing

```python
from frederickson import frederickson

vehicle_tours = frederickson(cost, vehicles=3, depot=0)
for i, tour in enumerate(vehicle_tours):
    print(f'Vehicle {i}: {tour}')
```

### Utility functions

```python
from utils import tour_cost, nearest_unvisited

# Cost of a closed tour
c = tour_cost(cost, [0, 2, 1, 3, 0])

# Index of the nearest unvisited city to city 0
nearest = nearest_unvisited(cost, city=0)
```

---

## Running the tests

```bash
python -m unittest discover -s tests -v
```

Expected output: **22 tests, 0 failures**.

---

## Data

Standard [TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/) benchmark instances are included under `data/TSP_data/` (`.tsp` format). Multi-vehicle benchmark instances with known optimal tours are under `data/mTSP/minmax/`.

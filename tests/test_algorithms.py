"""Unit tests for TSP heuristic algorithms."""

import importlib.util
import os
import sys
import unittest

import numpy as np

# Allow modules inside tsp_heuristics/ to resolve their own bare imports
# (e.g. `from utils import tour_cost`) without a package install.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_HEURISTICS = os.path.join(_ROOT, 'tsp_heuristics')
sys.path.insert(0, _HEURISTICS)
sys.path.insert(0, _ROOT)

from utils import tour_cost, nearest_unvisited          # noqa: E402
from nearest_neighbour import nn                         # noqa: E402
from christofides import Christofides                    # noqa: E402
from insertion_nearest import nearest_insertion          # noqa: E402
from insertion_cheapest import cheapest_insertion        # noqa: E402
from insertion_farthest import farthest_insertion        # noqa: E402


def _load(filename, attr):
    """Import a module from a file whose name starts with a digit."""
    path = os.path.join(_HEURISTICS, filename)
    spec = importlib.util.spec_from_file_location(filename, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, attr)


two_opt = _load('2_opt.py', 'two_opt')
opt_3   = _load('3_opt.py', 'opt_3')


# ---------------------------------------------------------------------------
# Shared test fixtures
# ---------------------------------------------------------------------------

# Standard 10×10 cost matrix used throughout the codebase.
COST = np.array([
    [ 0, 32, 53, 51, 84, 72, 76, 33, 33, 64],
    [32,  0, 21, 29, 76, 40, 43, 41, 36, 37],
    [53, 21,  0, 23, 72, 19, 23, 52, 46, 22],
    [51, 29, 23,  0, 50, 35, 39, 36, 30, 14],
    [84, 76, 72, 50,  0, 79, 83, 51, 51, 53],
    [72, 40, 19, 35, 79,  0,  4, 69, 63, 26],
    [76, 43, 23, 39, 83,  4,  0, 74, 67, 30],
    [33, 41, 52, 36, 51, 69, 74,  0,  6, 50],
    [33, 36, 46, 30, 51, 63, 67,  6,  0, 44],
    [64, 37, 22, 14, 53, 26, 30, 50, 44,  0],
], dtype=float)
N = len(COST)


def _identity_tour(n=N):
    """Return the trivial tour 0→1→…→n-1→0."""
    return list(range(n)) + [0]


def is_valid_tour(tour, n, depot=0):
    """Return True if *tour* is a valid closed Hamiltonian cycle from depot."""
    return (
        len(tour) == n + 1
        and tour[0] == depot
        and tour[-1] == depot
        and sorted(tour[:-1]) == list(range(n))
    )


# ---------------------------------------------------------------------------
# tour_cost
# ---------------------------------------------------------------------------

class TestTourCost(unittest.TestCase):
    def test_three_edge_cycle(self):
        # 0→1→2→0: 32 + 21 + 53 = 106
        self.assertEqual(tour_cost(COST, [0, 1, 2, 0]), 106)

    def test_two_node_round_trip(self):
        cost = np.array([[0., 5.], [5., 0.]])
        self.assertEqual(tour_cost(cost, [0, 1, 0]), 10)

    def test_single_self_loop(self):
        self.assertEqual(tour_cost(COST, [3, 3]), 0)

    def test_does_not_mutate_matrix(self):
        snapshot = COST.copy()
        tour_cost(COST, [0, 1, 2, 0])
        np.testing.assert_array_equal(COST, snapshot)


# ---------------------------------------------------------------------------
# nearest_unvisited (utils)
# ---------------------------------------------------------------------------

class TestNearestUnvisited(unittest.TestCase):
    def test_returns_closest_city(self):
        # Row 0 of COST: [0,32,53,51,84,72,76,33,33,64].
        # After masking column 0, cheapest neighbour is city 1 (cost 32).
        self.assertEqual(nearest_unvisited(COST, 0), 1)

    def test_does_not_mutate_matrix(self):
        snapshot = COST.copy()
        nearest_unvisited(COST, 0)
        np.testing.assert_array_equal(COST, snapshot)


# ---------------------------------------------------------------------------
# Nearest Neighbour
# ---------------------------------------------------------------------------

class TestNearestNeighbour(unittest.TestCase):
    def test_valid_tour_from_depot_0(self):
        self.assertTrue(is_valid_tour(nn(COST, depot=0), N))

    def test_valid_tour_all_depots(self):
        for d in range(N):
            with self.subTest(depot=d):
                self.assertTrue(is_valid_tour(nn(COST, depot=d), N, depot=d))

    def test_does_not_mutate_matrix(self):
        snapshot = COST.copy()
        nn(COST, depot=0)
        np.testing.assert_array_equal(COST, snapshot)

    def test_greedy_choice_small_instance(self):
        # From 0 the greedy path must visit 1 before 2 because cost(0,1)=1 < cost(0,2)=100.
        cost = np.array([[0., 1., 100.], [1., 0., 1.], [100., 1., 0.]])
        self.assertEqual(nn(cost, depot=0), [0, 1, 2, 0])

    def test_two_city_instance(self):
        cost = np.array([[0., 7.], [7., 0.]])
        tour = nn(cost, depot=0)
        self.assertTrue(is_valid_tour(tour, 2))
        self.assertEqual(tour_cost(cost, tour), 14)


# ---------------------------------------------------------------------------
# 2-opt
# ---------------------------------------------------------------------------

class TestTwoOpt(unittest.TestCase):
    def test_valid_tour(self):
        result = two_opt(COST, _identity_tour(), iterations=3)
        self.assertTrue(is_valid_tour(result, N))

    def test_does_not_worsen_tour(self):
        initial = _identity_tour()
        result = two_opt(COST, initial, iterations=5)
        self.assertLessEqual(tour_cost(COST, result), tour_cost(COST, initial))

    def test_improves_suboptimal_tour(self):
        # The identity tour is known to be suboptimal for this cost matrix.
        initial = _identity_tour()
        result = two_opt(COST, initial, iterations=10)
        self.assertLess(tour_cost(COST, result), tour_cost(COST, initial))

    def test_two_city_tour_unchanged(self):
        cost = np.array([[0., 5.], [5., 0.]])
        tour = [0, 1, 0]
        result = two_opt(cost, tour, iterations=1)
        self.assertEqual(tour_cost(cost, result), 10)


# ---------------------------------------------------------------------------
# 3-opt
# ---------------------------------------------------------------------------

class TestThreeOpt(unittest.TestCase):
    def test_valid_tour(self):
        result = opt_3(COST, _identity_tour(), iterations=1)
        self.assertTrue(is_valid_tour(result, N))

    def test_does_not_worsen_tour(self):
        initial = _identity_tour()
        result = opt_3(COST, initial, iterations=1)
        self.assertLessEqual(tour_cost(COST, result), tour_cost(COST, initial))

    def test_result_no_worse_than_two_opt(self):
        # 3-opt subsumes 2-opt moves, so its cost should be ≤ 2-opt on same input.
        initial = _identity_tour()
        cost_2opt = tour_cost(COST, two_opt(COST, initial[:], iterations=3))
        cost_3opt = tour_cost(COST, opt_3(COST, initial[:], iterations=3))
        self.assertLessEqual(cost_3opt, cost_2opt + 1e-9)


# ---------------------------------------------------------------------------
# Nearest insertion
# ---------------------------------------------------------------------------

class TestNearestInsertion(unittest.TestCase):
    def test_valid_tour(self):
        tour = nearest_insertion(COST, depot=0, unvisited=list(range(N)))
        self.assertTrue(is_valid_tour(tour, N))

    def test_cost_is_positive(self):
        tour = nearest_insertion(COST, depot=0, unvisited=list(range(N)))
        self.assertGreater(tour_cost(COST, tour), 0)

    def test_small_three_city_instance(self):
        cost = np.array([[0., 1., 2.], [1., 0., 1.], [2., 1., 0.]])
        tour = nearest_insertion(cost, depot=0, unvisited=[0, 1, 2])
        self.assertTrue(is_valid_tour(tour, 3))

    def test_two_city_instance(self):
        cost = np.array([[0., 7.], [7., 0.]])
        tour = nearest_insertion(cost, depot=0, unvisited=[0, 1])
        self.assertTrue(is_valid_tour(tour, 2))
        self.assertEqual(tour_cost(cost, tour), 14)


# ---------------------------------------------------------------------------
# Cheapest insertion
# ---------------------------------------------------------------------------

class TestCheapestInsertion(unittest.TestCase):
    def test_valid_tour(self):
        tour = cheapest_insertion(COST, depot=0, unvisited=list(range(N)))
        self.assertTrue(is_valid_tour(tour, N))

    def test_cost_is_positive(self):
        tour = cheapest_insertion(COST, depot=0, unvisited=list(range(N)))
        self.assertGreater(tour_cost(COST, tour), 0)

    def test_two_city_instance(self):
        cost = np.array([[0., 5.], [5., 0.]])
        tour = cheapest_insertion(cost, depot=0, unvisited=[0, 1])
        self.assertTrue(is_valid_tour(tour, 2))
        self.assertEqual(tour_cost(cost, tour), 10)

    def test_cost_not_worse_than_nearest(self):
        # Cheapest insertion minimises insertion delta at each step,
        # so it should find a tour competitive with nearest insertion.
        ci = tour_cost(COST, cheapest_insertion(COST, 0, list(range(N))))
        ni = tour_cost(COST, nearest_insertion(COST, 0, list(range(N))))
        # Not a strict bound, but both are reasonable heuristics — within 50%
        self.assertLess(ci, ni * 1.5)


# ---------------------------------------------------------------------------
# Farthest insertion
# ---------------------------------------------------------------------------

class TestFarthestInsertion(unittest.TestCase):
    def test_valid_tour(self):
        tour = farthest_insertion(COST, depot=0, unvisited=list(range(N)))
        self.assertTrue(is_valid_tour(tour, N))

    def test_cost_is_positive(self):
        tour = farthest_insertion(COST, depot=0, unvisited=list(range(N)))
        self.assertGreater(tour_cost(COST, tour), 0)

    def test_small_three_city_instance(self):
        # Farthest from depot (0): city 2 (cost 10) > city 1 (cost 1).
        # Initial tour: [0, 2, 0].  Then insert city 1 cheaply.
        cost = np.array([[0., 1., 10.], [1., 0., 1.], [10., 1., 0.]])
        tour = farthest_insertion(cost, depot=0, unvisited=[0, 1, 2])
        self.assertTrue(is_valid_tour(tour, 3))


# ---------------------------------------------------------------------------
# Christofides
# ---------------------------------------------------------------------------

class TestChristofides(unittest.TestCase):
    def test_returns_all_nodes(self):
        _, nodes, _ = Christofides(COST)
        self.assertEqual(sorted(nodes), list(range(N)))

    def test_tour_cost_is_positive(self):
        _, _, cost = Christofides(COST)
        self.assertGreater(cost, 0)

    def test_reported_cost_matches_nodes(self):
        _, nodes, reported = Christofides(COST)
        recomputed = sum(
            COST[nodes[i], nodes[(i + 1) % len(nodes)]]
            for i in range(len(nodes))
        )
        self.assertAlmostEqual(reported, recomputed)

    def test_does_not_mutate_matrix(self):
        snapshot = COST.copy()
        Christofides(COST)
        np.testing.assert_array_equal(COST, snapshot)

    def test_approximation_ratio(self):
        # Christofides guarantees ≤ 1.5× optimal for metric TSP.
        # As a sanity check, verify it beats the trivially bad identity tour.
        _, nodes, christofides_cost = Christofides(COST)
        identity_cost = tour_cost(COST, _identity_tour())
        self.assertLess(christofides_cost, identity_cost)


if __name__ == '__main__':
    unittest.main(verbosity=2)

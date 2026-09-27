"""
Exercise 8: Travelling Salesman Problem (TSP) using Branch and Bound
Implements state space tree exploration with reduced cost matrix bounding.
"""
import heapq
import math
from typing import List, Tuple, Dict, Any, Optional

INF = float('inf')


class TSPNode:
    """Represents a node in the state space tree for TSP Branch and Bound."""
    def __init__(self, matrix: List[List[float]], path: List[int], bound: float, level: int, node_id: int):
        self.matrix = [row[:] for row in matrix]  # Reduced cost matrix
        self.path = list(path)                    # Current path taken
        self.bound = bound                        # Lower bound cost for this subproblem
        self.level = level                        # Tree level (number of cities visited)
        self.node_id = node_id                    # Unique identifier for tracking

    def __lt__(self, other: 'TSPNode') -> bool:
        # Min-heap priority comparison based on lower bound cost
        if self.bound == other.bound:
            return self.level > other.level  # Prefer deeper node if bounds match
        return self.bound < other.bound


def reduce_matrix(matrix: List[List[float]], n: int) -> Tuple[List[List[float]], float]:
    """
    Reduces the matrix by subtracting row and column minimums.
    Returns the reduced matrix and the total reduction cost added to bound.
    """
    reduced = [row[:] for row in matrix]
    reduction_cost = 0.0

    # Row reduction
    for i in range(n):
        min_val = INF
        for j in range(n):
            if reduced[i][j] < min_val:
                min_val = reduced[i][j]
        
        if min_val != INF and min_val > 0:
            reduction_cost += min_val
            for j in range(n):
                if reduced[i][j] != INF:
                    reduced[i][j] -= min_val

    # Column reduction
    for j in range(n):
        min_val = INF
        for i in range(n):
            if reduced[i][j] < min_val:
                min_val = reduced[i][j]
        
        if min_val != INF and min_val > 0:
            reduction_cost += min_val
            for i in range(n):
                if reduced[i][j] != INF:
                    reduced[i][j] -= min_val

    return reduced, reduction_cost


def solve_tsp_branch_and_bound(adj_matrix: List[List[float]], start_city: int = 0) -> Dict[str, Any]:
    """
    Solves TSP using Least Cost Branch and Bound (LCBB) with Reduced Cost Matrix.
    
    Args:
        adj_matrix: NxN distance matrix where INF/0 represents no self-edge
        start_city: City to start and end the tour (0-indexed)
        
    Returns:
        Dict containing optimal_cost, optimal_path, steps, and execution metrics.
    """
    n = len(adj_matrix)
    if n <= 1:
        return {
            "optimal_cost": 0.0,
            "optimal_path": [0, 0] if n == 1 else [],
            "steps": ["Graph has 1 or fewer cities."],
            "nodes_explored": 0,
            "nodes_generated": 0
        }

    steps = []
    steps.append(f"=== Starting TSP Branch & Bound (Cities: {n}, Start: City {start_city+1}) ===")

    # Format initial matrix with INF on diagonal
    cost_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j or adj_matrix[i][j] < 0:
                row.append(INF)
            else:
                row.append(float(adj_matrix[i][j]))
        cost_matrix.append(row)

    # Initial reduction at root node
    initial_matrix, root_reduction = reduce_matrix(cost_matrix, n)
    node_counter = 1
    root_node = TSPNode(initial_matrix, [start_city], root_reduction, 1, node_counter)

    pq: List[TSPNode] = []
    heapq.heappush(pq, root_node)

    best_cost = INF
    best_path = []
    nodes_explored = 0
    nodes_generated = 1

    steps.append(f"Root Node #1: Initial lower bound = {root_reduction:.2f}")

    while pq:
        current = heapq.heappop(pq)
        nodes_explored += 1

        # Prune if current lower bound exceeds or equals best cost found so far
        if current.bound >= best_cost:
            steps.append(f"Pruned Node #{current.node_id} (Path: {[p+1 for p in current.path]}, Bound: {current.bound:.2f} >= Best: {best_cost:.2f})")
            continue

        curr_city = current.path[-1]

        # If all cities visited, complete the tour by returning to start city
        if current.level == n:
            # Check edge back to start city
            return_cost = current.matrix[curr_city][start_city]
            if return_cost != INF or adj_matrix[curr_city][start_city] != INF:
                actual_cost = current.bound
                if actual_cost < best_cost:
                    best_cost = actual_cost
                    best_path = current.path + [start_city]
                    steps.append(f"[BEST] New Best Solution Found! Node #{current.node_id}: Path = {[p+1 for p in best_path]}, Total Cost = {best_cost:.2f}")
            continue

        # Branching: generate child nodes for all unvisited cities
        for next_city in range(n):
            if next_city not in current.path:
                edge_cost = current.matrix[curr_city][next_city]
                if edge_cost == INF:
                    continue

                # Prepare child matrix:
                # Set row curr_city and col next_city to INF, and edge (next_city -> start_city) to INF if incomplete
                child_matrix = [row[:] for row in current.matrix]
                for k in range(n):
                    child_matrix[curr_city][k] = INF
                    child_matrix[k][next_city] = INF
                child_matrix[next_city][start_city] = INF

                # Reduce child matrix
                reduced_child, child_reduction = reduce_matrix(child_matrix, n)
                child_bound = current.bound + edge_cost + child_reduction

                node_counter += 1
                nodes_generated += 1
                child_node = TSPNode(reduced_child, current.path + [next_city], child_bound, current.level + 1, node_counter)

                path_str = " -> ".join([str(p+1) for p in child_node.path])
                if child_bound < best_cost:
                    heapq.heappush(pq, child_node)
                    steps.append(f"  Generated Node #{node_counter}: Path [{path_str}], Lower Bound = {child_bound:.2f}")
                else:
                    steps.append(f"  Generated Node #{node_counter}: Path [{path_str}], Bound = {child_bound:.2f} (Pruned >= Best: {best_cost:.2f})")

    steps.append("")
    steps.append(f"=== Execution Complete ===")
    steps.append(f"Optimal Path: {' -> '.join([str(p+1) for p in best_path])}")
    steps.append(f"Optimal Cost: {best_cost:.2f}")
    steps.append(f"Total Nodes Explored: {nodes_explored}")
    steps.append(f"Total Nodes Generated: {nodes_generated}")

    return {
        "optimal_cost": best_cost,
        "optimal_path": best_path,
        "steps": steps,
        "nodes_explored": nodes_explored,
        "nodes_generated": nodes_generated
    }


def get_preset_tsp_matrix(preset_name: str) -> Tuple[List[List[float]], List[str]]:
    """Returns preset distance matrices and city names."""
    if preset_name == "4-City Classic":
        cities = ["City A", "City B", "City C", "City D"]
        matrix = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ]
    elif preset_name == "5-City Asymmetric":
        cities = ["Delhi", "Mumbai", "Kolkata", "Chennai", "Bengaluru"]
        matrix = [
            [0, 20, 30, 10, 11],
            [15, 0, 16, 4, 2],
            [3, 5, 0, 2, 4],
            [19, 6, 18, 0, 3],
            [16, 4, 7, 16, 0]
        ]
    elif preset_name == "5-City Symmetric":
        cities = ["Node 1", "Node 2", "Node 3", "Node 4", "Node 5"]
        matrix = [
            [0, 3, 1, 5, 8],
            [3, 0, 6, 7, 9],
            [1, 6, 0, 4, 2],
            [5, 7, 4, 0, 3],
            [8, 9, 2, 3, 0]
        ]
    elif preset_name == "6-City Standard":
        cities = ["City 1", "City 2", "City 3", "City 4", "City 5", "City 6"]
        matrix = [
            [0, 12, 10, 19, 8, 22],
            [12, 0, 3, 7, 6, 15],
            [10, 3, 0, 2, 20, 9],
            [19, 7, 2, 0, 4, 11],
            [8, 6, 20, 4, 0, 17],
            [22, 15, 9, 11, 17, 0]
        ]
    else:  # Default 4-city
        cities = ["A", "B", "C", "D"]
        matrix = [
            [0, 4, 1, 3],
            [4, 0, 2, 1],
            [1, 2, 0, 5],
            [3, 1, 5, 0]
        ]

    return matrix, cities


if __name__ == "__main__":
    matrix, cities = get_preset_tsp_matrix("5-City Asymmetric")
    result = solve_tsp_branch_and_bound(matrix)
    print("Optimal Cost:", result["optimal_cost"])
    print("Optimal Path:", [cities[p] for p in result["optimal_path"]])
    print("\nFirst 15 Execution Steps:")
    for step in result["steps"][:15]:
        print(step)

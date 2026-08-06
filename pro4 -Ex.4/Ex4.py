import heapq
from typing import List, Tuple, Dict

def dijkstra_algorithm(graph: Dict[int, List[Tuple[int, int]]], start: int, n: int):
    """
    Dijkstra's algorithm to find shortest paths from start node.
    
    Args:
        graph: Adjacency list {node: [(neighbor, weight), ...]}
        start: Starting node
        n: Total number of nodes
    
    Returns:
        distances, previous nodes, and step-by-step execution
    """
    # Initialize distances and previous nodes
    distances = [float('inf')] * n
    previous = [-1] * n
    distances[start] = 0
    
    # Priority queue: (distance, node)
    pq = [(0, start)]
    visited = set()
    steps = []
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        steps.append(f"Visit node {current_node} (distance: {current_dist})")
        
        # Check all neighbors
        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in visited:
                new_distance = current_dist + weight
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))
                    steps.append(f"  Update node {neighbor}: distance = {new_distance} (via node {current_node})")
    
    return distances, previous, steps

def get_shortest_path(previous: List[int], start: int, end: int) -> List[int]:
    """Reconstruct shortest path from start to end."""
    if previous[end] == -1 and start != end:
        return []  # No path exists
    
    path = []
    current = end
    while current != -1:
        path.append(current)
        current = previous[current]
    
    return path[::-1]  # Reverse to get path from start to end

# Example usage
if __name__ == "__main__":
    # Example graph: {node: [(neighbor, weight), ...]}
    graph = {
        0: [(1, 4), (2, 2)],
        1: [(2, 1), (3, 5)],
        2: [(3, 8), (4, 10)],
        3: [(4, 2)],
        4: []
    }
    
    n = 5  # Number of nodes (0 to 4)
    start = 0
    
    distances, previous, steps = dijkstra_algorithm(graph, start, n)
    
    print("=== Dijkstra's Algorithm ===")
    print(f"Starting from node {start}")
    print("\nStep-by-step execution:")
    for step in steps:
        print(step)
    
    print(f"\nFinal shortest distances from node {start}:")
    for i in range(n):
        if distances[i] == float('inf'):
            print(f"  Node {i}: No path")
        else:
            path = get_shortest_path(previous, start, i)
            print(f"  Node {i}: distance = {distances[i]}, path = {' -> '.join(map(str, path))}")
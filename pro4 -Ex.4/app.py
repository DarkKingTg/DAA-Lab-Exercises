"""Exercise 4: Dijkstra's Algorithm Visualizer."""
import tkinter as tk
from tkinter import messagebox, ttk
from Ex4 import dijkstra_algorithm, get_shortest_path


def parse_edges(edges_text):
    """Parse edge input in format: 0-1-4, 0-2-2, 1-2-1, ..."""
    edges = []
    graph = {}
    max_node = 0
    
    for edge_str in edges_text.split(","):
        edge_str = edge_str.strip()
        if not edge_str:
            continue
        try:
            parts = edge_str.split("-")
            if len(parts) != 3:
                raise ValueError(f"Invalid edge format: {edge_str}")
            u, v, weight = int(parts[0]), int(parts[1]), int(parts[2])
            edges.append((u, v, weight))
            max_node = max(max_node, u, v)
            
            # Build adjacency list
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            graph[u].append((v, weight))
        except ValueError as e:
            raise ValueError(f"Error parsing edge '{edge_str}': {str(e)}")
    
    return graph, max_node + 1


def run_dijkstra():
    try:
        # Parse input
        graph, n = parse_edges(edges_var.get())
        start_node = int(start_var.get())
        
        if start_node < 0 or start_node >= n:
            raise ValueError(f"Start node must be between 0 and {n-1}")
        
        if not graph:
            raise ValueError("Please enter at least one edge")
        
        # Run Dijkstra's algorithm
        distances, previous, steps = dijkstra_algorithm(graph, start_node, n)
        
        # Display results
        output.delete("1.0", tk.END)
        output.insert(tk.END, f"Dijkstra's Algorithm from node {start_node}:\n\n")
        
        # Show step-by-step execution
        output.insert(tk.END, "Step-by-step execution:\n")
        for i, step in enumerate(steps):
            output.insert(tk.END, f"{i+1}. {step}\n")
        
        output.insert(tk.END, f"\nShortest distances and paths:\n")
        
        # Show final results
        for i in range(n):
            if i in graph or any(i in neighbors for neighbors in graph.values()):
                if distances[i] == float('inf'):
                    output.insert(tk.END, f"Node {i}: No path from {start_node}\n")
                else:
                    path = get_shortest_path(previous, start_node, i)
                    path_str = " -> ".join(map(str, path))
                    output.insert(tk.END, f"Node {i}: distance = {distances[i]}, path = {path_str}\n")
        
        # Update result summary
        reachable = sum(1 for d in distances if d != float('inf'))
        result_var.set(f"Processed {n} nodes, {reachable} reachable from node {start_node}")
        
    except ValueError as e:
        messagebox.showerror("Invalid input", str(e))
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return


root = tk.Tk()
root.title("Exercise 4 - Dijkstra's Algorithm")
root.geometry("800x550")

frame = ttk.Frame(root, padding=18)
frame.pack(fill="both", expand=True)

# Title
ttk.Label(frame, text="Dijkstra's Shortest Path Algorithm", font=("Segoe UI", 18, "bold")).pack(anchor="w")

# Edges input
ttk.Label(frame, text="Graph edges (format: node1-node2-weight, comma separated)").pack(anchor="w", pady=(16, 2))
edges_var = tk.StringVar(value="0-1-4, 0-2-2, 1-2-1, 1-3-5, 2-3-8, 2-4-10, 3-4-2")
ttk.Entry(frame, textvariable=edges_var, width=80).pack(fill="x")

# Start node input
ttk.Label(frame, text="Start node").pack(anchor="w", pady=(10, 2))
start_var = tk.StringVar(value="0")
ttk.Entry(frame, textvariable=start_var, width=10).pack(anchor="w")

# Run button
ttk.Button(frame, text="Find Shortest Paths", command=run_dijkstra).pack(anchor="w", pady=14)

# Result summary
result_var = tk.StringVar()
ttk.Label(frame, textvariable=result_var, font=("Segoe UI", 10, "bold")).pack(anchor="w")

# Output text area
output = tk.Text(frame, height=20, wrap="word", font=("Consolas", 9))
output.pack(fill="both", expand=True, pady=(10, 0))

root.mainloop()

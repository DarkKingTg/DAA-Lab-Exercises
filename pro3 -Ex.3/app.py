"""Exercise 3: Minimum spanning tree comparison GUI."""
import heapq
import tkinter as tk
from tkinter import messagebox, ttk


def mst_kruskal(n, edges):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    selected, cost = [], 0
    for weight, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[rv] = ru; selected.append((u, v, weight)); cost += weight
    return selected, cost


def mst_prim(n, edges):
    graph = [[] for _ in range(n)]
    for weight, u, v in edges:
        graph[u].append((weight, v)); graph[v].append((weight, u))
    heap, visited, selected, cost = [(0, 0, -1)], set(), [], 0
    while heap:
        weight, node, previous = heapq.heappop(heap)
        if node in visited: continue
        visited.add(node); cost += weight
        if previous >= 0: selected.append((previous, node, weight))
        for edge_weight, neighbour in graph[node]:
            if neighbour not in visited: heapq.heappush(heap, (edge_weight, neighbour, node))
    return selected, cost


def run():
    try:
        edges = []
        for part in edges_var.get().split(","):
            u, v, weight = map(int, part.strip().split("-")); edges.append((weight, u, v))
        n = max(max(u, v) for _, u, v in edges) + 1
    except ValueError:
        messagebox.showerror("Invalid graph", "Use edges in the form: 0-1-7, 0-3-5")
        return
    kruskal, kc = mst_kruskal(n, edges); prim, pc = mst_prim(n, edges)
    output.delete("1.0", tk.END)
    fmt = lambda items: "\n".join(f"  {u} - {v}  (weight {w})" for u, v, w in items)
    output.insert(tk.END, f"Kruskal's MST — total cost: {kc}\n{fmt(kruskal)}\n\nPrim's MST — total cost: {pc}\n{fmt(prim)}")


root = tk.Tk(); root.title("Exercise 3 - Minimum Spanning Tree"); root.geometry("760x510")
frame = ttk.Frame(root, padding=18); frame.pack(fill="both", expand=True)
ttk.Label(frame, text="Minimum Spanning Tree Explorer", font=("Segoe UI", 18, "bold")).pack(anchor="w")
ttk.Label(frame, text="Edges: node-node-weight (comma separated; nodes start at 0)").pack(anchor="w", pady=(15, 2))
edges_var = tk.StringVar(value="0-1-7, 0-3-5, 1-2-8, 1-3-9, 1-4-7, 2-4-5, 3-4-15, 3-5-6, 4-5-8, 4-6-9, 5-6-11")
ttk.Entry(frame, textvariable=edges_var).pack(fill="x")
ttk.Button(frame, text="Build MSTs", command=run).pack(anchor="w", pady=14)
output = tk.Text(frame, height=17, wrap="word", font=("Consolas", 10)); output.pack(fill="both", expand=True)
root.mainloop()

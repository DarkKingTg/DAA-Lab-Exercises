"""
Exercise 8: Travelling Salesman Problem using Branch and Bound (Interactive GUI App)
"""
import math
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Dict, Any, Optional
from Ex_8 import solve_tsp_branch_and_bound, get_preset_tsp_matrix, INF


class TSPApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Ex 8: Travelling Salesman Problem - Branch & Bound")
        self.root.geometry("1100x720")
        self.root.configure(bg="#F4F6F9")

        # Color Palette
        self.PRIMARY = "#1E3A8A"      # Navy Blue
        self.SECONDARY = "#2563EB"    # Blue
        self.ACCENT = "#10B981"       # Emerald Green
        self.BG_CARD = "#FFFFFF"
        self.TEXT_COLOR = "#1F2937"

        self.current_matrix = []
        self.current_cities = []

        self._build_ui()
        self.load_preset("5-City Asymmetric")

    def _build_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.PRIMARY)
        header_frame.pack(fill="x")

        title_lbl = tk.Label(
            header_frame,
            text="Travelling Salesman Problem (TSP)",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg=self.PRIMARY
        )
        title_lbl.pack(anchor="w", padx=20, pady=(12, 2))

        subtitle_lbl = tk.Label(
            header_frame,
            text="Branch and Bound Algorithm with Reduced Cost Matrix Lower Bounding",
            font=("Segoe UI", 10),
            fg="#93C5FD",
            bg=self.PRIMARY
        )
        subtitle_lbl.pack(anchor="w", padx=20, pady=(0, 12))

        # Main Layout (Split Left and Right)
        main_frame = tk.Frame(self.root, bg="#F4F6F9", padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="#F4F6F9", width=420)
        left_frame.pack(side="left", fill="both", padx=(0, 10))

        right_frame = tk.Frame(main_frame, bg="#F4F6F9")
        right_frame.pack(side="right", fill="both", expand=True)

        # --- Left Panel: Controls & Matrix Input ---
        control_card = tk.LabelFrame(left_frame, text=" Controls & Input Matrix ", font=("Segoe UI", 11, "bold"),
                                    bg=self.BG_CARD, fg=self.PRIMARY, padx=12, pady=12, relief="groove")
        control_card.pack(fill="x", pady=(0, 10))

        tk.Label(control_card, text="Select Preset Graph:", font=("Segoe UI", 9, "bold"), bg=self.BG_CARD).pack(anchor="w")

        self.preset_var = tk.StringVar(value="5-City Asymmetric")
        preset_cb = ttk.Combobox(
            control_card,
            textvariable=self.preset_var,
            values=["4-City Classic", "5-City Asymmetric", "5-City Symmetric", "6-City Standard"],
            state="readonly",
            font=("Segoe UI", 9)
        )
        preset_cb.pack(fill="x", pady=(4, 10))
        preset_cb.bind("<<ComboboxSelected>>", lambda e: self.load_preset(self.preset_var.get()))

        tk.Label(control_card, text="Distance Matrix (comma-separated rows, 0/INF for self):",
                 font=("Segoe UI", 9, "bold"), bg=self.BG_CARD).pack(anchor="w", pady=(5, 2))

        self.matrix_text = tk.Text(control_card, height=7, width=42, font=("Consolas", 9), relief="solid", bd=1)
        self.matrix_text.pack(fill="x", pady=(0, 10))

        btn_frame = tk.Frame(control_card, bg=self.BG_CARD)
        btn_frame.pack(fill="x")

        run_btn = tk.Button(
            btn_frame,
            text="Run Branch & Bound",
            font=("Segoe UI", 10, "bold"),
            bg=self.SECONDARY,
            fg="#FFFFFF",
            activebackground=self.PRIMARY,
            activeforeground="#FFFFFF",
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.run_algorithm
        )
        run_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        reset_btn = tk.Button(
            btn_frame,
            text="Reset",
            font=("Segoe UI", 10),
            bg="#E5E7EB",
            fg=self.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2",
            command=lambda: self.load_preset(self.preset_var.get())
        )
        reset_btn.pack(side="right")

        # Summary Card
        self.summary_card = tk.LabelFrame(left_frame, text=" Optimal Solution Summary ", font=("Segoe UI", 11, "bold"),
                                         bg=self.BG_CARD, fg=self.PRIMARY, padx=12, pady=12, relief="groove")
        self.summary_card.pack(fill="x")

        self.cost_lbl = tk.Label(self.summary_card, text="Optimal Cost: -", font=("Segoe UI", 11, "bold"), fg="#047857", bg=self.BG_CARD)
        self.cost_lbl.pack(anchor="w", pady=2)

        self.path_lbl = tk.Label(self.summary_card, text="Optimal Tour: -", font=("Segoe UI", 9, "bold"), fg=self.TEXT_COLOR, bg=self.BG_CARD, wraplength=380, justify="left")
        self.path_lbl.pack(anchor="w", pady=2)

        self.nodes_lbl = tk.Label(self.summary_card, text="Nodes Explored / Generated: -", font=("Segoe UI", 9), fg="#4B5563", bg=self.BG_CARD)
        self.nodes_lbl.pack(anchor="w", pady=2)

        # --- Right Panel: Graph Visualization & Steps Log ---
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill="both", expand=True)

        # Tab 1: Graph Canvas
        tab_graph = ttk.Frame(notebook)
        notebook.add(tab_graph, text="  Optimal Tour Graph  ")

        self.canvas = tk.Canvas(tab_graph, bg="#FFFFFF", highlightthickness=1, highlightbackground="#E5E7EB")
        self.canvas.pack(fill="both", expand=True)

        # Tab 2: Execution Trace
        tab_trace = ttk.Frame(notebook)
        notebook.add(tab_trace, text="  Branch & Bound Execution Log  ")

        self.log_text = tk.Text(tab_trace, font=("Consolas", 9), bg="#1E1E1E", fg="#D4D4D4", relief="flat")
        log_scroll = ttk.Scrollbar(tab_trace, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

    def load_preset(self, preset_name: str):
        matrix, cities = get_preset_tsp_matrix(preset_name)
        self.current_matrix = matrix
        self.current_cities = cities

        # Format matrix for text input
        text_lines = []
        for row in matrix:
            row_str = ", ".join([str(int(x)) if x != INF and x == int(x) else ("INF" if x == INF else str(x)) for x in row])
            text_lines.append(row_str)
        
        self.matrix_text.delete("1.0", tk.END)
        self.matrix_text.insert(tk.END, "\n".join(text_lines))

        self.cost_lbl.config(text="Optimal Cost: -")
        self.path_lbl.config(text="Optimal Tour: -")
        self.nodes_lbl.config(text="Nodes Explored / Generated: -")

        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, f"Loaded preset '{preset_name}'. Click 'Run Branch & Bound' to solve.\n")
        
        self.draw_graph(matrix, cities, None)

    def parse_matrix_from_input(self) -> Tuple[List[List[float]], List[str]]:
        content = self.matrix_text.get("1.0", tk.END).strip()
        if not content:
            raise ValueError("Distance matrix text box is empty.")

        lines = [line.strip() for line in content.split("\n") if line.strip()]
        n = len(lines)
        if n < 2:
            raise ValueError("Matrix must have at least 2 rows.")

        matrix = []
        for i, line in enumerate(lines):
            parts = [p.strip() for p in line.split(",") if p.strip()]
            if len(parts) != n:
                raise ValueError(f"Row {i+1} has {len(parts)} columns, expected {n}.")
            
            row = []
            for val in parts:
                val_upper = val.upper()
                if val_upper in ("INF", "INF.", "9999", "99999", "X", "-"):
                    row.append(INF)
                else:
                    try:
                        num = float(val)
                        if num == 0:
                            row.append(INF)  # Self loops or 0 cost handled as INF
                        else:
                            row.append(num)
                    except ValueError:
                        raise ValueError(f"Invalid distance value '{val}' in Row {i+1}.")
            matrix.append(row)

        cities = [f"City {i+1}" for i in range(n)]
        return matrix, cities

    def run_algorithm(self):
        try:
            matrix, cities = self.parse_matrix_from_input()
            self.current_matrix = matrix
            self.current_cities = cities

            result = solve_tsp_branch_and_bound(matrix, start_city=0)

            opt_cost = result["optimal_cost"]
            opt_path = result["optimal_path"]
            steps = result["steps"]

            # Update UI Log
            self.log_text.delete("1.0", tk.END)
            for step in steps:
                self.log_text.insert(tk.END, step + "\n")

            if opt_cost == INF or not opt_path:
                self.cost_lbl.config(text="Optimal Cost: No valid tour")
                self.path_lbl.config(text="Optimal Tour: N/A")
                messagebox.showwarning("No Solution", "No valid TSP tour found for the input matrix.")
                return

            city_path = [cities[idx] for idx in opt_path]
            path_str = " -> ".join(city_path)

            self.cost_lbl.config(text=f"Optimal Cost: {opt_cost:.2f}")
            self.path_lbl.config(text=f"Optimal Tour: {path_str}")
            self.nodes_lbl.config(text=f"Explored: {result['nodes_explored']} | Generated: {result['nodes_generated']}")

            self.draw_graph(matrix, cities, opt_path)

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Execution Error", f"An unexpected error occurred:\n{str(e)}")

    def draw_graph(self, matrix: List[List[float]], cities: List[str], optimal_path: Optional[List[int]]):
        self.canvas.delete("all")
        self.canvas.update()

        width = self.canvas.winfo_width() or 600
        height = self.canvas.winfo_height() or 500

        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) * 0.35

        n = len(cities)
        if n == 0:
            return

        # Calculate node coordinates around a circle
        coords = {}
        for i in range(n):
            angle = (2 * math.pi * i) / n - (math.pi / 2)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            coords[i] = (x, y)

        # Build path edges dictionary for fast lookup: (u, v) -> sequence_index
        tour_edges = {}
        if optimal_path and len(optimal_path) > 1:
            for seq in range(len(optimal_path) - 1):
                u = optimal_path[seq]
                v = optimal_path[seq + 1]
                tour_edges[(u, v)] = seq + 1

        # Draw all non-optimal underlying background edges
        for i in range(n):
            for j in range(n):
                if i != j and matrix[i][j] != INF:
                    if (i, j) not in tour_edges:
                        x1, y1 = coords[i]
                        x2, y2 = coords[j]
                        self.canvas.create_line(x1, y1, x2, y2, fill="#E5E7EB", width=1, dash=(4, 4))

        # Draw optimal tour edges with bold highlights and sequence numbers
        for (u, v), seq in tour_edges.items():
            x1, y1 = coords[u]
            x2, y2 = coords[v]

            # Shorten line slightly so arrows don't collide with node circles
            dx = x2 - x1
            dy = y2 - y1
            dist = math.hypot(dx, dy)
            if dist > 0:
                offset = 25
                x1_adj = x1 + (dx / dist) * offset
                y1_adj = y1 + (dy / dist) * offset
                x2_adj = x2 - (dx / dist) * offset
                y2_adj = y2 - (dy / dist) * offset

                self.canvas.create_line(
                    x1_adj, y1_adj, x2_adj, y2_adj,
                    fill=self.SECONDARY,
                    width=3,
                    arrow=tk.LAST,
                    arrowshape=(12, 15, 5)
                )

                # Draw weight tag near line midpoint
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                cost_val = matrix[u][v]

                self.canvas.create_rectangle(
                    mid_x - 18, mid_y - 10, mid_x + 18, mid_y + 10,
                    fill="#EFF6FF", outline=self.SECONDARY, width=1
                )
                self.canvas.create_text(
                    mid_x, mid_y,
                    text=f"#{seq}: {cost_val:.0f}",
                    font=("Segoe UI", 8, "bold"),
                    fill=self.PRIMARY
                )

        # Draw City Nodes
        node_radius = 22
        for i in range(n):
            x, y = coords[i]
            is_in_tour = False
            if optimal_path and i in optimal_path:
                is_in_tour = True

            node_fill = self.ACCENT if is_in_tour else "#9CA3AF"
            node_outline = "#047857" if is_in_tour else "#4B5563"

            self.canvas.create_oval(
                x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                fill=node_fill, outline=node_outline, width=2.5
            )

            city_name = cities[i]
            self.canvas.create_text(
                x, y,
                text=city_name,
                font=("Segoe UI", 9, "bold"),
                fill="#FFFFFF"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = TSPApp(root)
    root.mainloop()

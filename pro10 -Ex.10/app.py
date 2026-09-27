"""
Exercise 10: Improving Quicksort using Randomized Algorithm (Interactive GUI App)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random
from Ex_10 import (
    run_quicksort, compare_quicksort_variants, generate_benchmark_data
)


class QuicksortApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Ex 10: Improving Quicksort using Randomized Algorithm")
        self.root.geometry("1120x740")
        self.root.configure(bg="#F4F6F9")

        # Color Palette
        self.PRIMARY = "#4C1D95"      # Deep Purple
        self.SECONDARY = "#6D28D9"    # Violet Accent
        self.ACCENT = "#10B981"       # Emerald Green
        self.BG_CARD = "#FFFFFF"
        self.TEXT_COLOR = "#1F2937"

        self.current_array = []
        self._build_ui()
        self.load_preset("Worst-Case Sorted Array")

    def _build_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.PRIMARY)
        header_frame.pack(fill="x")

        title_lbl = tk.Label(
            header_frame,
            text="Improving Quicksort via Randomized Pivot Selection",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg=self.PRIMARY
        )
        title_lbl.pack(anchor="w", padx=20, pady=(12, 2))

        subtitle_lbl = tk.Label(
            header_frame,
            text="Eliminating O(n²) Worst-Case Degradation on Sorted & Structured Inputs",
            font=("Segoe UI", 10),
            fg="#DDD6FE",
            bg=self.PRIMARY
        )
        subtitle_lbl.pack(anchor="w", padx=20, pady=(0, 12))

        # Main Layout (Left: Controls, Right: Visuals & Data)
        main_frame = tk.Frame(self.root, bg="#F4F6F9", padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="#F4F6F9", width=420)
        left_frame.pack(side="left", fill="both", padx=(0, 10))

        right_frame = tk.Frame(main_frame, bg="#F4F6F9")
        right_frame.pack(side="right", fill="both", expand=True)

        # --- Left Panel: Controls & Input ---
        control_card = tk.LabelFrame(left_frame, text=" Dataset & Algorithm Options ", font=("Segoe UI", 11, "bold"),
                                    bg=self.BG_CARD, fg=self.PRIMARY, padx=12, pady=12, relief="groove")
        control_card.pack(fill="x", pady=(0, 10))

        tk.Label(control_card, text="Preset Dataset Generator:", font=("Segoe UI", 9, "bold"), bg=self.BG_CARD).pack(anchor="w")
        self.preset_var = tk.StringVar(value="Worst-Case Sorted Array")
        preset_cb = ttk.Combobox(
            control_card,
            textvariable=self.preset_var,
            values=["Worst-Case Sorted Array", "Reverse Sorted Array", "Random Unsorted Array", "Array with Duplicates", "Custom Input"],
            state="readonly",
            font=("Segoe UI", 9)
        )
        preset_cb.pack(fill="x", pady=(3, 8))
        preset_cb.bind("<<ComboboxSelected>>", lambda e: self.load_preset(self.preset_var.get()))

        # Size slider
        size_frame = tk.Frame(control_card, bg=self.BG_CARD)
        size_frame.pack(fill="x", pady=(0, 6))
        tk.Label(size_frame, text="Array Size (N):", font=("Segoe UI", 9, "bold"), bg=self.BG_CARD).pack(side="left")
        self.size_val_lbl = tk.Label(size_frame, text="100", font=("Segoe UI", 9, "bold"), fg=self.SECONDARY, bg=self.BG_CARD)
        self.size_val_lbl.pack(side="right")

        self.size_scale = ttk.Scale(control_card, from_=10, to=250, value=100, command=self._on_scale_change)
        self.size_scale.pack(fill="x", pady=(0, 8))

        tk.Label(control_card, text="Custom Array Elements (comma-separated):", font=("Segoe UI", 9, "bold"), bg=self.BG_CARD).pack(anchor="w")
        self.array_entry = tk.Entry(control_card, font=("Consolas", 9), relief="solid", bd=1)
        self.array_entry.pack(fill="x", pady=(3, 8))

        tk.Label(control_card, text="Select Quicksort Variant:", font=("Segoe UI", 9, "bold"), bg=self.BG_CARD).pack(anchor="w")
        self.alg_var = tk.StringVar(value="Compare All Quicksort Variants")
        alg_cb = ttk.Combobox(
            control_card,
            textvariable=self.alg_var,
            values=[
                "Compare All Quicksort Variants",
                "Randomized Quicksort (Random Pivot)",
                "Randomized Quicksort (Median-of-3)",
                "Deterministic (First Element Pivot)",
                "Deterministic (Last Element Pivot)"
            ],
            state="readonly",
            font=("Segoe UI", 9)
        )
        alg_cb.pack(fill="x", pady=(3, 10))

        run_btn = tk.Button(
            control_card,
            text="Analyze Quicksort Performance",
            font=("Segoe UI", 10, "bold"),
            bg=self.SECONDARY,
            fg="#FFFFFF",
            activebackground=self.PRIMARY,
            activeforeground="#FFFFFF",
            relief="flat",
            pady=6,
            cursor="hand2",
            command=self.run_analysis
        )
        run_btn.pack(fill="x", pady=(4, 0))

        # Metrics Card
        self.metrics_card = tk.LabelFrame(left_frame, text=" Performance Metrics ", font=("Segoe UI", 11, "bold"),
                                         bg=self.BG_CARD, fg=self.PRIMARY, padx=12, pady=12, relief="groove")
        self.metrics_card.pack(fill="x")

        self.comps_lbl = tk.Label(self.metrics_card, text="Comparisons: -", font=("Segoe UI", 10, "bold"), fg=self.TEXT_COLOR, bg=self.BG_CARD)
        self.comps_lbl.pack(anchor="w", pady=2)

        self.swaps_lbl = tk.Label(self.metrics_card, text="Swaps: -", font=("Segoe UI", 10), fg="#4B5563", bg=self.BG_CARD)
        self.swaps_lbl.pack(anchor="w", pady=2)

        self.depth_lbl = tk.Label(self.metrics_card, text="Max Recursion Depth: -", font=("Segoe UI", 10, "bold"), fg="#D97706", bg=self.BG_CARD)
        self.depth_lbl.pack(anchor="w", pady=2)

        self.time_lbl = tk.Label(self.metrics_card, text="Execution Time: -", font=("Segoe UI", 9), fg="#047857", bg=self.BG_CARD)
        self.time_lbl.pack(anchor="w", pady=2)

        self.verdict_lbl = tk.Label(self.metrics_card, text="Complexity Verdict: -", font=("Segoe UI", 9, "bold"), fg=self.PRIMARY, bg=self.BG_CARD, wraplength=380, justify="left")
        self.verdict_lbl.pack(anchor="w", pady=2)

        # --- Right Panel Notebook ---
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill="both", expand=True)

        # Tab 1: Array Bar Visualization Canvas
        tab_visual = ttk.Frame(notebook)
        notebook.add(tab_visual, text="  Array Bar Visualization  ")

        self.canvas = tk.Canvas(tab_visual, bg="#FFFFFF", highlightthickness=1, highlightbackground="#E5E7EB")
        self.canvas.pack(fill="both", expand=True)

        # Tab 2: Comparative Analysis Table
        tab_table = ttk.Frame(notebook)
        notebook.add(tab_table, text="  Comparative Benchmark Table  ")

        self.tree = ttk.Treeview(
            tab_table,
            columns=("alg", "comps", "swaps", "depth", "time"),
            show="headings"
        )
        self.tree.heading("alg", text="Quicksort Variant")
        self.tree.heading("comps", text="Comparisons")
        self.tree.heading("swaps", text="Swaps")
        self.tree.heading("depth", text="Max Recursion Depth")
        self.tree.heading("time", text="Time (ms)")

        self.tree.column("alg", width=220, anchor="w")
        self.tree.column("comps", width=110, anchor="center")
        self.tree.column("swaps", width=90, anchor="center")
        self.tree.column("depth", width=130, anchor="center")
        self.tree.column("time", width=100, anchor="center")

        tree_scroll = ttk.Scrollbar(tab_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Tab 3: Execution Trace Log
        tab_log = ttk.Frame(notebook)
        notebook.add(tab_log, text="  Execution Trace Log  ")

        self.log_text = tk.Text(tab_log, font=("Consolas", 9), bg="#1E1E1E", fg="#D4D4D4", relief="flat")
        log_scroll = ttk.Scrollbar(tab_log, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

    def _on_scale_change(self, val):
        size = int(float(val))
        self.size_val_lbl.config(text=str(size))
        if self.preset_var.get() != "Custom Input":
            self.load_preset(self.preset_var.get())

    def load_preset(self, preset_name: str):
        size = int(float(self.size_scale.get()))

        if preset_name == "Worst-Case Sorted Array":
            arr = list(range(1, size + 1))
        elif preset_name == "Reverse Sorted Array":
            arr = list(range(size, 0, -1))
        elif preset_name == "Random Unsorted Array":
            arr = [random.randint(1, 1000) for _ in range(size)]
        elif preset_name == "Array with Duplicates":
            arr = [random.choice([10, 25, 50, 75, 100]) for _ in range(size)]
        else:
            arr = [34, 7, 23, 32, 5, 62, 78, 12, 1, 99, 45, 18, 54, 88]

        self.current_array = arr
        arr_str = ", ".join(map(str, arr[:40])) + ("..." if len(arr) > 40 else "")
        self.array_entry.delete(0, tk.END)
        self.array_entry.insert(0, arr_str)

        self.draw_array_bars(arr)

    def parse_array_from_entry(self):
        text = self.array_entry.get().strip()
        if not text:
            raise ValueError("Array input text is empty.")

        # Clean trailing dots if present
        if text.endswith("..."):
            text = text[:-3].strip()

        items = []
        for part in text.split(","):
            part = part.strip()
            if part:
                try:
                    items.append(int(part))
                except ValueError:
                    raise ValueError(f"Invalid integer '{part}' in array input.")

        if not items:
            raise ValueError("Must provide at least 1 element.")
        return items

    def run_analysis(self):
        try:
            if self.preset_var.get() == "Custom Input":
                arr = self.parse_array_from_entry()
            else:
                arr = list(self.current_array)

            self.log_text.delete("1.0", tk.END)
            for item in self.tree.get_children():
                self.tree.delete(item)

            selected_alg = self.alg_var.get()

            if selected_alg == "Compare All Quicksort Variants":
                comp_results = compare_quicksort_variants(arr)

                for r in comp_results:
                    self.tree.insert("", "end", values=(
                        r["algorithm"],
                        r["comparisons"],
                        r["swaps"],
                        r["max_depth"],
                        f"{r['time_ms']:.3f}"
                    ))

                # Find randomized vs deterministic first
                rand_res = next(r for r in comp_results if r["pivot_type"] == "randomized")
                det_res = next(r for r in comp_results if r["pivot_type"] == "deterministic_first")

                self.comps_lbl.config(text=f"Randomized Comps: {rand_res['comparisons']} (vs Det: {det_res['comparisons']})")
                self.swaps_lbl.config(text=f"Randomized Swaps: {rand_res['swaps']} (vs Det: {det_res['swaps']})")
                self.depth_lbl.config(text=f"Recursion Depth: {rand_res['max_depth']} (vs Det: {det_res['max_depth']})")
                self.time_lbl.config(text=f"Randomized Time: {rand_res['time_ms']:.3f} ms (vs Det: {det_res['time_ms']:.3f} ms)")

                comp_reduction = ((det_res["comparisons"] - rand_res["comparisons"]) / det_res["comparisons"] * 100) if det_res["comparisons"] > 0 else 0
                if comp_reduction > 20:
                    self.verdict_lbl.config(text=f"✓ Randomized Quicksort reduced comparisons by {comp_reduction:.1f}%! Eliminates O(n²) worst-case recursion depth!")
                else:
                    self.verdict_lbl.config(text="✓ Both variants perform in O(n log n) range on balanced input.")

                self.log_text.insert(tk.END, "=== COMPARATIVE QUICKSORT BENCHMARK ===\n\n")
                for r in comp_results:
                    self.log_text.insert(tk.END, f"--> {r['algorithm']:<42} | Comps: {r['comparisons']:<6} | Depth: {r['max_depth']:<3} | Time: {r['time_ms']:.3f} ms\n")

                self.draw_array_bars(rand_res["sorted_array"])

            else:
                pivot_type_map = {
                    "Randomized Quicksort (Random Pivot)": "randomized",
                    "Randomized Quicksort (Median-of-3)": "randomized_median3",
                    "Deterministic (First Element Pivot)": "deterministic_first",
                    "Deterministic (Last Element Pivot)": "deterministic_last"
                }

                p_type = pivot_type_map.get(selected_alg, "randomized")
                res = run_quicksort(arr, pivot_type=p_type)

                self.comps_lbl.config(text=f"Comparisons: {res['comparisons']}")
                self.swaps_lbl.config(text=f"Swaps: {res['swaps']}")
                self.depth_lbl.config(text=f"Max Recursion Depth: {res['max_depth']}")
                self.time_lbl.config(text=f"Execution Time: {res['time_ms']:.3f} ms")

                n = len(arr)
                if res['max_depth'] >= n * 0.5 and n > 20:
                    self.verdict_lbl.config(text=f"⚠️ WARNING: High recursion depth ({res['max_depth']}) indicates O(n²) worst-case execution!")
                else:
                    self.verdict_lbl.config(text=f"✓ Balanced recursion tree depth ({res['max_depth']}) confirms O(n log n) complexity.")

                for line in res["trace"]:
                    self.log_text.insert(tk.END, line + "\n")

                # Populate table with all variants for context
                comp_results = compare_quicksort_variants(arr)
                for r in comp_results:
                    self.tree.insert("", "end", values=(
                        r["algorithm"],
                        r["comparisons"],
                        r["swaps"],
                        r["max_depth"],
                        f"{r['time_ms']:.3f}"
                    ))

                self.draw_array_bars(res["sorted_array"])

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def draw_array_bars(self, arr):
        self.canvas.delete("all")
        if not arr:
            return

        width = self.canvas.winfo_width() or 600
        height = self.canvas.winfo_height() or 480

        margin_x = 25
        margin_y = 35
        drawable_w = width - 2 * margin_x
        drawable_h = height - 2 * margin_y

        n = len(arr)
        max_val = max(arr) if arr else 1
        bar_w = drawable_w / n

        for i, val in enumerate(arr):
            bar_h = (val / max_val) * drawable_h
            x0 = margin_x + i * bar_w
            x1 = x0 + bar_w - (1 if bar_w > 4 else 0)
            y1 = height - margin_y
            y0 = y1 - bar_h

            # Color gradient based on index / value
            color = self.SECONDARY if i % 2 == 0 else self.PRIMARY

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="" if bar_w < 5 else "#312E81")

            # Draw value text if array is small enough
            if n <= 30 and bar_w >= 16:
                self.canvas.create_text(
                    (x0 + x1) / 2, y0 - 10,
                    text=str(val),
                    font=("Segoe UI", 8, "bold"),
                    fill=self.TEXT_COLOR
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = QuicksortApp(root)
    root.mainloop()
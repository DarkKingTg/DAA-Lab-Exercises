"""
Exercise 9: Effective Bin Packing Algorithms (Interactive GUI App)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random
from Ex_9 import (
    next_fit, first_fit, best_fit, worst_fit,
    first_fit_decreasing, best_fit_decreasing,
    compare_all_bin_packing_algorithms, get_preset_bin_packing
)


class BinPackingApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Ex 9: Effective Bin Packing Algorithms")
        self.root.geometry("1120x740")
        self.root.configure(bg="#F4F6F9")

        # Color Palette
        self.PRIMARY = "#0F766E"      # Teal/Cyan
        self.SECONDARY = "#0D9488"    # Teal Accent
        self.ACCENT = "#F59E0B"       # Amber
        self.BG_CARD = "#FFFFFF"
        self.TEXT_COLOR = "#1F2937"

        # Color palette for stacked item blocks inside bins
        self.ITEM_COLORS = [
            "#3B82F6", "#8B5CF6", "#EC4899", "#10B981", "#F59E0B",
            "#6366F1", "#14B8A6", "#F97316", "#06B6D4", "#84CC16"
        ]

        self._build_ui()
        self.load_preset("Textbook Classic")

    def _build_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.PRIMARY)
        header_frame.pack(fill="x")

        title_lbl = tk.Label(
            header_frame,
            text="Effective Bin Packing Optimization",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg=self.PRIMARY
        )
        title_lbl.pack(anchor="w", padx=20, pady=(12, 2))

        subtitle_lbl = tk.Label(
            header_frame,
            text="Comparison of Next-Fit, First-Fit, Best-Fit, Worst-Fit, FFD, and BFD Heuristics",
            font=("Segoe UI", 10),
            fg="#CCFBF1",
            bg=self.PRIMARY
        )
        subtitle_lbl.pack(anchor="w", padx=20, pady=(0, 12))

        # Main Layout (Left: Controls, Right: Visualization & Results)
        main_frame = tk.Frame(self.root, bg="#F4F6F9", padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="#F4F6F9", width=420)
        left_frame.pack(side="left", fill="both", padx=(0, 10))

        right_frame = tk.Frame(main_frame, bg="#F4F6F9")
        right_frame.pack(side="right", fill="both", expand=True)

        # --- Left Panel Controls ---
        control_card = tk.LabelFrame(left_frame, text=" Configuration & Preset Inputs ", font=("Segoe UI", 11, "bold"),
                                    bg=self.BG_CARD, fg=self.PRIMARY, padx=12, pady=12, relief="groove")
        control_card.pack(fill="x", pady=(0, 10))

        tk.Label(control_card, text="Preset Dataset:", font=("Segoe UI", 9, "bold"), bg=self.BG_CARD).pack(anchor="w")
        self.preset_var = tk.StringVar(value="Textbook Classic")
        preset_cb = ttk.Combobox(
            control_card,
            textvariable=self.preset_var,
            values=["Textbook Classic", "Heavy Cargo", "Small Mixed Items", "Disparate Sizes"],
            state="readonly",
            font=("Segoe UI", 9)
        )
        preset_cb.pack(fill="x", pady=(3, 8))
        preset_cb.bind("<<ComboboxSelected>>", lambda e: self.load_preset(self.preset_var.get()))

        tk.Label(control_card, text="Item Sizes (comma-separated):", font=("Segoe UI", 9, "bold"), bg=self.BG_CARD).pack(anchor="w")
        self.items_entry = tk.Entry(control_card, font=("Consolas", 10), relief="solid", bd=1)
        self.items_entry.pack(fill="x", pady=(3, 8))

        tk.Label(control_card, text="Bin Capacity (C):", font=("Segoe UI", 9, "bold"), bg=self.BG_CARD).pack(anchor="w")
        self.capacity_entry = tk.Entry(control_card, font=("Consolas", 10), relief="solid", bd=1)
        self.capacity_entry.pack(fill="x", pady=(3, 8))

        tk.Label(control_card, text="Select Algorithm:", font=("Segoe UI", 9, "bold"), bg=self.BG_CARD).pack(anchor="w")
        self.alg_var = tk.StringVar(value="First-Fit Decreasing (FFD)")
        alg_cb = ttk.Combobox(
            control_card,
            textvariable=self.alg_var,
            values=[
                "First-Fit Decreasing (FFD)",
                "Best-Fit Decreasing (BFD)",
                "First-Fit (FF)",
                "Best-Fit (BF)",
                "Next-Fit (NF)",
                "Worst-Fit (WF)",
                "Compare All Algorithms"
            ],
            state="readonly",
            font=("Segoe UI", 9)
        )
        alg_cb.pack(fill="x", pady=(3, 10))

        run_btn = tk.Button(
            control_card,
            text="Pack Items into Bins",
            font=("Segoe UI", 10, "bold"),
            bg=self.SECONDARY,
            fg="#FFFFFF",
            activebackground=self.PRIMARY,
            activeforeground="#FFFFFF",
            relief="flat",
            pady=6,
            cursor="hand2",
            command=self.run_bin_packing
        )
        run_btn.pack(fill="x", pady=(4, 0))

        # Metrics Card
        self.metrics_card = tk.LabelFrame(left_frame, text=" Packing Efficiency Summary ", font=("Segoe UI", 11, "bold"),
                                         bg=self.BG_CARD, fg=self.PRIMARY, padx=12, pady=12, relief="groove")
        self.metrics_card.pack(fill="x")

        self.bins_used_lbl = tk.Label(self.metrics_card, text="Bins Used: -", font=("Segoe UI", 11, "bold"), fg="#0F766E", bg=self.BG_CARD)
        self.bins_used_lbl.pack(anchor="w", pady=2)

        self.efficiency_lbl = tk.Label(self.metrics_card, text="Packing Efficiency: -", font=("Segoe UI", 10, "bold"), fg=self.TEXT_COLOR, bg=self.BG_CARD)
        self.efficiency_lbl.pack(anchor="w", pady=2)

        self.wasted_lbl = tk.Label(self.metrics_card, text="Total Wasted Space: -", font=("Segoe UI", 9), fg="#6B7280", bg=self.BG_CARD)
        self.wasted_lbl.pack(anchor="w", pady=2)

        # --- Right Panel Notebook ---
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill="both", expand=True)

        # Tab 1: Visual Bins Canvas
        tab_visual = ttk.Frame(notebook)
        notebook.add(tab_visual, text="  Visual Bin Layout  ")

        self.canvas = tk.Canvas(tab_visual, bg="#FFFFFF", highlightthickness=1, highlightbackground="#E5E7EB")
        canvas_scroll = ttk.Scrollbar(tab_visual, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=canvas_scroll.set)
        canvas_scroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="top", fill="both", expand=True)

        # Tab 2: Execution Trace Log
        tab_log = ttk.Frame(notebook)
        notebook.add(tab_log, text="  Execution Trace Log  ")

        self.log_text = tk.Text(tab_log, font=("Consolas", 9), bg="#1E1E1E", fg="#D4D4D4", relief="flat")
        log_scroll = ttk.Scrollbar(tab_log, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

        # Tab 3: Algorithm Comparison Table
        tab_table = ttk.Frame(notebook)
        notebook.add(tab_table, text="  Algorithm Comparison  ")

        self.tree = ttk.Treeview(
            tab_table,
            columns=("alg", "bins", "packed", "wasted", "efficiency"),
            show="headings"
        )
        self.tree.heading("alg", text="Algorithm Name")
        self.tree.heading("bins", text="Bins Used")
        self.tree.heading("packed", text="Packed Weight")
        self.tree.heading("wasted", text="Wasted Space")
        self.tree.heading("efficiency", text="Efficiency (%)")

        self.tree.column("alg", width=180, anchor="w")
        self.tree.column("bins", width=90, anchor="center")
        self.tree.column("packed", width=110, anchor="center")
        self.tree.column("wasted", width=110, anchor="center")
        self.tree.column("efficiency", width=120, anchor="center")

        tree_scroll = ttk.Scrollbar(tab_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    def load_preset(self, preset_name: str):
        items, cap = get_preset_bin_packing(preset_name)
        items_str = ", ".join([str(x) for x in items])
        self.items_entry.delete(0, tk.END)
        self.items_entry.insert(0, items_str)
        
        self.capacity_entry.delete(0, tk.END)
        self.capacity_entry.insert(0, str(cap))

    def parse_inputs(self):
        items_str = self.items_entry.get().strip()
        cap_str = self.capacity_entry.get().strip()

        if not items_str:
            raise ValueError("Items entry cannot be empty.")
        if not cap_str:
            raise ValueError("Bin capacity entry cannot be empty.")

        try:
            capacity = float(cap_str)
            if capacity <= 0:
                raise ValueError("Bin capacity must be greater than 0.")
        except ValueError:
            raise ValueError("Invalid bin capacity format.")

        items = []
        for p in items_str.split(","):
            p = p.strip()
            if p:
                try:
                    val = float(p)
                    if val <= 0:
                        raise ValueError("All item sizes must be > 0.")
                    items.append(val)
                except ValueError:
                    raise ValueError(f"Invalid item size '{p}'.")

        if not items:
            raise ValueError("At least one valid item is required.")

        return items, capacity

    def run_bin_packing(self):
        try:
            items, capacity = self.parse_inputs()
            selected_alg = self.alg_var.get()

            self.log_text.delete("1.0", tk.END)

            # Clear comparison treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            if selected_alg == "Compare All Algorithms":
                comp_results = compare_all_bin_packing_algorithms(items, capacity)
                best_res = comp_results[0]  # Top ranked algorithm

                # Fill comparison table
                for r in comp_results:
                    self.tree.insert("", "end", values=(
                        r["algorithm"],
                        r["num_bins"],
                        f"{r['total_weight']:.1f}",
                        f"{r['wasted']:.1f}",
                        f"{r['efficiency']:.2f}%"
                    ))

                self.bins_used_lbl.config(text=f"Best Bins Used: {best_res['num_bins']} ({best_res['algorithm']})")
                self.efficiency_lbl.config(text=f"Best Efficiency: {best_res['efficiency']:.2f}%")
                self.wasted_lbl.config(text=f"Wasted Space: {best_res['wasted']:.1f}")

                self.log_text.insert(tk.END, "=== COMPARATIVE BIN PACKING ANALYSIS ===\n\n")
                for r in comp_results:
                    self.log_text.insert(tk.END, f"--> {r['algorithm']:<24}: {r['num_bins']} bins | Efficiency: {r['efficiency']:.2f}%\n")
                
                self.draw_bins(best_res["bins"], capacity, items)

            else:
                if "First-Fit Decreasing" in selected_alg:
                    res = first_fit_decreasing(items, capacity)
                elif "Best-Fit Decreasing" in selected_alg:
                    res = best_fit_decreasing(items, capacity)
                elif "First-Fit" in selected_alg:
                    res = first_fit(items, capacity)
                elif "Best-Fit" in selected_alg:
                    res = best_fit(items, capacity)
                elif "Next-Fit" in selected_alg:
                    res = next_fit(items, capacity)
                else:
                    res = worst_fit(items, capacity)

                for line in res["trace"]:
                    self.log_text.insert(tk.END, line + "\n")

                self.bins_used_lbl.config(text=f"Bins Used: {res['num_bins']}")
                self.efficiency_lbl.config(text=f"Packing Efficiency: {res['efficiency']:.2f}%")
                self.wasted_lbl.config(text=f"Total Wasted Space: {res['wasted']:.1f}")

                # Populate table with all for comparison context
                comp_results = compare_all_bin_packing_algorithms(items, capacity)
                for r in comp_results:
                    self.tree.insert("", "end", values=(
                        r["algorithm"],
                        r["num_bins"],
                        f"{r['total_weight']:.1f}",
                        f"{r['wasted']:.1f}",
                        f"{r['efficiency']:.2f}%"
                    ))

                self.draw_bins(res["bins"], capacity, items)

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def draw_bins(self, bins, capacity: float, original_items):
        self.canvas.delete("all")

        if not bins:
            return

        bin_width = 110
        bin_max_height = 360
        margin_x = 30
        margin_y = 40

        total_width = margin_x + len(bins) * (bin_width + 25) + margin_x
        self.canvas.config(scrollregion=(0, 0, max(total_width, 700), 500))

        scale = bin_max_height / capacity

        for b_idx, b in enumerate(bins):
            x0 = margin_x + b_idx * (bin_width + 25)
            x1 = x0 + bin_width
            y1 = margin_y + bin_max_height
            y0 = margin_y

            # Draw outer container bin frame
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="#374151", width=3, fill="#F9FAFB")
            
            # Bin Header label
            self.canvas.create_text(
                (x0 + x1) / 2, y0 - 15,
                text=f"Bin #{b.bin_id}",
                font=("Segoe UI", 10, "bold"),
                fill=self.PRIMARY
            )

            # Draw stacked items from bottom up
            current_y = y1
            for orig_idx, sz in b.items:
                item_h = sz * scale
                top_y = current_y - item_h

                color = self.ITEM_COLORS[orig_idx % len(self.ITEM_COLORS)]
                self.canvas.create_rectangle(x0 + 3, top_y, x1 - 3, current_y, fill=color, outline="#1F2937", width=1.5)

                # Text inside item block if height allows
                if item_h >= 18:
                    self.canvas.create_text(
                        (x0 + x1) / 2, (top_y + current_y) / 2,
                        text=f"#{orig_idx+1}: {sz:.1f}",
                        font=("Segoe UI", 9, "bold"),
                        fill="#FFFFFF"
                    )

                current_y = top_y

            # Draw unused empty top portion of the bin
            if b.remaining > 0:
                empty_h = b.remaining * scale
                self.canvas.create_rectangle(x0 + 3, y0, x1 - 3, y0 + empty_h, fill="#F3F4F6", outline="", width=0)
                if empty_h >= 16:
                    self.canvas.create_text(
                        (x0 + x1) / 2, y0 + empty_h / 2,
                        text=f"Free: {b.remaining:.1f}",
                        font=("Segoe UI", 8, "italic"),
                        fill="#9CA3AF"
                    )

            # Footer label showing bin capacity usage
            self.canvas.create_text(
                (x0 + x1) / 2, y1 + 18,
                text=f"Used: {b.used_capacity():.1f}/{capacity:.1f}",
                font=("Segoe UI", 9, "bold"),
                fill=self.TEXT_COLOR
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = BinPackingApp(root)
    root.mainloop()

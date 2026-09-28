"""Exercise 1: Interpolation Search visualizer (standard-library GUI)."""
import tkinter as tk
from tkinter import messagebox, ttk


def interpolation_search(values, target):
    values = sorted(values)
    low, high, steps = 0, len(values) - 1, []
    while low <= high and values[low] <= target <= values[high]:
        if values[low] == values[high]:
            steps.append(f"Range {low}..{high}; probe {low} (value {values[low]})")
            return (low if values[low] == target else None), values, steps
        pos = low + int((high - low) * (target - values[low]) / (values[high] - values[low]))
        steps.append(f"Range {low}..{high}; probe {pos} (value {values[pos]})")
        if values[pos] == target:
            return pos, values, steps
        if values[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return None, values, steps


def run():
    try:
        values = [int(item.strip()) for item in array_var.get().split(",") if item.strip()]
        if not values:
            raise ValueError("Enter at least one number.")
        index, ordered, steps = interpolation_search(values, int(target_var.get()))
    except ValueError as error:
        messagebox.showerror("Invalid input", str(error))
        return
    result_var.set(f"Sorted array: {ordered}\n" + (f"Found at index {index}." if index is not None else "Target not found."))
    output.delete("1.0", tk.END)
    output.insert(tk.END, "Search steps:\n\n" + "\n".join(f"{i + 1}. {step}" for i, step in enumerate(steps)))


root = tk.Tk(); root.title("Exercise 1 - Interpolation Search"); root.geometry("720x500")
frame = ttk.Frame(root, padding=18); frame.pack(fill="both", expand=True)
ttk.Label(frame, text="Interpolation Search Visualizer", font=("Segoe UI", 18, "bold")).pack(anchor="w")
ttk.Label(frame, text="Numbers (comma separated)").pack(anchor="w", pady=(16, 2))
array_var = tk.StringVar(value="10, 13, 15, 16, 19, 22, 24, 26, 27, 31, 35")
ttk.Entry(frame, textvariable=array_var).pack(fill="x")
ttk.Label(frame, text="Target number").pack(anchor="w", pady=(10, 2))
target_var = tk.StringVar(value="24")
ttk.Entry(frame, textvariable=target_var).pack(fill="x")
ttk.Button(frame, text="Search", command=run).pack(anchor="w", pady=14)
result_var = tk.StringVar(); ttk.Label(frame, textvariable=result_var, font=("Segoe UI", 10, "bold")).pack(anchor="w")
output = tk.Text(frame, height=12, wrap="word"); output.pack(fill="both", expand=True, pady=(10, 0))
root.mainloop()

"""Exercise 5: MinMax using Divide & Conquer Visualizer."""
import tkinter as tk
from tkinter import messagebox, ttk
from Ex_5 import minmax_wrapper, minmax_naive


def run_minmax():
    try:
        # Parse input array
        array_text = array_var.get().strip()
        if not array_text:
            raise ValueError("Please enter at least one number")
        
        # Convert comma-separated string to list of integers
        array = []
        for item in array_text.split(","):
            item = item.strip()
            if item:
                array.append(int(item))
        
        if len(array) == 0:
            raise ValueError("Please enter at least one number")
        
        # Run divide & conquer algorithm
        min_dc, max_dc, steps = minmax_wrapper(array)
        
        # Run naive algorithm for comparison
        min_naive, max_naive, naive_comparisons = minmax_naive(array)
        
        # Display results
        output.delete("1.0", tk.END)
        output.insert(tk.END, f"MinMax using Divide & Conquer Technique\n")
        output.insert(tk.END, f"Input array: {array}\n")
        output.insert(tk.END, f"Array size: {len(array)}\n\n")
        
        # Show step-by-step execution
        output.insert(tk.END, "Step-by-step execution:\n")
        output.insert(tk.END, "=" * 50 + "\n")
        for i, step in enumerate(steps):
            output.insert(tk.END, f"{i+1}. {step}\n")
        
        output.insert(tk.END, "\n" + "=" * 50 + "\n")
        
        # Show comparison with naive approach
        output.insert(tk.END, f"Algorithm Comparison:\n")
        output.insert(tk.END, f"Divide & Conquer: Min = {min_dc}, Max = {max_dc}\n")
        output.insert(tk.END, f"Naive approach:   Min = {min_naive}, Max = {max_naive}\n")
        output.insert(tk.END, f"Naive comparisons: {naive_comparisons}\n")
        
        # Theoretical analysis
        n = len(array)
        if n > 1:
            dc_comparisons = int(1.5 * n - 2)
            output.insert(tk.END, f"D&C theoretical comparisons: ~{dc_comparisons}\n")
            
            if naive_comparisons > 0:
                efficiency = ((naive_comparisons - dc_comparisons) / naive_comparisons) * 100
                output.insert(tk.END, f"Efficiency improvement: ~{efficiency:.1f}%\n")
        
        # Update result summary
        result_var.set(f"Found: Min = {min_dc}, Max = {max_dc} (Array size: {len(array)})")
        
    except ValueError as e:
        messagebox.showerror("Invalid input", str(e))
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return


def load_example(example_type):
    """Load different example arrays."""
    examples = {
        "small": "3, 5, 1, 9, 8, 2, 7, 4, 6",
        "large": "15, 23, 8, 42, 7, 31, 19, 6, 28, 14, 35, 11, 39, 2, 26",
        "sorted": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
        "reverse": "10, 9, 8, 7, 6, 5, 4, 3, 2, 1"
    }
    array_var.set(examples.get(example_type, examples["small"]))


root = tk.Tk()
root.title("Exercise 5 - MinMax Divide & Conquer")
root.geometry("850x600")

frame = ttk.Frame(root, padding=18)
frame.pack(fill="both", expand=True)

# Title
ttk.Label(frame, text="MinMax using Divide & Conquer", font=("Segoe UI", 18, "bold")).pack(anchor="w")

# Input section
ttk.Label(frame, text="Numbers (comma separated)").pack(anchor="w", pady=(16, 2))
array_var = tk.StringVar(value="3, 5, 1, 9, 8, 2, 7, 4, 6")
entry = ttk.Entry(frame, textvariable=array_var, width=60)
entry.pack(fill="x")

# Example buttons
example_frame = ttk.Frame(frame)
example_frame.pack(fill="x", pady=(5, 0))
ttk.Label(example_frame, text="Examples:").pack(side="left")
ttk.Button(example_frame, text="Small", command=lambda: load_example("small")).pack(side="left", padx=5)
ttk.Button(example_frame, text="Large", command=lambda: load_example("large")).pack(side="left", padx=5)
ttk.Button(example_frame, text="Sorted", command=lambda: load_example("sorted")).pack(side="left", padx=5)
ttk.Button(example_frame, text="Reverse", command=lambda: load_example("reverse")).pack(side="left", padx=5)

# Run button
ttk.Button(frame, text="Find Min & Max", command=run_minmax).pack(anchor="w", pady=14)

# Result summary
result_var = tk.StringVar()
ttk.Label(frame, textvariable=result_var, font=("Segoe UI", 10, "bold")).pack(anchor="w")

# Output text area
output = tk.Text(frame, height=22, wrap="word", font=("Consolas", 9))
output.pack(fill="both", expand=True, pady=(10, 0))

# Add scrollbar
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=output.yview)
scrollbar.pack(side="right", fill="y")
output.configure(yscrollcommand=scrollbar.set)

root.mainloop()
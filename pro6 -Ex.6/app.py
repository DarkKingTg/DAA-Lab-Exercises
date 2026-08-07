"""Exercise 6: Matrix Chain Multiplication using Dynamic Programming."""
import tkinter as tk
from tkinter import messagebox, ttk
from Ex_6 import matrix_chain_wrapper, format_matrix_dimensions


def run_matrix_chain():
    try:
        # Parse input dimensions
        dims_text = dimensions_var.get().strip()
        if not dims_text:
            raise ValueError("Please enter matrix dimensions")
        
        # Convert comma-separated string to list of integers
        dimensions = []
        for item in dims_text.split(","):
            item = item.strip()
            if item:
                dimensions.append(int(item))
        
        if len(dimensions) < 3:
            raise ValueError("Need at least 3 dimensions (for 2 matrices)")
        
        # Run matrix chain multiplication algorithm
        optimal_cost, optimal_parentheses, dp_steps, order_steps = matrix_chain_wrapper(dimensions)
        
        # Display results
        output.delete("1.0", tk.END)
        output.insert(tk.END, "Matrix Chain Multiplication using Dynamic Programming\n")
        output.insert(tk.END, "=" * 60 + "\n\n")
        
        # Show input
        n_matrices = len(dimensions) - 1
        output.insert(tk.END, f"Number of matrices: {n_matrices}\n")
        output.insert(tk.END, f"Matrix dimensions: {format_matrix_dimensions(dimensions)}\n\n")
        
        # Show results summary
        output.insert(tk.END, f"RESULTS:\n")
        output.insert(tk.END, f"Optimal cost: {optimal_cost} scalar multiplications\n")
        output.insert(tk.END, f"Optimal parenthesization: {optimal_parentheses}\n\n")
        
        # Show detailed DP steps
        output.insert(tk.END, "DYNAMIC PROGRAMMING STEPS:\n")
        output.insert(tk.END, "-" * 40 + "\n")
        for step in dp_steps:
            output.insert(tk.END, f"{step}\n")
        
        output.insert(tk.END, "\n" + "=" * 60 + "\n\n")
        
        # Show computation order
        output.insert(tk.END, "OPTIMAL COMPUTATION ORDER:\n")
        output.insert(tk.END, "-" * 40 + "\n")
        for step in order_steps:
            output.insert(tk.END, f"{step}\n")
        
        # Create DP table visualization
        show_dp_table(dimensions)
        
        # Update result summary
        result_var.set(f"Optimal cost: {optimal_cost} multiplications, Matrices: {n_matrices}")
        
    except ValueError as e:
        messagebox.showerror("Invalid input", str(e))
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return


def show_dp_table(dimensions):
    """Display the DP table in a separate window."""
    try:
        from Ex_6 import matrix_chain_multiplication
        
        optimal_cost, dp_table, _ = matrix_chain_multiplication(dimensions)
        n = len(dp_table)
        
        # Create new window for DP table
        table_window = tk.Toplevel(root)
        table_window.title("DP Table Visualization")
        table_window.geometry("600x400")
        
        # Create frame for table
        table_frame = ttk.Frame(table_window, padding=10)
        table_frame.pack(fill="both", expand=True)
        
        ttk.Label(table_frame, text="Dynamic Programming Table", 
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Create treeview for table display
        tree = ttk.Treeview(table_frame)
        tree.pack(fill="both", expand=True)
        
        # Configure columns
        columns = [f"M{i+1}" for i in range(n)]
        tree["columns"] = columns
        tree["show"] = "tree headings"
        
        # Configure column headings
        tree.heading("#0", text="")
        tree.column("#0", width=50, anchor="center")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=80, anchor="center")
        
        # Insert data
        for i in range(n):
            row_values = []
            for j in range(n):
                if i <= j:
                    row_values.append(str(dp_table[i][j]))
                else:
                    row_values.append("-")
            
            tree.insert("", "end", text=f"M{i+1}", values=row_values)
        
        # Add explanation
        explanation = ttk.Label(table_frame, 
                              text="Table shows minimum cost to multiply matrices from row to column",
                              font=("Segoe UI", 10))
        explanation.pack(pady=(10, 0))
        
    except Exception as e:
        messagebox.showerror("Error", f"Could not display DP table: {str(e)}")


def load_example(example_type):
    """Load different example matrix chains."""
    examples = {
        "small": "1, 2, 3, 4, 5",  # 4 matrices: A1(1×2), A2(2×3), A3(3×4), A4(4×5)
        "medium": "5, 4, 6, 2, 7, 3",  # 5 matrices with varying dimensions
        "large": "2, 3, 6, 4, 5, 2, 4, 3",  # 7 matrices
        "textbook": "40, 20, 30, 10, 30"  # Classic textbook example
    }
    dimensions_var.set(examples.get(example_type, examples["small"]))


def show_help():
    """Show help dialog with input format information."""
    help_text = """Matrix Chain Multiplication - Input Format:

Enter matrix dimensions as comma-separated values.

Example: 1, 2, 3, 4, 5
This represents 4 matrices:
• Matrix 1: 1×2
• Matrix 2: 2×3  
• Matrix 3: 3×4
• Matrix 4: 4×5

The algorithm finds the optimal way to parenthesize 
the matrix multiplication to minimize scalar multiplications.

For n matrices, you need n+1 dimension values.
"""
    messagebox.showinfo("Help - Input Format", help_text)


root = tk.Tk()
root.title("Exercise 6 - Matrix Chain Multiplication DP")
root.geometry("900x650")

frame = ttk.Frame(root, padding=18)
frame.pack(fill="both", expand=True)

# Title
ttk.Label(frame, text="Matrix Chain Multiplication using Dynamic Programming", 
          font=("Segoe UI", 18, "bold")).pack(anchor="w")

# Input section
input_frame = ttk.Frame(frame)
input_frame.pack(fill="x", pady=(16, 0))

ttk.Label(input_frame, text="Matrix dimensions (comma separated)").pack(anchor="w", pady=(0, 2))

# Input with help button
entry_frame = ttk.Frame(input_frame)
entry_frame.pack(fill="x")

dimensions_var = tk.StringVar(value="1, 2, 3, 4, 5")
entry = ttk.Entry(entry_frame, textvariable=dimensions_var, width=50)
entry.pack(side="left", fill="x", expand=True)

ttk.Button(entry_frame, text="Help", command=show_help, width=8).pack(side="right", padx=(10, 0))

# Example buttons
example_frame = ttk.Frame(frame)
example_frame.pack(fill="x", pady=(5, 0))

ttk.Label(example_frame, text="Examples:").pack(side="left")
ttk.Button(example_frame, text="Small (4 matrices)", 
           command=lambda: load_example("small")).pack(side="left", padx=5)
ttk.Button(example_frame, text="Medium (5 matrices)", 
           command=lambda: load_example("medium")).pack(side="left", padx=5)
ttk.Button(example_frame, text="Large (7 matrices)", 
           command=lambda: load_example("large")).pack(side="left", padx=5)
ttk.Button(example_frame, text="Textbook Example", 
           command=lambda: load_example("textbook")).pack(side="left", padx=5)

# Control buttons
button_frame = ttk.Frame(frame)
button_frame.pack(fill="x", pady=14)

ttk.Button(button_frame, text="Find Optimal Cost", 
           command=run_matrix_chain).pack(side="left")
ttk.Button(button_frame, text="Show DP Table", 
           command=lambda: show_dp_table([int(x.strip()) for x in dimensions_var.get().split(",") if x.strip()])).pack(side="left", padx=(10, 0))

# Result summary
result_var = tk.StringVar()
ttk.Label(frame, textvariable=result_var, font=("Segoe UI", 10, "bold")).pack(anchor="w")

# Output text area with scrollbar
text_frame = ttk.Frame(frame)
text_frame.pack(fill="both", expand=True, pady=(10, 0))

output = tk.Text(text_frame, height=25, wrap="word", font=("Consolas", 9))
scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=output.yview)

output.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
output.configure(yscrollcommand=scrollbar.set)

# Initial explanation
initial_text = """Matrix Chain Multiplication using Dynamic Programming

This algorithm finds the optimal way to parenthesize a chain of matrix multiplications
to minimize the number of scalar multiplications.

ALGORITHM OVERVIEW:
• Uses dynamic programming to build solutions bottom-up
• dp[i][j] = minimum cost to multiply matrices from i to j
• Tries all possible split points k between i and j
• Recurrence: dp[i][j] = min(dp[i][k] + dp[k+1][j] + cost of multiplying results)

INPUT FORMAT:
• Enter dimensions as: d0, d1, d2, ..., dn
• This represents n matrices: M1(d0×d1), M2(d1×d2), ..., Mn(dn-1×dn)

Click 'Find Optimal Cost' to see the algorithm in action!
"""

output.insert("1.0", initial_text)

root.mainloop()
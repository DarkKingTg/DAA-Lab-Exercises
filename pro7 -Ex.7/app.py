"""Exercise 7: N-Queens Problem using Backtracking."""
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageDraw, ImageTk
from Ex_7 import solve_n_queens, solution_to_board
import io

CELL_SIZE = 50
QUEEN_SYMBOL = "♛"


def create_board_image(solution: list, n: int, cell_size: int = 60) -> ImageTk.PhotoImage:
    """
    Create a visual representation of the N-Queens solution.
    
    Args:
        solution: List where solution[i] is column of queen in row i
        n: Board size
        cell_size: Size of each cell in pixels
    
    Returns:
        PhotoImage object for display
    """
    # Create image
    size = n * cell_size
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # Colors
    light_color = (240, 217, 181)  # Light square
    dark_color = (181, 136, 99)    # Dark square
    queen_color = (255, 215, 0)    # Gold for queen
    
    # Draw board
    for row in range(n):
        for col in range(n):
            x0 = col * cell_size
            y0 = row * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            
            # Alternate colors (chess board pattern)
            if (row + col) % 2 == 0:
                fill_color = light_color
            else:
                fill_color = dark_color
            
            draw.rectangle([x0, y0, x1, y1], fill=fill_color, outline='black', width=2)
            
            # Draw queen if present
            if solution[row] == col:
                # Draw filled circle for queen
                margin = cell_size // 6
                draw.ellipse([x0 + margin, y0 + margin, x1 - margin, y1 - margin], 
                           fill=queen_color, outline='darkgoldenrod', width=3)
                
                # Draw queen symbol in center
                text_x = x0 + cell_size // 2
                text_y = y0 + cell_size // 2
                draw.text((text_x, text_y), QUEEN_SYMBOL, fill='darkred', anchor='mm')
    
    # Convert to PhotoImage
    photo = ImageTk.PhotoImage(img)
    return photo


def run_n_queens():
    try:
        # Get board size
        n = int(n_var.get())
        
        if n <= 0:
            raise ValueError("Board size must be greater than 0")
        
        if n > 12:
            response = messagebox.askyesno("Large board",
                f"Solving for n={n} may take some time. Continue?")
            if not response:
                return
        
        # Show progress
        output.delete("1.0", tk.END)
        output.insert(tk.END, f"Solving {n}-Queens problem...\n")
        root.update()
        
        # Solve N-Queens
        solutions, steps = solve_n_queens(n)
        
        # Display results
        output.delete("1.0", tk.END)
        output.insert(tk.END, f"N-Queens Problem (Backtracking) - Board size: {n}×{n}\n")
        output.insert(tk.END, "=" * 60 + "\n\n")
        
        # Check if solutions exist
        if not solutions:
            output.insert(tk.END, "No solutions found for this board size.\n")
            output.insert(tk.END, "Note: Solutions exist for n=1 and n≥4.\n")
            result_var.set("No solutions exist")
            return
        
        output.insert(tk.END, f"Total solutions found: {len(solutions)}\n\n")
        
        # Show algorithm steps (first 30)
        output.insert(tk.END, "Algorithm Execution (first 30 steps):\n")
        output.insert(tk.END, "-" * 40 + "\n")
        for step in steps[:30]:
            output.insert(tk.END, f"{step}\n")
        
        if len(steps) > 30:
            output.insert(tk.END, f"\n... ({len(steps) - 30} more steps)\n")
        
        output.insert(tk.END, "\n" + "=" * 60 + "\n\n")
        output.insert(tk.END, "Solutions:\n")
        output.insert(tk.END, "-" * 40 + "\n")
        
        # Show all solutions
        for idx, sol in enumerate(solutions):
            output.insert(tk.END, f"Solution {idx + 1}: {sol}\n")
        
        # Update result summary
        result_var.set(f"Found {len(solutions)} solutions for {n}×{n} board")
        
        # Show first solution visually
        if solutions:
            show_solution_visual(solutions[0], n, 0)
            
            # Update solution counter
            solution_counter_var.set(f"Showing solution 1 of {len(solutions)}")
            current_solution['index'] = 0
            current_solution['solutions'] = solutions
            current_solution['n'] = n
        
    except ValueError as e:
        messagebox.showerror("Invalid input", str(e))
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return


def show_solution_visual(solution: list, n: int, index: int):
    """Display visual representation of a solution."""
    try:
        photo = create_board_image(solution, n)
        board_label.config(image=photo)
        board_label.image = photo  # Keep a reference
    except Exception as e:
        messagebox.showerror("Error", f"Could not display board: {str(e)}")


def next_solution():
    """Show next solution."""
    if 'solutions' not in current_solution or not current_solution['solutions']:
        messagebox.showwarning("No solutions", "Run the algorithm first")
        return
    
    index = current_solution.get('index', 0)
    solutions = current_solution['solutions']
    n = current_solution['n']
    
    if index < len(solutions) - 1:
        index += 1
        current_solution['index'] = index
        show_solution_visual(solutions[index], n, index)
        solution_counter_var.set(f"Showing solution {index + 1} of {len(solutions)}")


def prev_solution():
    """Show previous solution."""
    if 'solutions' not in current_solution or not current_solution['solutions']:
        messagebox.showwarning("No solutions", "Run the algorithm first")
        return
    
    index = current_solution.get('index', 0)
    solutions = current_solution['solutions']
    n = current_solution['n']
    
    if index > 0:
        index -= 1
        current_solution['index'] = index
        show_solution_visual(solutions[index], n, index)
        solution_counter_var.set(f"Showing solution {index + 1} of {len(solutions)}")


def show_help():
    """Show help dialog."""
    help_text = """N-Queens Problem - Help

ALGORITHM:
The N-Queens problem asks to place N queens on an N×N chessboard such that no two queens 
attack each other. Queens can attack horizontally, vertically, and diagonally.

BACKTRACKING APPROACH:
1. Place queens row by row from top to bottom
2. For each row, try placing queen in each column
3. Check if position is safe (no conflicts with previously placed queens)
4. If safe, place queen and move to next row
5. If not safe or no solution found, backtrack and try next column
6. Continue until all solutions are found or all possibilities exhausted

IMPORTANT NOTES:
- No solution exists for n=2 and n=3
- Solutions exist for n=1 and all n≥4
- For n=8, there are exactly 92 solutions
- Time complexity: O(N!) in worst case

BOARD VISUALIZATION:
- Light/Dark squares represent the chessboard
- Gold circles with ♛ symbols represent queen positions
- Use arrow buttons to navigate between different solutions
"""
    messagebox.showinfo("Help", help_text)


# Store current solution data
current_solution = {}

root = tk.Tk()
root.title("Exercise 7 - N-Queens Problem (Backtracking)")
root.geometry("1000x800")

# Main frame
main_frame = ttk.Frame(root, padding=18)
main_frame.pack(fill="both", expand=True)

# Title
ttk.Label(main_frame, text="N-Queens Problem using Backtracking",
          font=("Segoe UI", 18, "bold")).pack(anchor="w")

# Input section
input_frame = ttk.LabelFrame(main_frame, text="Input", padding=10)
input_frame.pack(fill="x", pady=(10, 10))

input_inner = ttk.Frame(input_frame)
input_inner.pack(fill="x")

ttk.Label(input_inner, text="Board size (N):").pack(side="left", padx=(0, 10))
n_var = tk.StringVar(value="8")
n_spin = ttk.Spinbox(input_inner, from_=1, to=13, textvariable=n_var, width=5)
n_spin.pack(side="left", padx=(0, 20))

ttk.Button(input_inner, text="Solve", command=run_n_queens).pack(side="left", padx=(0, 10))
ttk.Button(input_inner, text="Help", command=show_help).pack(side="left")

# Quick preset buttons
ttk.Label(input_inner, text="Quick presets:").pack(side="left", padx=(20, 10))
ttk.Button(input_inner, text="4-Queens", command=lambda: (n_var.set("4"), run_n_queens())).pack(side="left", padx=2)
ttk.Button(input_inner, text="8-Queens", command=lambda: (n_var.set("8"), run_n_queens())).pack(side="left", padx=2)
ttk.Button(input_inner, text="10-Queens", command=lambda: (n_var.set("10"), run_n_queens())).pack(side="left", padx=2)

# Result summary
result_var = tk.StringVar(value="Enter board size and click Solve")
ttk.Label(main_frame, textvariable=result_var, font=("Segoe UI", 10, "bold"),
          foreground="darkgreen").pack(anchor="w", pady=(0, 10))

# Board visualization section
board_frame = ttk.LabelFrame(main_frame, text="Solution Visualization", padding=10)
board_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))

board_label = ttk.Label(board_frame, text="Board will appear here", foreground="gray")
board_label.pack()

# Navigation controls
nav_frame = ttk.Frame(board_frame)
nav_frame.pack(fill="x", pady=(10, 0))

ttk.Button(nav_frame, text="← Previous", command=prev_solution).pack(side="left")
solution_counter_var = tk.StringVar(value="No solution")
ttk.Label(nav_frame, textvariable=solution_counter_var, justify="center").pack(side="left", expand=True, fill="x")
ttk.Button(nav_frame, text="Next →", command=next_solution).pack(side="left")

# Output section
output_frame = ttk.LabelFrame(main_frame, text="Algorithm Details", padding=10)
output_frame.pack(side="right", fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

output = tk.Text(output_frame, height=30, width=60, wrap="word",
                font=("Consolas", 9), yscrollcommand=scrollbar.set)
output.pack(side="left", fill="both", expand=True)
scrollbar.config(command=output.yview)

# Initial message
initial_text = """N-Queens Problem using Backtracking

Enter the board size (N) and click "Solve" to find all solutions.

ALGORITHM:
- Uses backtracking to find all valid placements
- Places queens row by row, checking safety at each step
- Backtracks when no valid position is found in current row
- Continues until all solutions are discovered

EXAMPLE:
For an 8×8 board, there are exactly 92 different solutions.

Click Help for more information.
"""
output.insert("1.0", initial_text)

root.mainloop()
from typing import List, Tuple

def is_safe(board: List[int], row: int, col: int) -> bool:
    """
    Check if placing a queen at (row, col) is safe.
    
    Args:
        board: List where board[i] represents column position of queen in row i
        row: Current row
        col: Column to place queen
    
    Returns:
        True if position is safe, False otherwise
    """
    # Check if any queen in the same column
    for i in range(row):
        if board[i] == col:
            return False
    
    # Check if any queen in the left diagonal
    for i in range(row):
        if abs(board[i] - col) == abs(i - row):
            return False
    
    return True

def solve_n_queens_backtrack(n: int, row: int, board: List[int], 
                            solutions: List[List[int]], steps: List[str]) -> None:
    """
    Solve N-Queens problem using backtracking.
    
    Args:
        n: Size of the board (number of queens)
        row: Current row being processed
        board: Current board state
        solutions: List to store all solutions
        steps: List to store execution steps
    """
    if row == n:
        # Found a valid solution
        solutions.append(board[:])
        steps.append(f"✓ Solution {len(solutions)} found: {board}")
        return
    
    for col in range(n):
        if is_safe(board, row, col):
            # Place queen
            board[row] = col
            steps.append(f"  Place queen at ({row}, {col})")
            
            # Recurse to place rest of queens
            solve_n_queens_backtrack(n, row + 1, board, solutions, steps)
            
            # Backtrack
            steps.append(f"  Backtrack from ({row}, {col})")
            board[row] = -1

def solve_n_queens(n: int) -> Tuple[List[List[int]], List[str]]:
    """
    Solve N-Queens problem and return all solutions.
    
    Args:
        n: Size of the board
    
    Returns:
        Tuple of (solutions, execution_steps)
    """
    if n <= 0:
        return [], ["Error: Board size must be greater than 0"]
    
    if n == 1:
        return [[0]], ["Solution 1 found: [0]"]
    
    if n < 4 and n > 1:
        return [], [f"No solution exists for n={n} (only n=1, n≥4 have solutions)"]
    
    board = [-1] * n
    solutions = []
    steps = []
    
    steps.append(f"Solving {n}-Queens Problem using Backtracking")
    steps.append(f"Finding all solutions for a {n}×{n} board...")
    steps.append("")
    
    solve_n_queens_backtrack(n, 0, board, solutions, steps)
    
    steps.append("")
    steps.append(f"Total solutions found: {len(solutions)}")
    
    return solutions, steps

def solution_to_board(solution: List[int], n: int) -> List[List[int]]:
    """
    Convert solution (column positions) to 2D board representation.
    
    Args:
        solution: List where solution[i] is column of queen in row i
        n: Board size
    
    Returns:
        2D list representing the board (1 = queen, 0 = empty)
    """
    board = [[0 for _ in range(n)] for _ in range(n)]
    
    for row in range(n):
        col = solution[row]
        board[row][col] = 1
    
    return board

def get_solution_summary(solutions: List[List[int]]) -> List[str]:
    """
    Generate human-readable summary of all solutions.
    
    Args:
        solutions: List of solutions
    
    Returns:
        List of formatted solution strings
    """
    summary = []
    
    for idx, sol in enumerate(solutions):
        n = len(sol)
        summary.append(f"Solution {idx + 1}: {sol}")
        
        # Convert to board representation
        board = solution_to_board(sol, n)
        
        # Show board visually
        for row in board:
            board_str = " ".join("♛" if cell == 1 else "·" for cell in row)
            summary.append(f"  {board_str}")
    
    return summary

def count_queens_placements(n: int) -> int:
    """
    Count total number of possible queen placements (n!) to understand problem space.
    
    Args:
        n: Board size
    
    Returns:
        Factorial of n
    """
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Example usage
if __name__ == "__main__":
    n = 8
    
    print(f"=== N-Queens Problem (Backtracking) ===")
    print(f"Board size: {n}×{n}")
    print(f"Total possible placements: {count_queens_placements(n)}!")
    print("")
    
    solutions, steps = solve_n_queens(n)
    
    print("Execution trace:")
    for step in steps[:20]:  # Show first 20 steps
        print(step)
    
    if len(steps) > 20:
        print(f"... ({len(steps) - 20} more steps)")
    
    print("\n" + "="*50)
    print(f"Solutions found: {len(solutions)}\n")
    
    # Show first few solutions
    summary = get_solution_summary(solutions)
    for line in summary[:min(20, len(summary))]:
        print(line)
    
    if len(summary) > 20:
        print(f"\n... and {len(summary) - 20} more lines")
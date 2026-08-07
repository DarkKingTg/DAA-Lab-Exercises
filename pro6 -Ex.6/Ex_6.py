from typing import List, Tuple

def matrix_chain_multiplication(dimensions: List[int]) -> Tuple[int, List[List[int]], List[str]]:
    """
    Find optimal cost for matrix chain multiplication using dynamic programming.
    
    Args:
        dimensions: List of matrix dimensions where matrix i has dimensions 
                   dimensions[i-1] x dimensions[i]
    
    Returns:
        Tuple of (minimum_cost, dp_table, execution_steps)
    """
    n = len(dimensions) - 1  # Number of matrices
    if n < 2:
        return 0, [[0]], ["Error: Need at least 2 matrices"]
    
    # dp[i][j] = minimum cost to multiply matrices from i to j
    dp = [[0 for _ in range(n)] for _ in range(n)]
    
    # s[i][j] = optimal split point for matrices from i to j
    s = [[0 for _ in range(n)] for _ in range(n)]
    
    steps = []
    steps.append(f"Matrix Chain Multiplication using Dynamic Programming")
    steps.append(f"Input: {n} matrices with dimensions: {format_matrix_dimensions(dimensions)}")
    steps.append(f"DP Table initialized: {n}x{n}")
    steps.append("")
    
    # l is chain length
    for l in range(2, n + 1):
        steps.append(f"Computing for chain length {l}:")
        
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float('inf')
            
            # Try all possible split points
            for k in range(i, j):
                # Cost of multiplying matrices from i to k and k+1 to j
                # plus cost of multiplying the two resulting matrices
                cost = (dp[i][k] + dp[k+1][j] + 
                       dimensions[i] * dimensions[k+1] * dimensions[j+1])
                
                steps.append(f"  M[{i+1}..{j+1}]: split at {k+1}, cost = {dp[i][k]} + {dp[k+1][j]} + {dimensions[i]}×{dimensions[k+1]}×{dimensions[j+1]} = {cost}")
                
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    s[i][j] = k
            
            steps.append(f"  M[{i+1}..{j+1}] optimal cost: {dp[i][j]} (split at {s[i][j]+1})")
        steps.append("")
    
    steps.append(f"Final optimal cost: {dp[0][n-1]}")
    
    return dp[0][n-1], dp, steps

def format_matrix_dimensions(dimensions: List[int]) -> str:
    """Format matrix dimensions for display."""
    result = []
    for i in range(len(dimensions) - 1):
        result.append(f"M{i+1}({dimensions[i]}×{dimensions[i+1]})")
    return ", ".join(result)

def print_optimal_parentheses(s: List[List[int]], i: int, j: int) -> str:
    """
    Reconstruct the optimal parenthesization.
    
    Args:
        s: Split point table
        i: Start matrix index
        j: End matrix index
    
    Returns:
        String representation of optimal parenthesization
    """
    if i == j:
        return f"M{i+1}"
    else:
        k = s[i][j]
        left = print_optimal_parentheses(s, i, k)
        right = print_optimal_parentheses(s, k+1, j)
        return f"({left} × {right})"

def get_computation_order(s: List[List[int]], i: int, j: int, dimensions: List[int], steps: List[str], level: int = 0) -> None:
    """
    Get the order of matrix multiplications with costs.
    
    Args:
        s: Split point table
        i: Start matrix index  
        j: End matrix index
        dimensions: Matrix dimensions
        steps: List to store computation steps
        level: Indentation level for display
    """
    if i == j:
        return
    
    k = s[i][j]
    indent = "  " * level
    
    # Calculate cost for this multiplication
    cost = dimensions[i] * dimensions[k+1] * dimensions[j+1]
    
    if i == k:
        left_str = f"M{i+1}"
    else:
        left_str = f"Result[M{i+1}..M{k+1}]"
        
    if k+1 == j:
        right_str = f"M{j+1}"
    else:
        right_str = f"Result[M{k+2}..M{j+1}]"
    
    steps.append(f"{indent}Step: Multiply {left_str} × {right_str}")
    steps.append(f"{indent}      Dimensions: ({dimensions[i]} × {dimensions[k+1]}) × ({dimensions[k+1]} × {dimensions[j+1]})")
    steps.append(f"{indent}      Cost: {dimensions[i]} × {dimensions[k+1]} × {dimensions[j+1]} = {cost} multiplications")
    steps.append("")
    
    # Recursively get order for left and right subproblems
    get_computation_order(s, i, k, dimensions, steps, level + 1)
    get_computation_order(s, k+1, j, dimensions, steps, level + 1)

def matrix_chain_wrapper(dimensions: List[int]) -> Tuple[int, str, List[str], List[str]]:
    """
    Wrapper function for matrix chain multiplication with detailed output.
    
    Returns:
        Tuple of (optimal_cost, optimal_parentheses, dp_steps, computation_order)
    """
    if len(dimensions) < 3:
        return 0, "", ["Error: Need at least 2 matrices"], []
    
    optimal_cost, dp, dp_steps = matrix_chain_multiplication(dimensions)
    
    n = len(dimensions) - 1
    s = [[0 for _ in range(n)] for _ in range(n)]
    
    # Rebuild split table for parentheses reconstruction
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float('inf')
            
            for k in range(i, j):
                cost = (dp[i][k] + dp[k+1][j] + 
                       dimensions[i] * dimensions[k+1] * dimensions[j+1])
                
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    s[i][j] = k
    
    optimal_parentheses = print_optimal_parentheses(s, 0, n-1)
    
    # Get computation order
    order_steps = []
    order_steps.append("Optimal computation order:")
    get_computation_order(s, 0, n-1, dimensions, order_steps)
    
    return optimal_cost, optimal_parentheses, dp_steps, order_steps

# Example usage
if __name__ == "__main__":
    # Example: 4 matrices A1(1×2), A2(2×3), A3(3×4), A4(4×5)
    # Dimensions array: [1, 2, 3, 4, 5]
    dimensions = [1, 2, 3, 4, 5]
    
    print("=== Matrix Chain Multiplication ===")
    print(f"Matrix dimensions: {format_matrix_dimensions(dimensions)}")
    
    optimal_cost, optimal_parentheses, dp_steps, order_steps = matrix_chain_wrapper(dimensions)
    
    print(f"\nOptimal cost: {optimal_cost}")
    print(f"Optimal parenthesization: {optimal_parentheses}")
    
    print("\nDetailed steps:")
    for step in dp_steps:
        print(step)
    
    print("\nComputation order:")
    for step in order_steps:
        print(step)
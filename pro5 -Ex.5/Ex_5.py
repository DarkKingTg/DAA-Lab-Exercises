from typing import List, Tuple

def minmax_divide_conquer(arr: List[int], low: int, high: int, steps: List[str] = None) -> Tuple[int, int]:
    """
    Find minimum and maximum values in array using divide and conquer technique.
    
    Args:
        arr: Input array
        low: Starting index
        high: Ending index
        steps: List to store execution steps (for visualization)
    
    Returns:
        Tuple of (minimum, maximum) values
    """
    if steps is None:
        steps = []
    
    # Base case: Only one element
    if low == high:
        steps.append(f"Base case: index {low}, value = {arr[low]} -> min = {arr[low]}, max = {arr[low]}")
        return arr[low], arr[low]
    
    # Base case: Two elements
    if high == low + 1:
        min_val = min(arr[low], arr[high])
        max_val = max(arr[low], arr[high])
        steps.append(f"Two elements: indices {low}-{high}, values = [{arr[low]}, {arr[high]}] -> min = {min_val}, max = {max_val}")
        return min_val, max_val
    
    # Divide: Find middle point
    mid = (low + high) // 2
    steps.append(f"Divide: range [{low}..{high}] split at index {mid}")
    
    # Conquer: Recursively find min-max in both halves
    min1, max1 = minmax_divide_conquer(arr, low, mid, steps)
    min2, max2 = minmax_divide_conquer(arr, mid + 1, high, steps)
    
    # Combine: Find overall min and max
    overall_min = min(min1, min2)
    overall_max = max(max1, max2)
    
    steps.append(f"Combine: left half min={min1}, max={max1}; right half min={min2}, max={max2} -> overall min={overall_min}, max={overall_max}")
    
    return overall_min, overall_max

def minmax_wrapper(arr: List[int]) -> Tuple[int, int, List[str]]:
    """
    Wrapper function to find min-max and return execution steps.
    
    Args:
        arr: Input array
        
    Returns:
        Tuple of (minimum, maximum, execution_steps)
    """
    if not arr:
        return None, None, ["Error: Empty array"]
    
    steps = []
    steps.append(f"Starting MinMax divide & conquer on array: {arr}")
    steps.append(f"Array size: {len(arr)}")
    
    min_val, max_val = minmax_divide_conquer(arr, 0, len(arr) - 1, steps)
    
    steps.append(f"Final result: Minimum = {min_val}, Maximum = {max_val}")
    
    return min_val, max_val, steps

def minmax_naive(arr: List[int]) -> Tuple[int, int, int]:
    """
    Naive approach to find min-max for comparison.
    
    Returns:
        Tuple of (minimum, maximum, comparisons_count)
    """
    if not arr:
        return None, None, 0
    
    min_val = max_val = arr[0]
    comparisons = 0
    
    for i in range(1, len(arr)):
        comparisons += 1
        if arr[i] < min_val:
            min_val = arr[i]
        comparisons += 1
        if arr[i] > max_val:
            max_val = arr[i]
    
    return min_val, max_val, comparisons

# Example usage
if __name__ == "__main__":
    # Test array
    test_array = [3, 5, 1, 9, 8, 2, 7, 4, 6]
    
    print("=== MinMax using Divide & Conquer ===")
    print(f"Input array: {test_array}")
    
    # Divide and conquer approach
    min_dc, max_dc, steps = minmax_wrapper(test_array)
    
    print("\nStep-by-step execution:")
    for i, step in enumerate(steps):
        print(f"{i+1}. {step}")
    
    # Naive approach for comparison
    min_naive, max_naive, comparisons = minmax_naive(test_array)
    
    print(f"\nComparison:")
    print(f"Divide & Conquer: Min = {min_dc}, Max = {max_dc}")
    print(f"Naive approach: Min = {min_naive}, Max = {max_naive}, Comparisons = {comparisons}")
    
    # Theoretical comparison count for divide & conquer
    n = len(test_array)
    if n > 1:
        # T(n) = 2T(n/2) + 2 for divide & conquer
        # Approximately 1.5n - 2 comparisons
        dc_comparisons = int(1.5 * n - 2) if n > 1 else 0
        print(f"Divide & Conquer theoretical comparisons: ~{dc_comparisons}")
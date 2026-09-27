"""
Exercise 10: Improving Quicksort using Randomized Algorithm
Implements Deterministic Quicksort vs. Randomized Quicksort with comparison & recursion depth metrics.
"""
import random
import time
import sys
from typing import List, Dict, Any, Tuple

# Increase recursion limit slightly for deterministic quicksort worst-case on large sorted arrays
sys.setrecursionlimit(5000)


class QuicksortTracker:
    """Tracks performance metrics during Quicksort execution."""
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.max_depth = 0
        self.current_depth = 0
        self.trace: List[str] = []

    def enter_rec(self):
        pass  # Helper for depth tracking


def partition(arr: List[int], low: int, high: int, tracker: QuicksortTracker) -> int:
    """Standard Lomuto partition scheme."""
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        tracker.comparisons += 1
        if arr[j] <= pivot:
            i += 1
            if i != j:
                arr[i], arr[j] = arr[j], arr[i]
                tracker.swaps += 1

    if i + 1 != high:
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        tracker.swaps += 1

    return i + 1


def partition_randomized(arr: List[int], low: int, high: int, tracker: QuicksortTracker) -> int:
    """Randomized pivot selection: picks random index in [low, high] and swaps with high."""
    rand_pivot_idx = random.randint(low, high)
    if rand_pivot_idx != high:
        arr[rand_pivot_idx], arr[high] = arr[high], arr[rand_pivot_idx]
        tracker.swaps += 1

    return partition(arr, low, high, tracker)


def partition_median3(arr: List[int], low: int, high: int, tracker: QuicksortTracker) -> int:
    """Median-of-3 Randomized pivot selection: picks 3 random indices and uses their median."""
    if high - low + 1 >= 3:
        candidates = random.sample(range(low, high + 1), 3)
        # Sort candidate indices by their array values
        candidates.sort(key=lambda idx: arr[idx])
        median_idx = candidates[1]
    else:
        median_idx = random.randint(low, high)

    if median_idx != high:
        arr[median_idx], arr[high] = arr[high], arr[median_idx]
        tracker.swaps += 1

    return partition(arr, low, high, tracker)


def _quicksort_helper(arr: List[int], low: int, high: int, pivot_type: str, tracker: QuicksortTracker, depth: int):
    tracker.max_depth = max(tracker.max_depth, depth)

    if low < high:
        if depth <= 4 and len(arr) <= 20:
            sub = arr[low:high+1]
            tracker.trace.append(f"Depth {depth}: Partitioning sub-array {sub} (low={low}, high={high})")

        if pivot_type == "deterministic_first":
            # Swap first element with high to use Lomuto partition
            arr[low], arr[high] = arr[high], arr[low]
            tracker.swaps += 1
            pi = partition(arr, low, high, tracker)
        elif pivot_type == "deterministic_last":
            pi = partition(arr, low, high, tracker)
        elif pivot_type == "randomized":
            pi = partition_randomized(arr, low, high, tracker)
        elif pivot_type == "randomized_median3":
            pi = partition_median3(arr, low, high, tracker)
        else:
            pi = partition(arr, low, high, tracker)

        _quicksort_helper(arr, low, pi - 1, pivot_type, tracker, depth + 1)
        _quicksort_helper(arr, pi + 1, high, pivot_type, tracker, depth + 1)


def run_quicksort(input_array: List[int], pivot_type: str = "randomized") -> Dict[str, Any]:
    """
    Executes specified variant of Quicksort and returns execution metrics.
    
    Args:
        input_array: Copy of list to sort
        pivot_type: One of ['deterministic_first', 'deterministic_last', 'randomized', 'randomized_median3']
    """
    arr = list(input_array)
    tracker = QuicksortTracker()

    readable_names = {
        "deterministic_first": "Deterministic (First Element Pivot)",
        "deterministic_last": "Deterministic (Last Element Pivot)",
        "randomized": "Randomized Quicksort (Random Pivot)",
        "randomized_median3": "Randomized Quicksort (Median-of-3 Pivot)"
    }

    alg_name = readable_names.get(pivot_type, pivot_type)
    tracker.trace.append(f"=== {alg_name} ===")
    tracker.trace.append(f"Array Size: {len(arr)} | Initial: {arr[:10]}{'...' if len(arr)>10 else ''}")

    start_time = time.perf_counter()
    if arr:
        _quicksort_helper(arr, 0, len(arr) - 1, pivot_type, tracker, 1)
    end_time = time.perf_counter()

    exec_time_ms = (end_time - start_time) * 1000.0

    tracker.trace.append(f"Sorted Array: {arr[:10]}{'...' if len(arr)>10 else ''}")
    tracker.trace.append(f"Comparisons: {tracker.comparisons} | Swaps: {tracker.swaps} | Max Recursion Depth: {tracker.max_depth} | Time: {exec_time_ms:.3f} ms")

    return {
        "algorithm": alg_name,
        "pivot_type": pivot_type,
        "sorted_array": arr,
        "comparisons": tracker.comparisons,
        "swaps": tracker.swaps,
        "max_depth": tracker.max_depth,
        "time_ms": exec_time_ms,
        "trace": tracker.trace
    }


def generate_benchmark_data(size: int = 150) -> Dict[str, List[int]]:
    """Generates 4 canonical array distributions for benchmarking."""
    random_arr = [random.randint(1, 1000) for _ in range(size)]
    sorted_arr = list(range(1, size + 1))
    reverse_sorted_arr = list(range(size, 0, -1))
    duplicates_arr = [random.choice([10, 20, 30, 40, 50]) for _ in range(size)]

    return {
        "Random Unsorted": random_arr,
        "Already Sorted (Worst-Case for Naive)": sorted_arr,
        "Reverse Sorted (Worst-Case for Naive)": reverse_sorted_arr,
        "Many Duplicates": duplicates_arr
    }


def compare_quicksort_variants(input_array: List[int]) -> List[Dict[str, Any]]:
    """Runs all 4 quicksort variants on the same array and returns comparative list."""
    variants = ["deterministic_first", "deterministic_last", "randomized", "randomized_median3"]
    results = []
    for v in variants:
        results.append(run_quicksort(input_array, pivot_type=v))
    return results


if __name__ == "__main__":
    test_arr = [34, 7, 23, 32, 5, 62, 78, 12, 1, 99, 45, 18, 54, 88]
    print("Input Array:", test_arr)
    print("\n--- Randomized Quicksort Run ---")
    res = run_quicksort(test_arr, "randomized")
    for t in res["trace"]:
        print(t)

    print("\n--- Benchmark on Sorted Array (Size 150) ---")
    bench = generate_benchmark_data(150)["Already Sorted (Worst-Case for Naive)"]
    comp = compare_quicksort_variants(bench)
    for r in comp:
        print(f"{r['algorithm']:<42} | Comps: {r['comparisons']:<6} | Swaps: {r['swaps']:<5} | Depth: {r['max_depth']:<3} | Time: {r['time_ms']:.3f} ms")

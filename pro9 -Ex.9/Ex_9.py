"""
Exercise 9: Effective Bin Packing Algorithms
Implements Next-Fit, First-Fit, Best-Fit, Worst-Fit, First-Fit Decreasing (FFD), and Best-Fit Decreasing (BFD).
"""
from typing import List, Dict, Any, Tuple


class Bin:
    """Represents a bin containing items."""
    def __init__(self, bin_id: int, capacity: float):
        self.bin_id = bin_id
        self.capacity = capacity
        self.items: List[Tuple[int, float]] = []  # List of (item_index, size)
        self.remaining: float = capacity

    def can_fit(self, size: float) -> bool:
        return self.remaining >= size

    def add_item(self, item_index: int, size: float):
        self.items.append((item_index, size))
        self.remaining -= size

    def used_capacity(self) -> float:
        return self.capacity - self.remaining

    def __repr__(self) -> str:
        items_str = ", ".join([f"Item #{idx+1}({sz})" for idx, sz in self.items])
        return f"Bin {self.bin_id} [Used: {self.used_capacity()}/{self.capacity}, Free: {self.remaining}] -> {items_str}"


def next_fit(items: List[float], capacity: float) -> Dict[str, Any]:
    """Next-Fit (NF) Bin Packing Algorithm."""
    bins: List[Bin] = []
    trace: List[str] = ["=== Next-Fit (NF) Algorithm ==="]

    if not items:
        return {"algorithm": "Next-Fit", "bins": [], "num_bins": 0, "wasted": 0, "efficiency": 0, "trace": trace}

    current_bin = Bin(1, capacity)
    bins.append(current_bin)

    for idx, item in enumerate(items):
        if item > capacity:
            trace.append(f"Skipped Item #{idx+1} (Size: {item} exceeds Bin Capacity: {capacity})")
            continue

        if current_bin.can_fit(item):
            current_bin.add_item(idx, item)
            trace.append(f"Placed Item #{idx+1} (Size: {item}) into Bin #{current_bin.bin_id} [Remaining: {current_bin.remaining}]")
        else:
            current_bin = Bin(len(bins) + 1, capacity)
            current_bin.add_item(idx, item)
            bins.append(current_bin)
            trace.append(f"Opened Bin #{current_bin.bin_id} & placed Item #{idx+1} (Size: {item}) [Remaining: {current_bin.remaining}]")

    return _compile_result("Next-Fit", bins, items, capacity, trace)


def first_fit(items: List[float], capacity: float) -> Dict[str, Any]:
    """First-Fit (FF) Bin Packing Algorithm."""
    bins: List[Bin] = []
    trace: List[str] = ["=== First-Fit (FF) Algorithm ==="]

    for idx, item in enumerate(items):
        if item > capacity:
            trace.append(f"Skipped Item #{idx+1} (Size: {item} exceeds Bin Capacity: {capacity})")
            continue

        placed = False
        for b in bins:
            if b.can_fit(item):
                b.add_item(idx, item)
                trace.append(f"Placed Item #{idx+1} (Size: {item}) into existing Bin #{b.bin_id} [Remaining: {b.remaining}]")
                placed = True
                break

        if not placed:
            new_bin = Bin(len(bins) + 1, capacity)
            new_bin.add_item(idx, item)
            bins.append(new_bin)
            trace.append(f"Opened new Bin #{new_bin.bin_id} & placed Item #{idx+1} (Size: {item}) [Remaining: {new_bin.remaining}]")

    return _compile_result("First-Fit", bins, items, capacity, trace)


def best_fit(items: List[float], capacity: float) -> Dict[str, Any]:
    """Best-Fit (BF) Bin Packing Algorithm."""
    bins: List[Bin] = []
    trace: List[str] = ["=== Best-Fit (BF) Algorithm ==="]

    for idx, item in enumerate(items):
        if item > capacity:
            trace.append(f"Skipped Item #{idx+1} (Size: {item} exceeds Bin Capacity: {capacity})")
            continue

        best_bin: Optional[Bin] = None
        min_space_left = float('inf')

        for b in bins:
            if b.can_fit(item):
                space_left = b.remaining - item
                if space_left < min_space_left:
                    min_space_left = space_left
                    best_bin = b

        if best_bin is not None:
            best_bin.add_item(idx, item)
            trace.append(f"Placed Item #{idx+1} (Size: {item}) into Best-Fit Bin #{best_bin.bin_id} [Remaining: {best_bin.remaining}]")
        else:
            new_bin = Bin(len(bins) + 1, capacity)
            new_bin.add_item(idx, item)
            bins.append(new_bin)
            trace.append(f"Opened new Bin #{new_bin.bin_id} & placed Item #{idx+1} (Size: {item}) [Remaining: {new_bin.remaining}]")

    return _compile_result("Best-Fit", bins, items, capacity, trace)


def worst_fit(items: List[float], capacity: float) -> Dict[str, Any]:
    """Worst-Fit (WF) Bin Packing Algorithm."""
    bins: List[Bin] = []
    trace: List[str] = ["=== Worst-Fit (WF) Algorithm ==="]

    for idx, item in enumerate(items):
        if item > capacity:
            trace.append(f"Skipped Item #{idx+1} (Size: {item} exceeds Bin Capacity: {capacity})")
            continue

        worst_bin: Optional[Bin] = None
        max_space_left = -1.0

        for b in bins:
            if b.can_fit(item):
                if b.remaining > max_space_left:
                    max_space_left = b.remaining
                    worst_bin = b

        if worst_bin is not None:
            worst_bin.add_item(idx, item)
            trace.append(f"Placed Item #{idx+1} (Size: {item}) into Worst-Fit Bin #{worst_bin.bin_id} [Remaining: {worst_bin.remaining}]")
        else:
            new_bin = Bin(len(bins) + 1, capacity)
            new_bin.add_item(idx, item)
            bins.append(new_bin)
            trace.append(f"Opened new Bin #{new_bin.bin_id} & placed Item #{idx+1} (Size: {item}) [Remaining: {new_bin.remaining}]")

    return _compile_result("Worst-Fit", bins, items, capacity, trace)


def first_fit_decreasing(items: List[float], capacity: float) -> Dict[str, Any]:
    """First-Fit Decreasing (FFD) Offline Bin Packing Algorithm."""
    # Pair items with original index: (orig_index, size)
    indexed_items = sorted(enumerate(items), key=lambda x: x[1], reverse=True)
    
    bins: List[Bin] = []
    trace: List[str] = ["=== First-Fit Decreasing (FFD) Algorithm ==="]
    trace.append("Items sorted in descending order before placement:")
    trace.append(", ".join([f"Item #{orig_idx+1}({sz})" for orig_idx, sz in indexed_items]))
    trace.append("")

    for orig_idx, item in indexed_items:
        if item > capacity:
            trace.append(f"Skipped Item #{orig_idx+1} (Size: {item} exceeds Bin Capacity: {capacity})")
            continue

        placed = False
        for b in bins:
            if b.can_fit(item):
                b.add_item(orig_idx, item)
                trace.append(f"Placed Item #{orig_idx+1} (Size: {item}) into Bin #{b.bin_id} [Remaining: {b.remaining}]")
                placed = True
                break

        if not placed:
            new_bin = Bin(len(bins) + 1, capacity)
            new_bin.add_item(orig_idx, item)
            bins.append(new_bin)
            trace.append(f"Opened Bin #{new_bin.bin_id} & placed Item #{orig_idx+1} (Size: {item}) [Remaining: {new_bin.remaining}]")

    return _compile_result("First-Fit Decreasing", bins, items, capacity, trace)


def best_fit_decreasing(items: List[float], capacity: float) -> Dict[str, Any]:
    """Best-Fit Decreasing (BFD) Offline Bin Packing Algorithm."""
    indexed_items = sorted(enumerate(items), key=lambda x: x[1], reverse=True)
    
    bins: List[Bin] = []
    trace: List[str] = ["=== Best-Fit Decreasing (BFD) Algorithm ==="]
    trace.append("Items sorted in descending order before placement:")
    trace.append(", ".join([f"Item #{orig_idx+1}({sz})" for orig_idx, sz in indexed_items]))
    trace.append("")

    for orig_idx, item in indexed_items:
        if item > capacity:
            trace.append(f"Skipped Item #{orig_idx+1} (Size: {item} exceeds Bin Capacity: {capacity})")
            continue

        best_bin: Optional[Bin] = None
        min_space_left = float('inf')

        for b in bins:
            if b.can_fit(item):
                space_left = b.remaining - item
                if space_left < min_space_left:
                    min_space_left = space_left
                    best_bin = b

        if best_bin is not None:
            best_bin.add_item(orig_idx, item)
            trace.append(f"Placed Item #{orig_idx+1} (Size: {item}) into Best-Fit Bin #{best_bin.bin_id} [Remaining: {best_bin.remaining}]")
        else:
            new_bin = Bin(len(bins) + 1, capacity)
            new_bin.add_item(orig_idx, item)
            bins.append(new_bin)
            trace.append(f"Opened Bin #{new_bin.bin_id} & placed Item #{orig_idx+1} (Size: {item}) [Remaining: {new_bin.remaining}]")

    return _compile_result("Best-Fit Decreasing", bins, items, capacity, trace)


def _compile_result(alg_name: str, bins: List[Bin], original_items: List[float], capacity: float, trace: List[str]) -> Dict[str, Any]:
    num_bins = len(bins)
    total_item_weight = sum([item for item in original_items if item <= capacity])
    total_bin_capacity = num_bins * capacity
    wasted = total_bin_capacity - total_item_weight if total_bin_capacity > 0 else 0
    efficiency = (total_item_weight / total_bin_capacity * 100) if total_bin_capacity > 0 else 0.0

    trace.append("")
    trace.append(f"Summary: {num_bins} bins used | Total Capacity: {total_bin_capacity:.1f} | Packed Weight: {total_item_weight:.1f} | Wasted: {wasted:.1f} | Efficiency: {efficiency:.2f}%")

    return {
        "algorithm": alg_name,
        "bins": bins,
        "num_bins": num_bins,
        "wasted": wasted,
        "efficiency": efficiency,
        "total_weight": total_item_weight,
        "trace": trace
    }


def compare_all_bin_packing_algorithms(items: List[float], capacity: float) -> List[Dict[str, Any]]:
    """Runs all 6 bin packing algorithms and returns comparative summary."""
    results = [
        first_fit_decreasing(items, capacity),
        best_fit_decreasing(items, capacity),
        first_fit(items, capacity),
        best_fit(items, capacity),
        next_fit(items, capacity),
        worst_fit(items, capacity),
    ]
    # Sort results primarily by num_bins ascending, then efficiency descending
    results.sort(key=lambda x: (x["num_bins"], -x["efficiency"]))
    return results


def get_preset_bin_packing(preset_name: str) -> Tuple[List[float], float]:
    """Returns sample item lists and bin capacities."""
    if preset_name == "Textbook Classic":
        items = [2.0, 5.0, 4.0, 7.0, 1.0, 3.0, 8.0, 6.0, 5.0, 4.0]
        capacity = 10.0
    elif preset_name == "Heavy Cargo":
        items = [7.0, 8.0, 9.0, 6.0, 8.0, 7.0, 9.0, 5.0]
        capacity = 10.0
    elif preset_name == "Small Mixed Items":
        items = [1.5, 2.0, 3.5, 1.0, 4.0, 2.5, 3.0, 1.2, 2.8, 3.2, 4.5]
        capacity = 5.0
    elif preset_name == "Disparate Sizes":
        items = [6.0, 1.0, 6.0, 1.0, 6.0, 1.0, 6.0, 1.0]
        capacity = 7.0
    else:  # Default
        items = [4.0, 8.0, 1.0, 4.0, 2.0, 5.0, 7.0, 3.0]
        capacity = 10.0

    return items, capacity


if __name__ == "__main__":
    items, cap = get_preset_bin_packing("Textbook Classic")
    print(f"Items: {items}, Bin Capacity: {cap}\n")

    results = compare_all_bin_packing_algorithms(items, cap)
    print("=== Algorithm Comparison ===")
    for r in results:
        print(f"{r['algorithm']:<22} | Bins: {r['num_bins']} | Wasted: {r['wasted']:.1f} | Efficiency: {r['efficiency']:.2f}%")

# DAA Lab Exercises

Design and Analysis of Algorithms (DAA) laboratory exercises with interactive GUI implementations.

## Exercises Overview

### Exercise 1: Interpolation Search
- **Algorithm**: Interpolation Search
- **Files**: `pro1 -Ex.1/`
- **Features**: 
  - Tkinter GUI for visualization
  - FastAPI web interface with HTML frontend
  - Step-by-step search process display

### Exercise 2: String Matching Algorithms
- **Algorithm**: Naive, KMP, and Rabin-Karp comparison
- **Files**: `pro2 -Ex.2/`
- **Features**: 
  - Comparative analysis of three string matching algorithms
  - Performance comparison with comparison counts
  - Tkinter GUI with results table

### Exercise 3: Minimum Spanning Tree
- **Algorithm**: Kruskal's and Prim's algorithms
- **Files**: `pro3 -Ex.3/`
- **Features**: 
  - MST comparison between two algorithms
  - Graph input with edge weights
  - Side-by-side MST results

### Exercise 4: Shortest Path Algorithm
- **Algorithm**: Dijkstra's Algorithm
- **Files**: `pro4 -Ex.4/`
- **Features**: 
  - Single-source shortest path finding
  - Step-by-step algorithm execution
  - Path reconstruction and visualization
  - Graph input as edge list format

### Exercise 5: Min-Max Finding
- **Algorithm**: MinMax using Divide & Conquer
- **Files**: `pro5 -Ex.5/`
- **Features**: 
  - Divide and conquer approach for finding minimum and maximum
  - Step-by-step recursion visualization
  - Comparison with naive approach
  - Efficiency analysis and comparison counts

### Exercise 6: Matrix Chain Multiplication
- **Algorithm**: Optimal Cost Computation using Dynamic Programming
- **Files**: `pro6 -Ex.6/`
- **Features**: 
  - Dynamic programming solution for matrix chain multiplication
  - DP table visualization in separate window
  - Step-by-step algorithm execution
  - Optimal parenthesization display
  - Computation order breakdown with costs
  - Multiple example datasets (small, medium, large, textbook)

### Exercise 7: N-Queens Problem
- **Algorithm**: Backtracking Algorithm
- **Files**: `pro7 -Ex.7/`
- **Features**: 
  - Backtracking solution for N-Queens problem
  - Visual board representation with queen symbols
  - Chess pattern board visualization
  - Navigation between multiple solutions
  - Quick preset buttons (4-Queens, 8-Queens, 10-Queens)
  - Algorithm execution trace with step-by-step details
  - Support for board sizes 1 to 13
  - Safety checking and conflict detection

## How to Run

Each exercise can be run independently:

```bash
# For GUI applications (Exercises 1-7)
cd "proX -Ex.X"
python app.py

# For command line testing (where available)
python Ex_X.py
```

### Web Interface (Exercise 1 only)
```bash
cd "pro1 -Ex.1"
python main.py
# Visit http://127.0.0.1:8000 in your browser
```

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- Pillow (PIL) for Exercise 7 image generation: `pip install Pillow`
- For Exercise 1 web interface:
  - FastAPI
  - uvicorn
  - pydantic

## Features

- **Interactive GUIs**: All exercises include user-friendly graphical interfaces
- **Default Examples**: Each exercise comes with pre-configured example inputs
- **Step-by-step Visualization**: See how algorithms progress through their execution
- **Performance Analysis**: Compare different algorithms and their efficiency
- **Educational Focus**: Clear explanations and visual feedback for learning
- **Visual Solutions**: Exercise 7 includes board visualization with queen symbols

## Exercise Details

### Input Formats

- **Exercise 1**: Comma-separated numbers for array, single target number
- **Exercise 2**: Text string and pattern string
- **Exercise 3**: Edge format: `node1-node2-weight, ...` (comma-separated)
- **Exercise 4**: Edge format: `node1-node2-weight, ...` with start node
- **Exercise 5**: Comma-separated numbers for array
- **Exercise 6**: Matrix dimensions: `d0, d1, d2, ..., dn` (represents n matrices)
- **Exercise 7**: Integer board size (1-13)

### Algorithm Implementations

All algorithms are implemented with:
- Time complexity optimizations
- Clear code structure and comments
- Educational step-by-step breakdowns
- Comparison with alternative approaches where applicable

### Backtracking Features (Exercise 7)

- **Solution Finding**: Discovers all valid N-Queens placements
- **Conflict Detection**: Checks horizontal, vertical, and diagonal conflicts
- **Visual Representation**: Chess board with queen symbols
- **Solution Navigation**: Browse through multiple solutions
- **Performance Notes**: 
  - 4-Queens: 2 solutions
  - 8-Queens: 92 solutions
  - 10-Queens: 724 solutions

## Contributing

Feel free to enhance the visualizations, add more algorithms, or improve the user interfaces.
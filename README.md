*This project has been created as part of the 42 curriculum by mohfalla and jung-kwa.*

# A-Maze-ing

## Description

A maze generator written in Python that generates random mazes using the
Recursive Backtracker algorithm. The program reads a configuration file,
generates a maze, embeds a visible "42" pattern, computes the shortest path
from entry to exit, and displays the result in a colored terminal interface.

## Instructions

### Installation

```bash
make install
```

### Run

```bash
make run
# or directly:
python3 a_maze_ing.py config.txt
```

### Config file format
Comments start with
WIDTH=20          # number of cells horizontally
HEIGHT=15         # number of cells vertically
ENTRY=0,0         # entry cell coordinates (x,y)
EXIT=19,14        # exit cell coordinates (x,y)
OUTPUT_FILE=maze.txt  # output file path
PERFECT=True      # True = perfect maze (one path between any two cells)
SEED=42           # optional: integer seed for reproducibility

## Maze Generation Algorithm

This project uses the **Recursive Backtracker** (iterative DFS) algorithm.

Starting from the entry cell, the algorithm maintains a stack of visited
cells. At each step it randomly picks an unvisited neighbor, removes the
wall between them, and pushes the neighbor onto the stack. When no unvisited
neighbors remain it backtracks by popping the stack. This continues until
all cells are visited.

### Why this algorithm?

- Produces perfect mazes (exactly one path between any two cells)
- Natural depth-first exploration creates long, winding corridors
- Easy to implement iteratively without recursion depth limits
- Seed-reproducible results

## Reusable Module

The `MazeGenerator` class in `mazegen/generator.py` can be installed as a
standalone package and imported in any Python project.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen.generator import MazeGenerator

# Create and generate a maze
mg = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    seed=42          # omit for random maze
)
mg.generate()

# Access the grid (2D list of hex wall bitmasks)
print(mg.grid)

# Access the shortest path as a list of directions
print(mg.solution)  # e.g. ['E', 'E', 'S', 'S', ...]
```

### Custom parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| width | int | Number of cells horizontally |
| height | int | Number of cells vertically |
| entry | tuple[int,int] | Entry cell (x, y) |
| exit | tuple[int,int] | Exit cell (x, y) |
| seed | int or None | Random seed (None = random) |

### Wall encoding

Each cell is stored as a 4-bit integer:

| Bit | Value | Direction |
|-----|-------|-----------|
| 0 | 1 | North |
| 1 | 2 | East |
| 2 | 4 | South |
| 3 | 8 | West |

A bit set to `1` means the wall is closed.

## Team and Project Management

### Team members

- mohfalla 
- jung-kwa

### Planning

...describe how you planned and how it evolved...

### What worked well

...

### What could be improved

...

### Tools used

- Claude (AI assistant) for guidance and concept explanation
- Python 3.10
- flake8 / mypy for linting

## Resources

- [Maze generation algorithms - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explained](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [Python typing module](https://docs.python.org/3/library/typing.html)
- [BFS algorithm](https://en.wikipedia.org/wiki/Breadth-first_search)

### AI usage

Claude was used as a teaching assistant throughout this project:
- Explaining graph theory concepts (spanning trees, BFS, DFS)
- Reviewing code for bugs and suggesting fixes
- Explaining Python concepts (bitwise operations, type hints, packaging)

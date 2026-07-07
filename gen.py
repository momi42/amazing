from typing import Optional
import random
from collections import deque


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST:  WEST,
    WEST:  EAST,
}

DIRECTION_DELTA = {
    NORTH: (0, -1),
    SOUTH: (0,  1),
    EAST:  (1,  0),
    WEST:  (-1, 0),
}

DIRECTION_NAME = {
    NORTH: 'N',
    SOUTH: 'S',
    EAST:  'E',
    WEST:  'W',
}


class MazeGenerator:
    """Generate, solve, and manage a 2D maze using Recursive Backtracker (DFS).

    Attributes:
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        entry: The (x, y) coordinates of the maze entry point.
        exit: The (x, y) coordinates of the maze exit point.
        seed: Optional random seed for reproducible maze generation.
        perfect: If True, the maze is perfect (no loops); if False, imperfect.
        grid: 2D list of bitmask integers encoding wall state for each cell.
        solution: Ordered list of (x, y) coordinates from entry to exit.
        solution_str: Cardinal direction string representing the solution path.
    """
    def __init__(self,
                 width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 seed: Optional[int] = None,
                 perfect: bool = True) -> None:
        """Initialize the maze with dimensions, entry/exit points, and optional seed.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
            entry: The (x, y) coordinates of the entry cell.
            exit: The (x, y) coordinates of the exit cell.
            seed: Optional random seed for reproducible generation.
            perfect: If True, generate a perfect maze. Defaults to True.
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect
        # random.seed(seed)
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.solution: list[tuple[int, int]] = []
        self.solution_str = ""

    def _get_pattern_42(self) -> set[tuple[int, int]]:
        """Compute the set of cells forming the '42' pattern centered in the maze.

        Returns:
            A set of (x, y) coordinates that make up the '42' pattern,
            or an empty set if the maze is too small to fit it.
        """
        if self.width < 11 or self.height < 7:
            print("Error: Maze size is too small to display the '42' pattern.")
            return set()

        pattern = [
            [1, 0, 1,  0, 1, 1, 1],
            [1, 0, 1,  0, 0, 0, 1],
            [1, 1, 1,  0, 1, 1, 1],
            [0, 0, 1,  0, 1, 0, 0],
            [0, 0, 1,  0, 1, 1, 1]
        ]

        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        cells_42 = set()
        for r_idx, row in enumerate(pattern):
            for c_idx, val in enumerate(row):
                if val == 1:
                    cells_42.add((start_x + c_idx, start_y + r_idx))
        return cells_42

    def generate(self) -> None:
        """Generate the maze using an iterative Recursive Backtracker (DFS) algorithm.

        Resets the grid, embeds the '42' pattern as pre-visited cells,
        then carves passages until all reachable cells are visited.
        """
        if self.seed is not None:
            random.seed(self.seed)
        self.grid = [
            [15 for _ in range(self.width)] for _ in range(self.height)
            ]
        self.solution = []
        self.pattern_42 = self._get_pattern_42()
        current = self.entry
        stack = []
        visited = set(self.pattern_42)
        visited.add(current)
        stack.append(current)
        while stack:
            neighbers = []
            x, y = current
            for key, value in DIRECTION_DELTA.items():
                dx, dy = value
                direction = key
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height)\
                   and (nx, ny) not in visited:
                    neighbers.append((nx, ny, direction))
            if neighbers:
                nx, ny, direction = random.choice(neighbers)
                stack.append((nx, ny))
                visited.add((nx, ny))
                self.grid[y][x] &= ~direction
                self.grid[ny][nx] &= ~OPPOSITE[direction]
                current = (nx, ny)
                stack.append(current)
                visited.add(current)
            else:
                current = stack.pop()

    def solve(self) -> list[tuple[int, int]]:
        """Find the shortest path from entry to exit using BFS.

        Stores the result in self.solution and self.solution_str.

        Returns:
            An ordered list of (x, y) coordinates from entry to exit,
            or an empty list if no path exists.
        """
        q: deque[tuple[int, int]] = deque()
        q.append((self.entry))
        visited = set()
        visited.add(self.entry)
        prev: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

        while q:
            x, y = q.popleft()
            if (x, y) == self.exit:
                path = [self.exit]
                directions = []
                current = self.exit
                while current != self.entry:
                    current, direction = prev[current]
                    path.append(current)
                    directions.append(direction)
                path.reverse()
                directions.reverse()
                self.solution = path
                self.solution_str = ''.join(directions)
                return path

            for key, value in DIRECTION_DELTA.items():
                if (self.grid[y][x] & key) == 0:
                    dx, dy = value
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.width and 0 <= ny < self.height)\
                       and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        prev[(nx, ny)] = ((x, y), DIRECTION_NAME[key])
                        q.append((nx, ny))
        return []

    def imperfect(self) -> None:
        """Remove one wall along the solution path to create a maze loop.

        Skips walls adjacent to the '42' pattern. Clears self.solution
        after modification since the maze structure has changed.

        Raises:
            ValueError: If no solution exists or no removable wall is found.
        """
        protected_cells = self.pattern_42 if hasattr(self, 'pattern_42')\
            else self._get_pattern_42()
        path = self.solve()
        if not path:
            raise ValueError(
                "Cannot make imperfect maze: no path from entry to exit"
                )

        candidates = []
        for x, y in path:
            for direction, (dx, dy) in DIRECTION_DELTA.items():
                nx, ny = x + dx, y + dy
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if (nx, ny) in protected_cells:
                    continue
                if self.grid[y][x] & direction:
                    candidates.append((x, y, nx, ny, direction))

        if not candidates:
            raise ValueError(
                "Cannot make imperfect maze: no removable wall found"
                )

        x, y, nx, ny, direction = random.choice(candidates)
        self.grid[y][x] &= ~direction
        self.grid[ny][nx] &= ~OPPOSITE[direction]
        self.solution = []


def print_maze(generator: MazeGenerator, show_solution: bool = True) -> None:
    """Print the maze with plain ASCII characters for debugging.

    Args:
        generator:
        The maze generator instance containing the grid and metadata.
        show_solution:
        If True, solves and overlays the solution path. Defaults to True.
    """
    if show_solution and not generator.solution:
        generator.solve()

    solution = set(generator.solution) if show_solution else set()
    pattern = generator.pattern_42 if hasattr(generator, 'pattern_42')\
        else set()

    print("+" + "---+" * generator.width)
    for y in range(generator.height):
        cell_line = "|"
        wall_line = "+"

        for x in range(generator.width):
            cell = (x, y)
            value = generator.grid[y][x]

            if cell == generator.entry:
                marker = " S "
            elif cell == generator.exit:
                marker = " E "
            elif cell in solution:
                marker = " * "
            elif cell in pattern:
                marker = " # "
            else:
                marker = "   "

            east_wall = "|" if value & EAST else " "
            south_wall = "---" if value & SOUTH else "   "
            cell_line += marker + east_wall
            wall_line += south_wall + "+"

        print(cell_line)
        print(wall_line)


if __name__ == "__main__":
    maze = MazeGenerator(9, 9, (0, 0), (8, 8), 42)
    maze.generate()
    path = maze.solve()
    print(path)
    print_maze(maze)
    maze.imperfect()
    print_maze(maze)

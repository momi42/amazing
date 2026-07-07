import os
import sys
import time
from mazegen.gen import MazeGenerator, WEST, EAST, SOUTH


GREEN = "\033[32;6;1m"
G = "\033[32m"
R = "\033[31;1m"
Y = "\033[33m"
RESET = "\033[0m"
BM = "\033[35;7;1m"
BY = "\033[33;7;1m"
BB = "\033[34;7;1m"
BR = "\033[31;7;1m"
BG = "\033[32;7;1m"
BC = "\033[36;7;1m"
BW = "\033[37;7;1m"

wall = [BB, BR, BG, BC, BW, BY, BM]


def display_menu(term_width: int, title: str, options: list[str]) -> None:
    """Render a centered ASCII box menu to the terminal.

    Args:
        term_width: The current terminal width in characters.
        title: The menu title displayed at the top of the box.
        options: A list of option strings, numbered automatically from 1.
    """
    box_width = term_width // 2
    top = "+" + "-" * (box_width - 2) + "+"
    bottom = "+" + "-" * (box_width - 2) + "+"
    title_line = f"| {title}".ljust(box_width - 1) + "|"
    mid_line = "|" + "-" * (box_width - 2) + "|"
    print(f"{R}")
    print(top.center(term_width))
    print(title_line.center(term_width))
    print(mid_line.center(term_width))
    for index, option in enumerate(options, 1):
        option_txt = f"| {index}. {option}"
        menu_line = option_txt.ljust(box_width - 1) + "|"
        print(menu_line.center(term_width))
    print(bottom.center(term_width))
    print("\n" * 3)


def _cell_display(generator: MazeGenerator,
                  x: int,
                  y: int,
                  pattern: set[tuple[int, int]],
                  path_cells: list[tuple[int, int]]) -> str:
    """Return the ANSI-colored display string for a single maze cell.

    Args:
        generator: The maze generator instance, used to check entry and exit.
        x: The column index of the cell.
        y: The row index of the cell.
        pattern: Set of (x, y) coordinates belonging to the 42 pattern.
        path_cells: List of (x, y) coordinates on the current solution path.

    Returns:
        A 3-character ANSI-escaped string representing the cell's visual state.
    """
    cell = (x, y)
    if cell == generator.entry:
        return BM + ' S ' + RESET
    if cell == generator.exit:
        return BY + ' E ' + RESET
    if cell in pattern:
        return GREEN + '███' + RESET
    if cell in path_cells:
        return R + ' ⚑ ' + RESET
    return '   '


def display_maze(
        generator: MazeGenerator,
        show_solution: bool = False,
        C: str = wall[0]) -> None:
    """Print the full maze grid to the terminal using ANSI color codes.

    Args:
        generator: The maze generator instance containing grid and metadata.
        show_solution: If True, highlights the solution path when available.
        C: ANSI color code used for wall characters.
    """
    if show_solution and hasattr(generator, 'solution'):
        sol = generator.solution
    else:
        sol = []
    pattern = generator.pattern_42 if hasattr(generator, 'pattern_42')\
        else set()
    print(C + '+' + RESET + (C + '---+' + RESET) * generator.width)
    for y in range(generator.height):
        for x in range(generator.width):
            num = generator.grid[y][x]
            print(C + '|' + RESET if num & WEST else ' ', end='')
            print(_cell_display(generator, x, y, pattern, sol), end='')
        last_num = generator.grid[y][generator.width - 1]
        print(C + '|' + RESET if last_num & EAST else ' ')

        for x in range(generator.width):
            num = generator.grid[y][x]
            print(
                C + '+' + RESET +
                (C + '---' + RESET if num & SOUTH else '   '), end='')
        print(C + '+' + RESET)


def animate_solution(
        generator: MazeGenerator,
        delay: float = 0.1,
        C: str = wall[0]) -> None:
    """Animate the solution path step-by-step from entry to exit.

    Hides the cursor during animation and restores it on exit.

    Args:
        generator: The maze generator instance with a precomputed solution.
        delay: Seconds to wait between each animation frame.
        C: ANSI color code used for wall characters.
    """
    if not generator.solution:
        print("No solution found to animate! Run solve() first.")
        return
    print("\033[?25l", end="")

    try:
        for i in range(1, len(generator.solution) + 1):
            print("\033[H", end="")
            current_visible_path = generator.solution[:i]
            draw_frame(generator, current_visible_path, C)
            sys.stdout.flush()
            time.sleep(delay)
    finally:
        print("\033[?25h")


def draw_frame(generator: MazeGenerator,
               visible_cells: list[tuple[int, int]],
               C: str = wall[0]) -> None:
    """Draw a single frame of the maze with a partial solution path visible.

    Args:
        generator:
        The maze generator instance containing the grid and metadata.
        visible_cells: The subset of solution cells to highlight in this frame.
        C: ANSI color code used for wall characters.
    """
    pattern = generator.pattern_42 if hasattr(generator, 'pattern_42')\
        else set()
    print(C + '+' + RESET + (C + '---+' + RESET) * generator.width)
    for y in range(generator.height):
        for x in range(generator.width):
            num = generator.grid[y][x]
            print(C + '|' + RESET if num & WEST else ' ', end='')
            print(
                _cell_display(generator, x, y, pattern, visible_cells), end='')
        last_num = generator.grid[y][generator.width - 1]
        print(C + '|' + RESET if last_num & EAST else ' ')

        for x in range(generator.width):
            num = generator.grid[y][x]
            print(
                C + '+' + RESET +
                (C + '---' + RESET if num & SOUTH else '   '), end='')
        print(C + '+' + RESET)


def display_logo(term_width: int) -> None:
    """Print the ASCII art A-MAZE-ING logo centered in the terminal.

    Args:
        term_width: The current terminal width in characters.
    """
    logo = [
        "  ▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄ "
        " ▄▄▄▄▄▄▄▄▄▄▄  ▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄ ",
        " ▐░░░░░░░░░░▌▐░░░░░░░░░░░░░░░░░░░▌▐░░░░░░░░░░▌"
        "▐░░░░░░░░░░░▌▐░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░▌",
        " ▐░░█▀▀▀▀█░░▌▐░░█▀▀▀▀▀▐░░█▀▀▀▀█░░▌▐░░█▀▀▀▀█░░▌"
        " ▀▀▀▀▀▀▀▀█░░▌    ▐░░█▀▀▀▀▀█░░▌▐░░█▀▀▀▀▀▀▀ ",
        " ▐░░█▄▄▄▄█░░▌▐░░█     ▐░░█    ▐░░▌▐░░█▄▄▄▄█░░▌"
        "         █░░▌▐░░█▐░░█     █░░▌▐░░█   ▄▄▄▄ ",
        " ▐░░░░░░░░░░▌▐░░█     ▐░░█    ▐░░▌▐░░░░░░░░░░▌"
        " ▄▄▄▄▄▄▄▄█░░▌▐░░█▐░░█     █░░▌▐░░█  ▐░░░░▌",
        " ▐░░█▀▀▀▀█░░▌▐░░█     ▐░░█    ▐░░▌▐░░█▀▀▀▀█░░▌"
        "▐░░░░░░░░░░░▌▐░░█▐░░█     █░░▌▐░░█    ▐░░▌",
        " ▐░░█    ▐░░▌▐░░█     ▐░░█    ▐░░▌▐░░█    ▐░░▌"
        "▐░░█▀▀▀▀▀▀▀▀ ▐░░█▐░░█     █░░▌▐░░█    ▐░░▌",
        " ▐░░█    ▐░░▌▐░░█     ▐░░█    ▐░░▌▐░░█    ▐░░▌"
        "▐░░█▄▄▄▄▄▄▄▄ ▐░░█▐░░█     █░░▌▐░░█▄▄▄▄█░░▌",
        " ▐░░█    ▐░░▌▐░░░     ▐░░█    ▐░░▌▐░░█    ▐░░▌"
        "▐░░░░░░░░░░░▌▐░░█▐░░█     █░░▌▐░░░░░░░░░░▌",
        "  ▀▀      ▀▀  ▀▀▀      ▀▀▀     ▀▀  ▀▀      ▀▀ "
        " ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀ ▀▀▀      ▀▀  ▀▀▀▀▀▀▀▀▀▀ "
    ]
    print("\n" * 2)
    for line in logo:
        print(F"{G}{line.center(term_width)}{RESET}")
    print("\n" * 2)


def display(generator: MazeGenerator) -> None:
    """Run the main interactive display loop for the maze application.

    Args:
        generator: A fully initialized maze generator instance.
    """
    term_width = os.get_terminal_size().columns
    show_solution = False
    menu_options = [
        "Re-generate a new maze",
        "Show/Hide path from entry to exit",
        "Animate solution",
        "Explore colors",
        "Quit"
    ]
    # generator.generate()
    os.system('cls' if os.name == 'nt' else 'clear')
    display_logo(term_width)
    print("\n" * 3)
    i = 0
    while True:
        # display_maze(generator, show_path)
        # display_logo(term_width)
        display_menu(term_width, "A-MAZE-ING MENU", menu_options)
        print("\n")
        choice = input(
            " " * ((term_width) // 4) + f"{GREEN}Choice? (1-5): {RESET}")
        if choice == '1':
            os.system('clear')
            # generator.seed = None
            generator.generate()
            if not generator.perfect:
                generator.imperfect()
            display_maze(generator, show_solution, wall[i])
        elif choice == '2':
            os.system('clear')
            show_solution = not show_solution
            generator.solve()
            display_maze(generator, show_solution, wall[i])

        elif choice == '3':
            os.system('clear')
            generator.solve()
            animate_solution(generator, 0.1, wall[i])
        elif choice == '4':
            os.system('clear')
            i += 1
            display_maze(generator, show_solution, wall[i])
            if i == len(wall)-1:
                i = -1
        elif choice == '5':
            os.system('clear')
            print('Adios')
            sys.exit()
        else:
            os.system('clear')
            print('Invalid choice')

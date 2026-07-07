from mazegen.gen import MazeGenerator


def write_output(generator: MazeGenerator, filepath: str) -> None:
    """Write the maze grid and metadata to a file in hexadecimal format.

    Each row of the grid is written as a string of hex digits,
    one row per line.
    Followed by a blank line, then the entry coordinates, exit coordinates,
    and the solution direction string on separate lines.

    Args:
        generator: The maze generator instance containing the grid,
                   entry, exit, and solution_str to serialize.
        filepath: Path to the output file to create or overwrite.
    """
    with open(filepath, 'w') as f:
        for row in generator.grid:
            f.write(''.join(f'{cell:X}' for cell in row) + '\n')
        f.write('\n')
        f.write(f'{generator.entry[0]},{generator.entry[1]}\n')
        f.write(f'{generator.exit[0]},{generator.exit[1]}\n')
        f.write(generator.solution_str)

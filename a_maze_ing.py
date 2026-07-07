import sys
from mazegen.config import parsing
from mazegen.gen import MazeGenerator
from mazegen.output import write_output
from mazegen.display import display


def main() -> None:
    """Run the A-MAZE-ING application from the command line.

    Parses the config file, generates and solves the maze, writes the
    output file, then launches the interactive terminal display.

    Exits with an error message if the config file is not found or
    contains invalid values.
    """
    if len(sys.argv) != 2:
        print('Usage: python3 a_maze_ing.py config.txt')
        sys.exit()

    try:
        config = parsing(sys.argv[1])
        generator = MazeGenerator(
            width=config['width'],
            height=config['height'],
            entry=config['entry'],
            exit=config['exit'],
            seed=config['seed'],
            perfect=config['perfect']
        )
        generator.generate()
        generator.solve()
        write_output(generator, config['output_file'])
        display(generator)
    except FileNotFoundError as e:
        print(f'Error: config file not found — {e}')
        sys.exit()
    except ValueError as e:
        print(f'Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()

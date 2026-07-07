from typing import Optional, Any


def parsing(path: str) -> dict[str, Any]:
    """Parse and validate a maze configuration file.

    The file should contain one ``KEY=value`` pair per line. Empty lines and
    lines starting with ``#`` are ignored. Required keys are ``WIDTH``,
    ``HEIGHT``, ``ENTRY``, ``EXIT``, ``OUTPUT_FILE``, and ``PERFECT``.
    ``SEED`` is optional.

    Args:
        path (str): Path to the configuration file.

    Raises:
        ValueError: If a required key is missing.
        ValueError: If a value cannot be converted to the expected type.
        ValueError: If width or height is not positive.
        ValueError: If the entry or exit coordinate is outside the maze.
        ValueError: If the entry and exit coordinates are the same.

    Returns:
        dict[str, Any]: Parsed configuration with normalized keys and values.
    """
    with open(path, "r") as f:
        config = {}
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            config[key] = value.strip()

    all_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    for key in all_keys:
        if key not in config:
            raise ValueError(f'{key} key is missing')
    try:
        width = int(config['WIDTH'])
        height = int(config['HEIGHT'])
        entry = tuple(map(int, config['ENTRY'].split(',')))
        exit = tuple(map(int, config['EXIT'].split(',')))
        output = config['OUTPUT_FILE']
        perfect = config['PERFECT'].lower() == 'true'
        seed: Optional[int] = int(config['SEED']) if 'SEED' in config else None
    except Exception as e:
        raise ValueError(f"Invalid config value: {e}")

    if width <= 0 or height <= 0:
        raise ValueError('🕳️ Width and Height should be positive integers 🕳️')
    if not (width > entry[0] >= 0 and height > entry[1] >= 0):
        raise ValueError('🚧 Entry is out of boundries 🚧')
    if not (width > exit[0] >= 0 and height > exit[1] >= 0):
        raise ValueError('🚧 Exit is out of boundries 🚧')
    if entry == exit:
        raise ValueError('🪃 entry and exit must be different 🪃')
    if config['PERFECT'].lower() != "true"\
       and config['PERFECT'].lower() != "false":
        raise ValueError('✔️ Perfect must be True or False💯')

    return {
        'width': width,
        'height': height,
        'entry': entry,
        'exit': exit,
        'output_file': output,
        'perfect': perfect,
        'seed': seed
    }

from collections import defaultdict

NUMERIC_KEYPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]

DIRECTIONAL_KEYPAD = [
    [None, "^", "A"],
    ["<", "v", ">"],
]


def create_coords_map(keypad):
    return {
        cell: (row, col)
        for row, row_cells in enumerate(keypad)
        for col, cell in enumerate(row_cells)
    }


def shortest_path_keys(from_key, to_key, coords) -> str:
    """Return the shortest sequence of directional arrows needed to move from `from_key`
    to `to_key`.
    """
    r_from, c_from = coords[from_key]
    r_to, c_to = coords[to_key]

    vertical_moves = "v" * (r_to - r_from) if r_to > r_from else "^" * (r_from - r_to)
    horizontal_moves = ">" * (c_to - c_from) if c_to > c_from else "<" * (c_from - c_to)

    # Attempt vertical-first if it's safe
    if (c_to > c_from) and (r_to, c_from) != coords[None]:
        return vertical_moves + horizontal_moves + "A"

    # Attempt horizontal-first if it's safe
    if (r_from, c_to) != coords[None]:
        return horizontal_moves + vertical_moves + "A"

    # Fallback: move vertically first if neither path is blocked
    return vertical_moves + horizontal_moves + "A"


def shortest_path_sequences(sequence, coords) -> list[str]:
    """Converts a string of keypad presses (e.g., "1234") into a list of arrow-key sequences.
    Each sub-sequence starts and ends with an "A" press.
    """
    keypress_chunks = []
    prev_key = "A"

    for key in sequence:
        keypress_chunks.append(shortest_path_keys(prev_key, key, coords))
        prev_key = key

    return keypress_chunks


def calculate_complexity(code: str, num_directional_keypads: int = 25) -> int:
    """Calculate the complexity of a given code.

    We exploit that the keypresses can be split into sequences starting and ending with "A",
    allowing them to be permuted, and, in turn, summarized by counts.
    """
    # Create coordinate mappings
    numeric_coords = create_coords_map(NUMERIC_KEYPAD)
    dir_coords = create_coords_map(DIRECTIONAL_KEYPAD)

    # Initialize frequency tables with numeric keypad sequences
    counts = defaultdict(int)

    # Initial sequences (on numeric keypad)
    for sequence in shortest_path_sequences(code, numeric_coords):
        counts[sequence] += 1

    # Expand sequences for each directional keypad
    for _ in range(num_directional_keypads):
        expanded_counts = defaultdict(int)

        for sequence, count in counts.items():
            for expanded_sequence in shortest_path_sequences(sequence, dir_coords):
                expanded_counts[expanded_sequence] += count

        counts = expanded_counts

    return (
        # Length of the sequence
        sum(len(sequence) * count for sequence, count in counts.items())
        # Numeric part of the code
        * int(code[:-1])
    )


if __name__ == "__main__":
    with open("input.txt") as f:
        codes = f.read().splitlines()

    # Part 1
    print(sum(calculate_complexity(code, num_directional_keypads=2) for code in codes))

    # Part 2
    print(sum(calculate_complexity(code, num_directional_keypads=25) for code in codes))

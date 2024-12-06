DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, right, down, left


def parse_input(input_str: str):
    grid = input_str.splitlines()

    rows = len(grid)
    cols = len(grid[0])

    obstructions = set()
    start = None

    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == "#":
                obstructions.add((row, col))
            elif char == "^":
                start = (row, col)

    assert start is not None

    return rows, cols, obstructions, start


def simulate(start: tuple, direction: int, obstructions: set, rows: int, cols: int):
    def step(state: tuple):
        (x, y), direction = state

        for _ in range(4):
            dx, dy = DIRECTIONS[direction]
            nx, ny = x + dx, y + dy

            # Try to move forward
            if (nx, ny) not in obstructions:
                return (nx, ny), direction

            # Try turning clockwise
            direction = (direction + 1) % 4

        raise ValueError("No valid moves")

    state = (start, direction)
    states = {state}

    while True:
        state = step(state)

        # Check if we are in a cycle
        if state in states:
            return None

        # Check if we are out of bounds
        (x, y), _ = state
        if not (0 <= x < rows and 0 <= y < cols):
            break

        states.add(state)

    return states


def guard_positions(
    start: tuple, direction: int, obstructions: set, rows: int, cols: int
):
    states = simulate(start, direction, obstructions, rows, cols)

    assert states is not None

    return set(position for position, _ in states)


def part1(start: tuple, direction: int, obstructions: set, rows: int, cols: int):
    return len(guard_positions(start, direction, obstructions, rows, cols))


def part2(start: tuple, direction: int, obstructions: set, rows: int, cols: int):
    # It only makes sense to add obstructions to the path of the guard
    positions = guard_positions(start, direction, obstructions, rows, cols)
    return sum(
        1
        for position in positions
        # Check if we have a cycle with the new obstruction
        if simulate(start, direction, obstructions | {position}, rows, cols) is None
    )


if __name__ == "__main__":
    with open("input.txt") as f:
        rows, cols, obstructions, start = parse_input(f.read())

    print(part1(start, 0, obstructions, rows, cols))
    print(part2(start, 0, obstructions, rows, cols))

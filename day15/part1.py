DIRS = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def parse_input(input: str):
    grid_str, moves_str = input.split("\n\n")

    grid = [list(row) for row in grid_str.splitlines()]
    moves = moves_str.replace("\n", "")

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "@":
                grid[x][y] = "."
                return x, y, grid, moves

    raise ValueError("No starting position found")


def step(x: int, y: int, direction: str):
    dx, dy = DIRS[direction]
    return x + dx, y + dy


class InvalidMoveError(Exception):
    pass


def try_move(x: int, y: int, direction: str, grid: list):
    mx, my = step(x, y, direction)

    if grid[mx][my] == "#":
        raise InvalidMoveError

    if grid[mx][my] == "O":
        try_move(mx, my, direction, grid)

    grid[mx][my] = grid[x][y]
    grid[x][y] = "."

    return mx, my


def simulate(x, y, grid, moves):
    for move in moves:
        try:
            x, y = try_move(x, y, move, grid)
        except InvalidMoveError:
            pass

    return grid


def gps_score(grid):
    return sum(
        x * 100 + y
        for x, row in enumerate(grid)
        for y, cell in enumerate(row)
        if cell in {"O", "["}
    )


if __name__ == "__main__":
    with open("input.txt") as f:
        x, y, grid, moves = parse_input(f.read())

    print(gps_score(simulate(x, y, grid, moves)))

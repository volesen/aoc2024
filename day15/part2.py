import copy

from part1 import InvalidMoveError, gps_score, step
from part1 import parse_input as parse_input_part1

SUBS = {"#": "##", "O": "[]", ".": "..", "@": "@."}


def parse_input(input: str):
    return parse_input_part1(str.translate(input, str.maketrans(SUBS)))


def try_move_box(x: int, y: int, direction: str, grid: list[list[str]]):
    mx, my = step(x, y, direction)

    if grid[mx][my] == "#" or grid[mx][my + 1] == "#":
        raise InvalidMoveError

    if direction == ">" and grid[mx][my + 1] == "[":
        try_move_box(mx, my + 1, direction, grid)

    if direction == "<" and grid[mx][my - 1] == "[":
        try_move_box(mx, my - 1, direction, grid)

    if direction in {"^", "v"} and grid[mx][my] == "[":
        try_move_box(mx, my, direction, grid)

    if direction in {"^", "v"} and grid[mx][my] == "]":
        try_move_box(mx, my - 1, direction, grid)

    if direction in {"^", "v"} and grid[mx][my + 1] == "[":
        try_move_box(mx, my + 1, direction, grid)

    grid[x][y] = "."
    grid[x][y + 1] = "."

    grid[mx][my] = "["
    grid[mx][my + 1] = "]"


def try_move(x: int, y: int, direction: str, grid: list) -> tuple:
    mx, my = step(x, y, direction)

    if grid[mx][my] == "#":
        raise InvalidMoveError

    if grid[mx][my] == "[":
        try_move_box(mx, my, direction, grid)

    elif grid[mx][my] == "]":
        try_move_box(mx, my - 1, direction, grid)

    return mx, my


def simulate(x, y, grid, moves):
    for move in moves:
        checkpoint = copy.deepcopy(grid)
        try:
            x, y = try_move(x, y, move, grid)
        except InvalidMoveError:
            grid = checkpoint  # Backtrack

    return grid


if __name__ == "__main__":
    with open("input.txt") as f:
        x, y, grid, moves = parse_input(f.read())

    print(gps_score(simulate(x, y, grid, moves)))

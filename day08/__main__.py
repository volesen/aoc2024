from collections import defaultdict
from itertools import combinations


def parse_input(input: str):
    grid = input.splitlines()
    rows, cols = len(grid), len(grid[0])

    antennas = defaultdict(list)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell.isalnum():
                antennas[cell].append((x, y))

    return rows, cols, antennas


def within_bounds(p, rows, cols):
    return 0 <= p[0] < cols and 0 <= p[1] < rows


def antinodes(a: tuple, b: tuple, rows: int, cols: int):
    a_x, a_y = a
    b_x, b_y = b

    delta_x = b_x - a_x
    delta_y = b_y - a_y

    an1 = (a_x - delta_x, a_y - delta_y)

    if within_bounds(an1, rows, cols):
        yield an1

    an2 = (b_x + delta_x, b_y + delta_y)
    if within_bounds(an2, rows, cols):
        yield an2


def part1(antennas: dict, rows: int, cols: int):
    nodes = set()

    for coords in antennas.values():
        for a, b in combinations(coords, 2):
            nodes.update(antinodes(a, b, rows, cols))

    return len(nodes)


def antinodes_w_harmonics(a: tuple, b: tuple, rows: int, cols: int):
    a_x, a_y = a
    b_x, b_y = b

    delta_x = b_x - a_x
    delta_y = b_y - a_y

    # Away from `b`
    x, y = a_x, a_y
    while within_bounds((x, y), rows, cols):
        yield x, y
        x += delta_x
        y += delta_y

    # Towards `b`
    x, y = a_x, a_y
    while within_bounds((x, y), rows, cols):
        yield x, y
        x -= delta_x
        y -= delta_y


def part2(antennas: dict, rows: int, cols: int):
    nodes = set()

    for coords in antennas.values():
        for a, b in combinations(coords, 2):
            nodes.update(antinodes_w_harmonics(a, b, rows, cols))

    return len(nodes)


if __name__ == "__main__":
    with open("input.txt") as f:
        rows, cols, parsed = parse_input(f.read())

    print(part1(parsed, rows, cols))
    print(part2(parsed, rows, cols))

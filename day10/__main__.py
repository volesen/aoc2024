from functools import cache


def parse_map(map: str):
    return [[int(cell) for cell in row] for row in map.splitlines()]


def get_neighbors(x: int, y: int, rows: int, cols: int):
    return (
        (x + dx, y + dy)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if 0 <= x + dx < rows and 0 <= y + dy < cols
    )


def part1(grid: list):
    rows, cols = len(grid), len(grid[0])

    @cache
    def reachable_nines(x: int, y: int) -> set:
        height = grid[x][y]

        if height == 9:
            return {(x, y)}

        nines = set()
        for nx, ny in get_neighbors(x, y, rows, cols):
            if grid[nx][ny] == 1 + height:
                nines |= reachable_nines(nx, ny)

        return nines

    return sum(
        len(reachable_nines(x, y))
        for x, row in enumerate(grid)
        for y, cell in enumerate(row)
        if cell == 0
    )


def part2(grid: list):
    rows, cols = len(grid), len(grid[0])

    @cache
    def num_hiking_trails(x: int, y: int) -> int:
        height = grid[x][y]

        if height == 9:
            return 1

        return sum(
            num_hiking_trails(nx, ny)
            for (nx, ny) in get_neighbors(x, y, rows, cols)
            if grid[nx][ny] == 1 + height
        )

    return sum(
        num_hiking_trails(x, y)
        for x, row in enumerate(grid)
        for y, cell in enumerate(row)
        if cell == 0
    )


if __name__ == "__main__":
    with open("input.txt") as f:
        grid = parse_map(f.read())

    print(part1(grid))
    print(part2(grid))

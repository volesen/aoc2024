DIRS = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]


def part1(grid: list[str]):
    rows, cols = len(grid), len(grid[0])

    def extract_in_direction(x, y, dx, dy, n=4):
        return "".join(
            [
                grid[x + i * dx][y + i * dy]
                for i in range(n)
                if 0 <= x + i * dx < rows and 0 <= y + i * dy < cols
            ]
        )

    return sum(
        1
        for x in range(rows)
        for y in range(cols)
        for dx, dy in DIRS
        if extract_in_direction(x, y, dx, dy) == "XMAS"
    )


def part2(grid: list[str]):
    rows, cols = len(grid), len(grid[0])

    def is_x_mas(x, y):
        return (
            grid[x][y] == "A"
            # Main diagonal
            and {grid[x - 1][y - 1], grid[x + 1][y + 1]} == {"M", "S"}
            # Anti-diagonal
            and {grid[x + 1][y - 1], grid[x - 1][y + 1]} == {"M", "S"}
        )

    return sum(
        1 for x in range(1, rows - 1) for y in range(1, cols - 1) if is_x_mas(x, y)
    )


if __name__ == "__main__":
    with open("input.txt") as f:
        grid = f.read().splitlines()

    print(part1(grid))
    print(part2(grid))

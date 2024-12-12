def parse_input(data):
    return [list(row) for row in data.splitlines()]


def get_neighbors(x, y):
    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        yield x + dr, y + dc


def within_bounds(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols


def find_regions(grid):
    rows, cols = len(grid), len(grid[0])

    regions = []
    visited = set()

    def flood_fill(x, y, plant):
        if (
            not within_bounds(x, y, rows, cols)
            or grid[x][y] != plant
            or (x, y) in visited
        ):
            return

        visited.add((x, y))
        yield (x, y)

        for nx, ny in get_neighbors(x, y):
            yield from flood_fill(nx, ny, plant)

    for x in range(rows):
        for y in range(cols):
            if (x, y) not in visited:
                region = set(flood_fill(x, y, grid[x][y]))
                regions.append(region)

    return regions


def perimeter(region):
    return sum(
        (nx, ny) not in region for x, y in region for nx, ny in get_neighbors(x, y)
    )


def area(region):
    return len(region)


def price(region):
    return area(region) * perimeter(region)


def count_corners(x, y, region):
    corners = 0

    # Diagonal neighbors
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        # Check exterior corner
        if (x + dx, y) not in region and (x, y + dy) not in region:
            corners += 1

        # Check interior corner
        if (
            (x + dx, y + dy) not in region
            and (x, y + dy) in region
            and (x + dx, y) in region
        ):
            corners += 1

    return corners


def corners(region):
    return sum(count_corners(x, y, region) for x, y in region)


def price_w_bulk_discount(region):
    # We exploit the fact that the number of segments is equal to the number of corners
    return area(region) * corners(region)


if __name__ == "__main__":
    with open("input.txt") as f:
        grid = parse_input(f.read())

    regions = find_regions(grid)

    # Part 1
    print(sum(price(region) for region in regions))

    # Part 2
    print(sum(price_w_bulk_discount(region) for region in regions))

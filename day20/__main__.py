from collections import deque


def parse_input(input: str):
    grid = [list(row) for row in input.splitlines()]

    start = None
    end = None

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "S":
                start = (x, y)

            if cell == "E":
                end = (x, y)

    return grid, start, end


def is_valid(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != "#"


def manhattan(a, b=(0, 0)):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(x, y, radius=1):
    return (
        (x + dx, y + dy)
        for dx in range(-radius, radius + 1)
        for dy in range(-radius, radius + 1)
        if manhattan((dx, dy)) <= radius
    )


def find_distances(start, end, grid):
    distances = {start: 0}
    queue = deque([start])

    while queue:
        current = queue.popleft()

        for neighbor in get_neighbors(*current):
            if not is_valid(*neighbor, grid) or neighbor in distances:
                continue

            distances[neighbor] = distances[current] + 1
            queue.append(neighbor)

    return distances


def count_shortcuts(distances, radius, threshold):
    return sum(
        1
        for point in distances.keys()
        for neighbor in get_neighbors(*point, radius=radius)
        if neighbor in distances
        # Check the improvement made by taking the shortcut
        and (
            distances[neighbor] - distances[point] - manhattan(point, neighbor)
            >= threshold
        )
    )


if __name__ == "__main__":
    with open("input.txt") as f:
        grid, start, end = parse_input(f.read())

    distances = find_distances(end, start, grid)

    # Part 1
    print(count_shortcuts(distances, radius=2, threshold=100))

    # Part 2
    print(count_shortcuts(distances, radius=20, threshold=100))

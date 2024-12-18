from collections import deque

ROWS = 70 + 1
COLS = 70 + 1


def parse_positions(positions):
    return [
        tuple(int(coord) for coord in line.split(",")) for line in positions.split("\n")
    ]


def neighbours(x, y):
    return [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]


def within_bounds(x, y):
    return 0 <= x < ROWS and 0 <= y < COLS


def shortest_distance(start, end, obstacles):
    queue = deque([(0, start)])
    visited = set()

    while queue:
        distance, (x, y) = queue.popleft()

        if (x, y) == end:
            return distance

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for neighbour in neighbours(x, y):
            nx, ny = neighbour

            if neighbour in obstacles:
                continue

            if not within_bounds(nx, ny):
                continue

            queue.append((distance + 1, neighbour))

    return None


def first_blocking_obstacle(start, end, positions):
    # Plan-of-attack: Binary search for the first obstacle that blocks the path
    low = 0
    high = len(positions)

    while low < high:
        mid = (low + high) // 2
        obstacles = set(positions[: mid + 1])

        if shortest_distance(start, end, obstacles) is None:
            high = mid
        else:
            low = mid + 1

    return positions[low]


if __name__ == "__main__":
    with open("input.txt") as f:
        positions = parse_positions(f.read())

    start = (0, 0)
    end = (ROWS - 1, COLS - 1)

    # Part 1
    obstacles = set(positions[:1024])
    print(shortest_distance(start, end, obstacles))

    # Part 2
    print(first_blocking_obstacle(start, end, positions))

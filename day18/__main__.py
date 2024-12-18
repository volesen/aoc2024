from collections import deque

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
ROWS = 71
COLS = 71


def parse_positions(positions):
    return [
        tuple(int(coord) for coord in line.split(",")) for line in positions.split("\n")
    ]


def neighbours(x, y):
    return [
        (x + dx, y + dy) for dx, dy in DIRS if 0 <= x + dx < ROWS and 0 <= y + dy < COLS
    ]


def shortest_distance(start, end, obstacles):
    queue = deque([(0, start)])
    visited = {start}

    while queue:
        distance, current = queue.popleft()

        if current == end:
            return distance

        for neighbour in neighbours(*current):
            if neighbour not in visited and neighbour not in obstacles:
                visited.add(neighbour)
                queue.append((distance + 1, neighbour))

    return None


def first_blocking_obstacle(start, end, positions):
    # Binary search for the first obstacle that prevents reaching the end.
    low, high = 0, len(positions)

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

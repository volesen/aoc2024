import heapq
from collections import defaultdict

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse_input(input: str):
    grid = input.splitlines()

    start = None
    end = None

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "S":
                start = (x, y)

            if cell == "E":
                end = (x, y)

    return grid, start, end


def cost_and_next(state):
    x, y, direction = state
    # Step
    dx, dy = DIRECTIONS[direction]
    yield 1, (x + dx, y + dy, direction)
    # Rotate clockwise
    yield 1000, (x, y, (direction + 1) % 4)
    # Rotate counter clockwise
    yield 1000, (x, y, (direction - 1) % 4)


def is_valid(state, grid):
    x, y, _ = state
    return grid[x][y] != "#"


def is_at_end(state, end):
    return state[:2] == end[:2]  # Ignore direction


def dijkstra_w_path(start, end, grid):
    queue = [(0, start)]

    costs = defaultdict(lambda: float("inf"))
    came_from = defaultdict(list)

    while queue:
        cost, state = heapq.heappop(queue)

        if is_at_end(state, end):
            # NOTE: We could break already when the cost of the end state strictly increases
            continue

        for action_cost, new_state in cost_and_next(state):
            new_cost = cost + action_cost

            if not is_valid(new_state, grid):
                continue

            if new_cost > costs[new_state]:
                continue

            if new_cost == costs[new_state]:
                came_from[new_state].append(state)
                continue

            costs[new_state] = new_cost
            came_from[new_state] = [state]

            heapq.heappush(queue, (new_cost, new_state))

    return costs, came_from


def follow_came_from(state, came_from, visited):
    if state in visited:
        return

    visited.add(state)

    for prev_state in came_from[state]:
        follow_came_from(prev_state, came_from, visited)


if __name__ == "__main__":
    with open("input.txt") as file:
        grid, start, end = parse_input(file.read())

    costs, came_from = dijkstra_w_path(
        (*start, 1),
        (*end, None),
        grid,
    )

    # Part 1
    optimal_end = min(
        ((*end, direction) for direction in range(4)),
        key=lambda state: costs[state],
    )

    print(costs[optimal_end])

    # Part 2
    visited = set()
    follow_came_from(optimal_end, came_from, visited)

    print(len({state[:2] for state in visited}))

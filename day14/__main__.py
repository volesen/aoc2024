import re
import numpy as np

WIDTH = 101
HEIGHT = 103


def parse_input(input: str):
    # Quick n' dirty
    return [[int(x) for x in re.findall(r"-?\d+", line)] for line in input.splitlines()]


def step_single(px, py, vx, vy):
    return (px + vx) % WIDTH, (py + vy) % HEIGHT, vx, vy


def step(states):
    for i, state in enumerate(states):
        states[i] = step_single(*state)

    return states


def safety_factor(states: list):
    first = second = third = fourth = 0

    SPLIT_X = WIDTH // 2
    SPLIT_Y = HEIGHT // 2

    for px, py, _, _ in states:
        if px < SPLIT_X and py < SPLIT_Y:
            first += 1

        elif px > SPLIT_X and py < SPLIT_Y:
            second += 1

        elif px < SPLIT_X and py > SPLIT_Y:
            third += 1

        elif px > SPLIT_X and py > SPLIT_Y:
            fourth += 1

    return first * second * third * fourth


def to_grid(states):
    grid = np.zeros((HEIGHT, WIDTH))

    for px, py, _, _ in states:
        grid[py, px] += 1

    return grid


def part1(states: list):
    states = states.copy()

    for _ in range(100):
        states = step(states)

    return safety_factor(states)


def part2(states: list):
    states = states.copy()

    # Assumption: The christmas tree will likely be in a single quadrant
    # Plan-of-attack: Find the smallest safety factor among 10,000 iterations
    min_safety = float("inf")
    min_iteration = -1

    for i in range(10_000):
        states = step(states)
        safety = safety_factor(states)

        if safety < min_safety:
            min_safety = safety
            min_iteration = i

    return min_iteration


if __name__ == "__main__":
    with open("input.txt") as f:
        points = parse_input(f.read())

    print(part1(points))

    print(part2(points))

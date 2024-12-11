from math import log10
from functools import cache


def parse(stones: str):
    return [int(x) for x in stones.split()]


def num_digits(n):
    return int(log10(n)) + 1


def split_digits(n):
    digits = num_digits(n)
    half = digits // 2
    return n // 10**half, n % 10**half


def step(stone):
    if stone == 0:
        yield 1
    elif (digits := num_digits(stone)) % 2 == 0:
        half = digits // 2
        yield stone // 10**half
        yield stone % 10**half
    else:
        yield stone * 2024


@cache
def num_stones(stone: int, blinks: int):
    if blinks == 0:
        return 1

    stones = step(stone)

    return sum(num_stones(stone, blinks - 1) for stone in stones)


if __name__ == "__main__":
    with open("input.txt") as f:
        stones = parse(f.read())

    # Part 1
    print(sum(num_stones(stone, blinks=25) for stone in stones))

    # Part 2
    print(sum(num_stones(stone, blinks=75) for stone in stones))

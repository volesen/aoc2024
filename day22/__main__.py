from typing import Iterable
from itertools import islice
from collections import defaultdict


def parse_input(secret_numbers: str) -> list[int]:
    return [int(x) for x in secret_numbers.splitlines()]


def step(state: int) -> int:
    state = (state ^ (state << 6)) & 0xFFFFFF
    state = (state ^ (state >> 5)) & 0xFFFFFF
    state = (state ^ (state << 11)) & 0xFFFFFF

    return state


def prng(state: int) -> Iterable[int]:
    while True:
        yield state
        state = step(state)


def take(iterable: Iterable, n: int) -> list:
    return list(islice(iterable, n))


def last_digit(n: int) -> int:
    return n % 10


def find_max_profit(price_series: list[list[int]]) -> int:
    profits = defaultdict(int)

    for prices in price_series:
        seen = set()

        # Sliding window of 5 days
        for i in range(len(prices) - 4):
            p0, p1, p2, p3, p4 = prices[i : i + 5]

            price_changes = (p1 - p0, p2 - p1, p3 - p2, p4 - p3)

            if price_changes not in seen:
                seen.add(price_changes)
                profits[price_changes] += p4

    return max(profits.values())


if __name__ == "__main__":
    with open("input.txt") as f:
        seeds = parse_input(f.read())

    # Part 1
    random_number_series = [take(prng(seed), n=2_001) for seed in seeds]
    print(sum(series[-1] for series in random_number_series))

    # Part 2
    price_series = [[last_digit(n) for n in series] for series in random_number_series]
    print(find_max_profit(price_series))

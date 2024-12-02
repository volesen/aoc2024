from functools import cache


def is_safe(levels: list[int], can_skip: bool) -> bool:
    def is_current_safe(current: int, previous: int, increasing: bool) -> bool:
        """
        - The levels are either all increasing or all decreasing.
        - Any two adjacent levels differ by at least one and at most three.
        """
        if increasing and levels[current] <= levels[previous]:
            return False

        if not increasing and levels[current] >= levels[previous]:
            return False

        if abs(levels[current] - levels[previous]) > 3:
            return False

        return True

    @cache
    def is_rest_safe(
        current: int, previous: int, increasing: bool, can_skip: bool
    ) -> bool:
        if current >= len(levels):
            return True

        return (
            is_current_safe(current, previous, increasing)
            and is_rest_safe(current + 1, current, increasing, can_skip)
        ) or (
            can_skip
            and (is_rest_safe(current + 1, previous, increasing, can_skip=False))
        )

    return (
        # Do not skip the first levels
        is_rest_safe(1, 0, levels[1] > levels[0], can_skip)
        # Skip the second level
        or (can_skip and is_rest_safe(2, 0, levels[2] > levels[0], can_skip=False))
        # Skip the first level
        or (can_skip and is_rest_safe(2, 1, levels[2] > levels[1], can_skip=False))
    )


if __name__ == "__main__":
    with open("day02/input.txt") as f:
        levels = [[int(x) for x in line.split()] for line in f]

    # Part 1
    print(sum(1 for level in levels if is_safe(level, can_skip=False)))

    # Part 2
    print(sum(1 for level in levels if is_safe(level, can_skip=True)))

def is_safe(levels: list[int]) -> bool:
    """
    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.
    """

    increasing = levels[0] < levels[1]

    for i in range(1, len(levels)):
        if increasing and levels[i - 1] >= levels[i]:
            return False

        if not increasing and levels[i - 1] <= levels[i]:
            return False

        if abs(levels[i - 1] - levels[i]) > 3:
            return False

    return True


def level_removed(level: list[int]):
    """Yields all possible levels where one level has been removed."""
    for i in range(len(level)):
        yield level[:i] + level[i + 1 :]


def is_safe_with_skip(
    levels: list[int],
):
    return any(is_safe(level) for level in level_removed(levels))


if __name__ == "__main__":
    with open("day02/input.txt") as f:
        levels = [[int(x) for x in line.split()] for line in f]

    # Part 1
    print(sum(1 for level in levels if is_safe(level)))

    # Part 2
    print(sum(1 for level in levels if is_safe_with_skip(level)))

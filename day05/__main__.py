from functools import cmp_to_key


def parse_input(input_str: str) -> tuple[list, list]:
    rules_str, updates_str = input_str.split("\n\n")
    return (
        [tuple(map(int, rule.split("|"))) for rule in rules_str.splitlines()],
        [list(map(int, line.split(","))) for line in updates_str.splitlines()],
    )


def check_ordering(update: list[int], rules: list[tuple[int, int]]) -> bool:
    # Validate ordering against dependency rules
    seen: set[int] = set()

    for page in update:
        for before, after in rules:
            if before == page and after in seen:
                return False

        seen.add(page)

    return True


def get_middle_value(sequence: list[int]) -> int:
    return sequence[len(sequence) // 2]


def part1(rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    return sum(
        get_middle_value(update) for update in updates if check_ordering(update, rules)
    )


def part2(rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    rules_set = set(rules)

    # I tried a topological sort, but the ordering is cyclic
    # However, all pairs of pages appear in the rules, so we can compare them directly
    def compare(x, y):
        if x == y:
            return 0

        if (x, y) in rules_set:
            return 1

        return -1

    return sum(
        get_middle_value(sorted(update, key=cmp_to_key(compare)))
        for update in updates
        if not check_ordering(update, rules)
    )


if __name__ == "__main__":
    with open("input.txt") as f:
        rules, updates = parse_input(f.read())

    print(part1(rules, updates))
    print(part2(rules, updates))

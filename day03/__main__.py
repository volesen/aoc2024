import re


def parse_input(corrupted_instructions: str) -> list[tuple]:
    # Defines a scanner that lexes the instructions and their arguments
    scanner = re.Scanner(
        [
            (r"do\(\)", lambda scanner, token: ("do",)),
            (r"don't\(\)", lambda scanner, token: ("dont",)),
            (
                r"mul\((\d+),(\d+)\)",
                lambda scanner, token: (
                    "mul",
                    (
                        int(scanner.match.group(1)),
                        int(scanner.match.group(2)),
                    ),
                ),
            ),
            # Everything else is ignored
            (r".", None),
            (r"\s+", None),
        ]
    )

    # Scan the input and ensure that the scanner consumed the entire input
    instructions, rest = scanner.scan(corrupted_instructions)
    assert not rest

    return instructions


def part1(instructions: list[tuple]) -> int:
    result = 0

    for instruction in instructions:
        match instruction:
            case ("mul", (x, y)):
                result += x * y
            case _:
                pass

    return result


def part2(instructions: list[tuple]) -> int:
    result = 0
    enabled = True

    for instruction in instructions:
        match instruction:
            case ("do",):
                enabled = True
            case ("dont",):
                enabled = False
            case ("mul", (x, y)):
                if enabled:
                    result += x * y

    return result


if __name__ == "__main__":
    with open("day03/input.txt") as f:
        corrupted_instructions = f.read()

    instructions = parse_input(corrupted_instructions)

    print(part1(instructions))
    print(part2(instructions))

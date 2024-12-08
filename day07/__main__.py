from math import log10
from operator import add, mul


def parse_input(input: str):
    eqns = []

    for line in input.splitlines():
        results, operands = line.split(":")

        results = int(results)
        operands = [int(operand) for operand in operands.split()]

        eqns.append((results, operands))

    return eqns


def concat(a: int, b: int):
    num_digits = int(log10(b)) + 1

    return a * 10**num_digits + b


def can_reach_target(
    target: int,
    current: int,
    operands: list,
    operations: list,
):
    if not operands:
        return current == target

    return any(
        can_reach_target(
            target,
            op(current, operands[0]),
            operands[1:],
            operations,
        )
        for op in operations
    )


def total_calibration_result(
    eqns: list,
    operations: list,
):
    return sum(
        target
        for target, operands in eqns
        if can_reach_target(target, operands[0], operands[1:], operations)
    )


if __name__ == "__main__":
    with open("day07/input.txt") as f:
        input = parse_input(f.read())

    # Part 1
    print(total_calibration_result(input, [add, mul]))

    # Part 2
    print(total_calibration_result(input, [add, mul, concat]))

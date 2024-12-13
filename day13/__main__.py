import re
from fractions import Fraction


PRIZE_DIFF = 10_000_000_000_000


def parse_input(input: str):
    # HACK: Quick and dirty parsing
    return [
        [Fraction(x) for x in re.findall(r"\d+", line)] for line in input.split("\n\n")
    ]


def cost(ax, ay, bx, by, px, py) -> int | None:
    """
    Plan-of-attack: solve (ax, ay) * m + (bx, by) * mn = (px, py) using Cramer's rule

    As long as the system is non-singular, the solution is unique, and the optimal solution
    is the given solution if m and n are natural numbers.
    """
    det = ax * by - ay * bx

    if det == 0:
        raise ValueError("System is singular")

    det_m = px * by - py * bx
    det_n = ax * py - ay * px

    m = det_m / det
    n = det_n / det

    if m < 0 or n < 0:
        return None

    if m.denominator != 1 or n.denominator != 1:
        return None

    return 3 * m.numerator + n.numerator


if __name__ == "__main__":
    with open("input.txt") as f:
        claw_machines = parse_input(f.read())

    # Part 1
    total_cost = 0

    for claw_machine in claw_machines:
        total_cost += cost(*claw_machine) or 0

    print(total_cost)

    # Part 2
    total_cost = 0

    for ax, ay, bx, by, px, py in claw_machines:
        total_cost += (
            cost(
                ax,
                ay,
                bx,
                by,
                px + PRIZE_DIFF,
                py + PRIZE_DIFF,
            )
            or 0
        )

    print(total_cost)

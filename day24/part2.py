from part1 import parse_input
from query import query

NUM_BITS = 45

# Plan of attack: Identify blocks that do not match a ripple-carry adder
# Implementing a "triplestore" was a bit overkill, but my train ride was long
FULL_ADDER_QUERY = [
    ("?cn", "XOR", "?xor_xn_yn", "?zn"),
    ("?xn", "XOR", "?yn", "?xor_xn_yn"),
    ("?xn", "AND", "?yn", "?and_xn_yn"),
    ("?xor_xn_yn", "AND", "?cn", "?and_xor_xn_yn_cn"),
    ("?and_xn_yn", "OR", "?and_xor_xn_yn_cn", "?cnp1"),
]


if __name__ == "__main__":
    with open("input.txt") as f:
        inputs, wires = parse_input(f.read())

    # Double the assertions as the operators are commutative
    facts = []
    for a, op, b, c in wires:
        facts.append((a, op, b, c))
        facts.append((b, op, a, c))

    # Finally, query the facts

    for n in range(1, NUM_BITS):
        matches = query(
            FULL_ADDER_QUERY,
            facts,
            [{"?xn": f"x{n:02}", "?yn": f"y{n:02}", "?zn": f"z{n:02}"}],
        )

        if not list(matches):
            print(n)

    # I manually found the swaps from here

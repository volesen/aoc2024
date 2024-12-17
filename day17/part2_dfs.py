from utils import parse_input


def get_outputs(a):
    """
    Translated and optimized from the specific input
    """
    assert a

    output = []

    while a != 0:
        b = a % 8
        b ^= 1
        c = a >> b
        b ^= 5
        b ^= c
        a = a >> 3
        output.append(b % 8)

    return output


def find_quines(a, n, instrs):
    if get_outputs(a) != instrs[-n:]:
        return

    if n == len(instrs):
        yield a

    for i in range(8):
        yield from find_quines(8 * a + i, n + 1, instrs)


if __name__ == "__main__":
    with open("input.txt") as f:
        program = f.read().strip()

    regs, instrs = parse_input(program)

    for quine in find_quines(4, 1, instrs):
        print(quine)

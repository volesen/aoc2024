import re

INPUT_PATTERN = re.compile(r"([a-z0-9]+): ([0-9]+)")
WIRE_PATTERN = re.compile(r"([a-z0-9]+) ([A-Z]+) ([a-z0-9]+) -> ([a-z0-9]+)")


def parse_input(input: str):
    inputs_str, wires_str = input.split("\n\n")

    inputs = dict(INPUT_PATTERN.findall(inputs_str))
    wires = WIRE_PATTERN.findall(wires_str)

    return inputs, wires


def evaluate(inputs, wires):
    graph = {c: (a, op, b) for a, op, b, c in wires}

    values = {k: int(v) for k, v in inputs.items()}

    def dfs(node):
        if node in values:
            return values[node]

        match graph[node]:
            case a, "AND", b:
                result = dfs(a) & dfs(b)

            case a, "OR", b:
                result = dfs(a) | dfs(b)

            case a, "XOR", b:
                result = dfs(a) ^ dfs(b)

        values[node] = result
        return result

    for wire in graph:
        dfs(wire)

    return values


if __name__ == "__main__":
    with open("input.txt") as f:
        inputs, wires = parse_input(f.read())

    values = evaluate(inputs, wires)

    print(
        int(
            "".join(
                str(values[node])
                for node in sorted(values, reverse=True)
                if node.startswith("z")
            ),
            2,
        )
    )

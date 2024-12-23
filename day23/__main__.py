from collections import defaultdict


def parse_graph(edges: str):
    neighbors = defaultdict(set)

    for line in edges.splitlines():
        a, b = line.split("-")
        neighbors[b].add(a)
        neighbors[a].add(b)

    return sorted(neighbors), neighbors


def find_three_cycles(nodes, neighbors):
    return {
        tuple(sorted((a, b, c)))
        for a in neighbors
        for b in neighbors[a]
        for c in neighbors[b]
        # Tie the knot
        if c in neighbors[a]
    }


def find_maximum_cliques(nodes, neighbors):
    cliques = []

    def bron_kerbosch(r, p, x):
        if not p and not x:
            cliques.append(r)
            return

        for v in p.copy():
            bron_kerbosch(
                r.union({v}),
                p.intersection(neighbors[v]),
                x.intersection(neighbors[v]),
            )
            p.remove(v)
            x.add(v)

    bron_kerbosch(set(), set(nodes), set())

    return cliques


if __name__ == "__main__":
    with open("input.txt") as f:
        nodes, neighbors = parse_graph(f.read())

    # Part 1
    three_cycles = find_three_cycles(nodes, neighbors)
    print(
        sum(1 for cycle in three_cycles if any(node.startswith("t") for node in cycle))
    )

    # Part 2
    max_clique = max(find_maximum_cliques(nodes, neighbors), key=len)
    print(",".join(sorted(max_clique)))

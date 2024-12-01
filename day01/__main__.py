from collections import Counter


def part1(left: list[int], right: list[int]) -> int:
    return sum(abs(l - r) for l, r in zip(sorted(left), sorted(right)))


def part2(left: list[int], right: list[int]) -> int:
    right_counts = Counter(right)

    return sum(right_counts[l] * l for l in left if l in right_counts)


def main():
    left, right = [], []

    with open("input.txt") as f:
        for line in f:
            l, r = line.split()

            left.append(int(l))
            right.append(int(r))

    print(part1(left, right))
    print(part2(left, right))


if __name__ == "__main__":
    main()

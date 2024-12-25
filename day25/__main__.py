WIDTH = 5
HEIGHT = 7


def parse_input(input):
    return [schematic.splitlines() for schematic in input.split("\n\n")]


def extract_heights(schematic):
    return tuple(
        sum(1 for cell in column if cell == "#")
        # Transpose the schematic
        for column in zip(*schematic)
    )


def is_key(schematic):
    return all(cell == "#" for cell in schematic[0])


def key_fits_lock(key, lock):
    return all(
        key_height + lock_height <= HEIGHT for key_height, lock_height in zip(key, lock)
    )


if __name__ == "__main__":
    with open("input.txt") as f:
        schematics = parse_input(f.read())

    key_heights = [
        extract_heights(schematic) for schematic in schematics if is_key(schematic)
    ]

    lock_heights = [
        extract_heights(schematic) for schematic in schematics if not is_key(schematic)
    ]

    print(
        sum(
            1
            for key in key_heights
            for lock in lock_heights
            if key_fits_lock(key, lock)
        )
    )

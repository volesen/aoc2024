from collections import deque

MAX_FILE_SIZE = 10


def parse_disk_map(input: str) -> list:
    disk_map = []
    id = 0
    for pos, c in enumerate(input):
        size = int(c)

        if pos % 2 == 0:
            disk_map.append((id, size, pos))
            id += 1
        else:
            disk_map.append((None, size, pos))

    return disk_map


def to_dense(disk_map: list):
    return sum(([id] * size for id, size, _ in disk_map), start=[])


def checksum(dense_disk_map: list) -> int:
    return sum(i * id for i, id in enumerate(dense_disk_map) if id is not None)


def defrag_by_block(dense_disk_map: list) -> list:
    i = 0
    j = len(dense_disk_map) - 1
    while i < j:
        # Move i to the next free block
        if dense_disk_map[i] is not None:
            i += 1
            continue

        # Move j to next occupied block
        if dense_disk_map[j] is None:
            j -= 1
            continue

        dense_disk_map[i], dense_disk_map[j] = dense_disk_map[j], dense_disk_map[i]

        i += 1
        j -= 1

    return dense_disk_map


def file_size_buckets(disk_map: list):
    """Returns buckets of files by size, with *ascending* ids in each bucket"""

    files_by_size = [deque() for _ in range(MAX_FILE_SIZE)]

    for file_id, size, pos in disk_map:
        if file_id is not None:
            files_by_size[size].append((file_id, size, pos))

    return files_by_size


def extract_file(files_by_size: list, size: int):
    return max(
        (bucket[-1] for bucket in files_by_size[: size + 1] if bucket),
        default=None,
    )


def defrag_by_file(disk_map: list):
    # O(n) in the number of files 😎
    disk_map = disk_map.copy()

    files_by_size = file_size_buckets(disk_map)

    defragged = []

    # Plan of attack:
    # Go from left to right and fill empty blocks with the highest id files that fit
    for id, size, pos in disk_map:
        # We have a file, which was not moved during the defrag
        if id is not None:
            # Remove file from bucket (guaranteed to be the first)
            files_by_size[size].popleft()

            # Move file to empty block
            defragged.append((id, size, pos))

            continue

        while True:
            # Iteratively fill the empty block with the highest id file that fits
            if file := extract_file(files_by_size, size):
                file_id, file_size, file_pos = file

                # Remove file from bucket
                files_by_size[file_size].pop()

                # Mark file as moved
                disk_map[file_pos] = (None, file_size, file_pos)

                # Shrink the free space
                size -= file_size

                # Move file to empty block
                defragged.append(file)
            else:
                # No file of the same or smaller size
                defragged.append((None, size, pos))
                break

    return defragged


if __name__ == "__main__":
    with open("input.txt") as f:
        disk_map = parse_disk_map(f.read())

    # Part 1
    print(checksum(defrag_by_block(to_dense(disk_map))))

    # Part 2
    print(checksum(to_dense(defrag_by_file(disk_map))))

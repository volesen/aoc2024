from functools import cache


def parse_input(input):
    vocab, messages = input.split("\n\n")

    vocab = vocab.split(", ")
    messages = messages.split("\n")

    return vocab, messages


def can_construct_message(message: str, vocab: set):
    @cache
    def dfs(position: int):
        if position == len(message):
            return True

        return any(
            dfs(position + len(word))
            for word in vocab
            if message.startswith(word, position)
        )

    return dfs(0)


def count_constructions(message: str, vocab: set):
    @cache
    def dfs(position: int):
        if position == len(message):
            return 1

        return sum(
            dfs(position + len(word))
            for word in vocab
            if message.startswith(word, position)
        )

    return dfs(0)


if __name__ == "__main__":
    with open("input.txt") as f:
        vocab, messages = parse_input(f.read())

    vocab = set(vocab)

    # Part 1
    print(sum(1 for message in messages if can_construct_message(message, vocab)))

    # Part 2
    print(sum(count_constructions(message, vocab) for message in messages))

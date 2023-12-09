from itertools import pairwise


def line_to_sequence(line: str) -> list[int]:
    return [int(number) for number in line.split()]


def get_next_number(sequence: list[int]) -> int:
    difference_sequence = [b - a for a, b in pairwise(sequence)]
    if set(difference_sequence) == {0}:
        return sequence[-1]
    return sequence[-1] + get_next_number(difference_sequence)


def get_previous_number(sequence: list[int]) -> int:
    difference_sequence = [b - a for a, b in pairwise(sequence)]
    if set(difference_sequence) == {0}:
        return sequence[0]
    return sequence[0] - get_previous_number(difference_sequence)


def do_part_one(filename: str) -> int:
    with open(filename, "r") as file:
        return sum(get_next_number(line_to_sequence(line)) for line in file.read().splitlines())


def do_part_two(filename: str) -> int:
    with open(filename, "r") as file:
        return sum(get_previous_number(line_to_sequence(line)) for line in file.read().splitlines())


def main():
    assert do_part_one("input_9_test") == 114
    print(do_part_one("input_9_full"))
    assert do_part_two("input_9_test") == 2
    print(do_part_two("input_9_full"))


if __name__ == "__main__":
    main()

from math import prod
from re import Match, compile

NUMBER_PATTERN = compile(r"\d+")
GEAR_PATTERN = compile(r"\*")


def is_valid_part_number(
    match: Match, row_number: int, all_data: list[str]
) -> bool:
    start_pos = match.start()
    end_pos = match.end()
    first_match_pos = max(start_pos - 1, 0)
    last_match_pos = min(end_pos, len(all_data[row_number]) - 1)
    if start_pos != 0 and all_data[row_number][first_match_pos] != ".":
        return True
    if (
        end_pos != len(all_data[row_number])
        and all_data[row_number][last_match_pos] != "."
    ):
        return True
    if row_number != 0 and not all(
        all_data[row_number - 1][idx] == "."
        for idx in range(first_match_pos, last_match_pos + 1)
    ):
        return True
    if row_number != len(all_data) - 1 and not all(
        all_data[row_number + 1][idx] == "."
        for idx in range(first_match_pos, last_match_pos + 1)
    ):
        return True
    return False


def get_part_number_if_valid(
    match: Match, row_number: int, all_data: list[str]
) -> int:
    if is_valid_part_number(match, row_number, all_data):
        return int(match.group())
    return 0


def get_gear_ratio_if_valid(
    match: Match, row_number: int, all_data: list[str]
) -> int:
    if (
        len(
            surrounding_numbers := get_surrounding_numbers(
                match, row_number, all_data
            )
        )
        == 2
    ):
        return prod(surrounding_numbers)
    return 0


def get_surrounding_numbers(
    match: Match, row_number: int, all_data: list[str]
) -> tuple[int, ...]:
    start_pos = match.start()
    end_pos = match.end()
    surrounding_numbers = []
    if row_number != 0:
        numbers_in_row_above = NUMBER_PATTERN.finditer(
            all_data[row_number - 1]
        )
        for match_ in numbers_in_row_above:
            if (
                set(range(match_.start(), match_.end() + 1)).intersection(
                    range(start_pos, end_pos + 1)
                )
                != set()
            ):
                surrounding_numbers.append(int(match_.group()))

    numbers_in_same_row = NUMBER_PATTERN.finditer(all_data[row_number])
    for match_ in numbers_in_same_row:
        if match_.start() == end_pos or match_.end() == start_pos:
            surrounding_numbers.append(int(match_.group()))

    if row_number != len(all_data) - 1:
        numbers_in_row_below = NUMBER_PATTERN.finditer(
            all_data[row_number + 1]
        )
        for match_ in numbers_in_row_below:
            if (
                set(range(match_.start(), match_.end() + 1)).intersection(
                    range(start_pos, end_pos + 1)
                )
                != set()
            ):
                surrounding_numbers.append(int(match_.group()))

    return tuple(surrounding_numbers)


def do_part_1(filename: str) -> int:
    with open(filename, "r") as file:
        all_data = file.read().splitlines()
    sum = 0
    for idx, line in enumerate(all_data):
        for match_ in NUMBER_PATTERN.finditer(line):
            sum += get_part_number_if_valid(match_, idx, all_data)
    return sum


def do_part_2(filename: str) -> int:
    with open(filename, "r") as file:
        all_data = file.read().splitlines()
    sum = 0
    for idx, line in enumerate(all_data):
        for match_ in GEAR_PATTERN.finditer(line):
            sum += get_gear_ratio_if_valid(match_, idx, all_data)
    return sum


def main():
    assert do_part_1("input_3_test") == 4361
    print(do_part_1("input_3_full"))
    assert do_part_2("input_3_test") == 467835
    print(do_part_2("input_3_full"))


if __name__ == "__main__":
    main()

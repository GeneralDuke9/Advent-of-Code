from collections import defaultdict
import re

PATTERN = re.compile(r"\d+")


def get_game_data_from_line(line: str) -> str:
    return line.split(":")[-1]


def parse_raw_numbers(raw_input: str) -> set[int]:
    return {int(match) for match in PATTERN.findall(raw_input)}


def parse_game_data(game_data: str) -> tuple[set[int], set[int]]:
    winning_numbers_raw, my_numbers_raw = game_data.split("|")
    return parse_raw_numbers(winning_numbers_raw), parse_raw_numbers(my_numbers_raw)


def determine_number_of_matches(line: str) -> int:
    game_data = get_game_data_from_line(line)
    winning_numbers, my_numbers = parse_game_data(game_data)
    return len(winning_numbers.intersection(my_numbers))


def get_value_of_scorecard(line: str) -> int:
    number_of_matches = determine_number_of_matches(line)
    return 2**(number_of_matches-1) if number_of_matches > 0 else 0


def do_part_one(filename: str) -> int:
    with open(filename, "r") as file:
        return sum(get_value_of_scorecard(line) for line in file.read().splitlines())


def do_part_two(filename: str) -> int:
    with open(filename, "r") as file:
        numbers_of_matches = [determine_number_of_matches(line) for line in file.read().splitlines()]
    card_counts = defaultdict(lambda: 1)
    for game_id, number_of_matches in enumerate(numbers_of_matches, start=1):
        _ = card_counts[game_id]
        for i in range(1, number_of_matches+1):
            card_counts[game_id+i] += card_counts[game_id]
    return sum(value for key, value in card_counts.items() if key <= len(numbers_of_matches))


def main():
    assert do_part_one("input_4_test") == 13
    print(do_part_one("input_4_full"))
    assert do_part_two("input_4_test") == 30
    print(do_part_two("input_4_full"))


if __name__ == "__main__":
    main()

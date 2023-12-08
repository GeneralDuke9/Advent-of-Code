import re

PATTERN_NUMERALS = re.compile(r"[1-9]")
PATTERN_ALPHANUMERIC = re.compile(r"(?=([1-9]|one|two|three|four|five|six|seven|eight|nine))")
STRING_TO_INT = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


def convert_digit(match: str) -> int:
    if len(match) == 1:
        return int(match)
    return STRING_TO_INT[match]


def find_first_and_last_digit(line: str) -> tuple[int, int]:
    digits = [convert_digit(match.group(1)) for match in PATTERN_ALPHANUMERIC.finditer(line)]
    return digits[0], digits[-1]


def parse_line(line: str) -> int:
    digits = [int(match) for match in PATTERN_NUMERALS.findall(line)]
    return 10 * digits[0] + digits[-1]


def parse_line_part_two(line: str) -> int:
    first, last = find_first_and_last_digit(line)
    return first * 10 + last


def do_part_one(filename: str) -> int:
    with open(filename, "r") as file:
        return sum(parse_line(line) for line in file.read().splitlines())


def do_part_two(filename: str) -> int:
    with open(filename, "r") as file:
        return sum(parse_line_part_two(line) for line in file.read().splitlines())


def main():
    assert do_part_one("input_1_test") == 142
    print(do_part_one("input_1_full"))
    assert do_part_two("input_1_test_2") == 281
    print(do_part_two("input_1_full"))


if __name__ == "__main__":
    main()

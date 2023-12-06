import re

PATTERN = re.compile(r"(?=([1-9]|one|two|three|four|five|six|seven|eight|nine))")
STRING_TO_INT = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


def convert_digit(match: str) -> int:
    if len(match) == 1:
        return int(match)
    return STRING_TO_INT[match]


def find_first_and_last_digit(line: str) -> tuple[int, int]:
    digits = [convert_digit(match.group(1)) for match in PATTERN.finditer(line)]
    return digits[0], digits[-1]


def parse_line(line: str) -> int:
    first, last = find_first_and_last_digit(line)
    return first * 10 + last


def main():
    sum = 0
    with open("input_1", "r") as file:
        for line in file:
            sum += parse_line(line)
    print(sum)


if __name__ == "__main__":
    main()

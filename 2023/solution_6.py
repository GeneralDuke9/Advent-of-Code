import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Race:
    time: int
    distance: int


def parse_file_part_one(lines: list[str]) -> list[Race]:
    times = lines[0].split(":")[-1].strip().split()
    distances = lines[1].split(":")[-1].strip().split()
    return [Race(time=int(time), distance=int(distance)) for time, distance in zip(times, distances)]


def parse_file_part_two(lines: list[str]) -> Race:
    times = lines[0].split(":")[-1].strip().split()
    distances = lines[1].split(":")[-1].strip().split()
    return Race(time=int("".join(times)), distance=int("".join(distances)))


def number_of_ways_to_win(race: Race) -> int:
    a, b, c = determine_quadratic_coefficients(race)
    solutions = solve_quadratic(a, b, c)
    return (math.ceil(max(solutions)) - 1) - (math.floor(min(solutions)) + 1) + 1


def determine_quadratic_coefficients(race: Race) -> tuple[int, int, int]:
    return -1, race.time, -race.distance


def solve_quadratic(a: int, b: int, c: int) -> tuple[float, float]:
    assert a != 0
    discriminant = b**2 - 4 * a * c
    assert discriminant > 0
    return (-b + math.sqrt(discriminant)) / (2 * a), (-b - math.sqrt(discriminant)) / (2 * a)


def do_part_one(filename: str) -> int:
    with open(filename, "r") as file:
        races = parse_file_part_one(file.read().splitlines())
    return math.prod(number_of_ways_to_win(race) for race in races)


def do_part_two(filename: str) -> int:
    with open(filename, "r") as file:
        race = parse_file_part_two(file.read().splitlines())
    return number_of_ways_to_win(race)


def main():
    assert do_part_one("input_6_test") == 288
    print(do_part_one("input_6_full"))
    assert do_part_two("input_6_test") == 71503
    print(do_part_two("input_6_full"))


if __name__ == "__main__":
    main()

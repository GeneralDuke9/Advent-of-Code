from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GameInfo:
    red: int
    green: int
    blue: int

    @classmethod
    def from_attempt(cls, attempt: str):
        red = green = blue = 0
        for cube in attempt.split(", "):
            count, color = cube.split(" ")
            match color:
                case "red":
                    red = int(count)
                case "green":
                    green = int(count)
                case "blue":
                    blue = int(count)
        return cls(red, green, blue)

    def is_valid(self) -> bool:
        if self.red > 12:
            return False
        if self.green > 13:
            return False
        if self.blue > 14:
            return False
        return True


def determine_power(game_infos: list[GameInfo]) -> int:
    max_red = max(game_info.red for game_info in game_infos if game_info.red != 0)
    max_green = max(game_info.green for game_info in game_infos if game_info.green != 0)
    max_blue = max(game_info.blue for game_info in game_infos if game_info.blue != 0)
    return max_red * max_green * max_blue


def parse_game_info(raw: str) -> list[GameInfo]:
    return [GameInfo.from_attempt(attempt) for attempt in raw.split("; ")]


def parse_game_input(line: str) -> tuple[int, list[GameInfo]]:
    game_id_raw, game_info_raw = line.split(": ")
    game_id = int(game_id_raw.split(" ")[-1])
    game_infos = parse_game_info(game_info_raw)
    return game_id, game_infos


def parse_line(line: str) -> int:
    game_id, game_infos = parse_game_input(line)
    if all(game_info.is_valid() for game_info in game_infos):
        return game_id
    return 0


def parse_line_part_two(line: str) -> int:
    _, game_infos = parse_game_input(line)
    return determine_power(game_infos)


def do_part_one(filename: str) -> int:
    with open(filename, "r") as file:
        return sum(parse_line(line) for line in file.read().splitlines())


def do_part_two(filename: str) -> int:
    with open(filename, "r") as file:
        return sum(parse_line_part_two(line) for line in file.read().splitlines())


def main():
    assert do_part_one("input_2_test") == 8
    print(do_part_one("input_2_full"))
    assert do_part_two("input_2_test") == 2286
    print(do_part_two("input_2_full"))


if __name__ == "__main__":
    main()

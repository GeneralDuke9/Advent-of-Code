import math
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Orientation(Enum):
    CLOCKWISE = "clockwise"
    COUNTERCLOCKWISE = "counterclockwise"


@dataclass(slots=True, frozen=True)
class Position:
    x: int
    y: int


class PipeMap:
    full_map: list[str]
    start_position: Position
    empty_spaces: set[Position]
    max_x: int
    max_y: int
    loop: tuple[Position, ...]
    loop_positions: set[Position]

    def __init__(self, lines: list[str]):
        self.full_map = lines
        self.max_x = len(lines[0]) - 1
        self.max_y = len(lines) - 1
        self.empty_spaces = set()
        for idx, line in enumerate(lines):
            for jdx, char in enumerate(line):
                if char == "S":
                    self.start_position = Position(jdx, idx)
                elif char == ".":
                    self.empty_spaces.add(Position(jdx, idx))

    @property
    def loop_length(self) -> int:
        return len(self.loop)

    def follow_loop(self):
        this_position = self.start_position
        direction = self._determine_initial_direction(this_position)
        loop_points = []
        while True:
            assert direction is not None
            loop_points.append(this_position)
            this_position = determine_next_position(this_position, direction)
            direction = self._determine_new_direction(this_position, direction)
            if direction is None:
                self.loop = tuple(loop_points)
                self.loop_positions = set(loop_points)
                return

    def simplify(self):
        simplified_map = []
        for idx, row in enumerate(self.full_map):
            simplified_row = []
            for jdx, char in enumerate(row):
                if (this_position := Position(jdx, idx)) in self.loop_positions:
                    simplified_row.append(char)
                else:
                    self.empty_spaces.add(this_position)
                    simplified_row.append(".")
            simplified_map.append("".join(simplified_row))

        self.full_map = simplified_map

    def size_of_contained_area(self) -> int:
        orientation = self._get_orientation_of_loop()
        inside_spaces = set()
        outside_spaces = set()
        for empty_space in self.empty_spaces:
            is_on_inside_of_loop = self._is_on_inside_of_loop(empty_space, orientation)
            if is_on_inside_of_loop is True:
                inside_spaces.add(empty_space)
            elif is_on_inside_of_loop is False:
                outside_spaces.add(empty_space)
            else:
                assert is_on_inside_of_loop is None

        while uncategorised_spaces := (self.empty_spaces - inside_spaces - outside_spaces):
            for empty_space in uncategorised_spaces:
                if touches(empty_space, inside_spaces):
                    inside_spaces.add(empty_space)
                elif touches(empty_space, outside_spaces):
                    outside_spaces.add(empty_space)

        return len(inside_spaces)

    def _get_next_in_loop(self, position: Position):
        try:
            return self.loop[self.loop.index(position) + 1]
        except IndexError:
            assert self.loop.index(position) == len(self.loop) - 1
            return self.loop[0]

    def _get_previous_in_loop(self, position: Position):
        return self.loop[self.loop.index(position) - 1]

    def _is_on_inside_of_loop(self, space: Position, orientation: Orientation) -> bool | None:
        if (position_to_the_right := Position(space.x + 1, space.y)) in self.loop_positions:
            previous_in_loop = self._get_previous_in_loop(position_to_the_right)
            next_in_loop = self._get_next_in_loop(position_to_the_right)
            previous_direction = get_direction(previous_in_loop, position_to_the_right)
            next_direction = get_direction(position_to_the_right, next_in_loop)
            if Direction.DOWN in (previous_direction, next_direction):
                return orientation is Orientation.CLOCKWISE
            elif Direction.UP in (previous_direction, next_direction):
                return orientation is Orientation.COUNTERCLOCKWISE

        if (position_below := Position(space.x, space.y + 1)) in self.loop_positions:
            previous_in_loop = self._get_previous_in_loop(position_below)
            next_in_loop = self._get_next_in_loop(position_below)
            previous_direction = get_direction(previous_in_loop, position_below)
            next_direction = get_direction(position_below, next_in_loop)
            if Direction.LEFT in (previous_direction, next_direction):
                return orientation is Orientation.CLOCKWISE
            elif Direction.RIGHT in (previous_direction, next_direction):
                return orientation is Orientation.COUNTERCLOCKWISE

        if (position_to_the_left := Position(space.x - 1, space.y)) in self.loop_positions:
            previous_in_loop = self._get_previous_in_loop(position_to_the_left)
            next_in_loop = self._get_next_in_loop(position_to_the_left)
            previous_direction = get_direction(previous_in_loop, position_to_the_left)
            next_direction = get_direction(position_to_the_left, next_in_loop)
            if Direction.UP in (previous_direction, next_direction):
                return orientation is Orientation.CLOCKWISE
            elif Direction.DOWN in (previous_direction, next_direction):
                return orientation is Orientation.COUNTERCLOCKWISE

        if (position_above := Position(space.x, space.y - 1)) in self.loop_positions:
            previous_in_loop = self._get_previous_in_loop(position_above)
            next_in_loop = self._get_next_in_loop(position_above)
            previous_direction = get_direction(previous_in_loop, position_above)
            next_direction = get_direction(position_above, next_in_loop)
            if Direction.RIGHT in (previous_direction, next_direction):
                return orientation is Orientation.CLOCKWISE
            elif Direction.LEFT in (previous_direction, next_direction):
                return orientation is Orientation.COUNTERCLOCKWISE

        return None

    def _get_orientation_of_loop(self) -> Orientation:
        top_left_point_on_loop = self._find_top_left_point_on_loop()
        next_point_in_loop = self.loop[self.loop.index(top_left_point_on_loop) + 1]
        if top_left_point_on_loop.y == next_point_in_loop.y and top_left_point_on_loop.x == next_point_in_loop.x - 1:
            return Orientation.CLOCKWISE
        elif top_left_point_on_loop.x == next_point_in_loop.x and top_left_point_on_loop.y == next_point_in_loop.y - 1:
            return Orientation.COUNTERCLOCKWISE
        raise ValueError("Cannot determine orientation")

    def _find_top_left_point_on_loop(self) -> Position:
        min_y_of_loop = min(point.y for point in self.loop)
        top_most_points = [point for point in self.loop if point.y == min_y_of_loop]
        min_x_of_top_most_points = min(point.x for point in top_most_points)
        for point in top_most_points:
            if point.x == min_x_of_top_most_points:
                return point
        raise ValueError("No top-left point")

    def _determine_initial_direction(self, position: Position) -> Direction:
        if position.x != self.max_x:
            to_the_right = self._get_pipe_configuration(Position(position.x + 1, position.y))
            if to_the_right in ("J", "7", "-"):
                return Direction.RIGHT
        if position.x != 0:
            to_the_left = self._get_pipe_configuration(Position(position.x - 1, position.y))
            if to_the_left in ("F", "L", "-"):
                return Direction.LEFT
        if position.y != self.max_y:
            downwards = self._get_pipe_configuration(Position(position.x, position.y + 1))
            if downwards in ("L", "J", "|"):
                return Direction.DOWN
        if position.y != 0:
            upwards = self._get_pipe_configuration(Position(position.x, position.y - 1))
            if upwards in ("7", "F", "|"):
                return Direction.UP
        raise ValueError(f"I'm stuck at {position}!")

    def _determine_new_direction(self, position: Position, previous_direction: Direction) -> Direction | None:
        pipe_configuration = self._get_pipe_configuration(position)
        if pipe_configuration in ("-", "|"):
            return previous_direction
        elif pipe_configuration == "J":
            if previous_direction is Direction.RIGHT:
                return Direction.UP
            elif previous_direction is Direction.DOWN:
                return Direction.LEFT
            raise ValueError(f"Entered a `J` from the {previous_direction}")
        elif pipe_configuration == "F":
            if previous_direction is Direction.LEFT:
                return Direction.DOWN
            elif previous_direction is Direction.UP:
                return Direction.RIGHT
            raise ValueError(f"Entered a `F` from the {previous_direction}")
        elif pipe_configuration == "7":
            if previous_direction is Direction.RIGHT:
                return Direction.DOWN
            elif previous_direction is Direction.UP:
                return Direction.LEFT
            raise ValueError(f"Entered a `7` from the {previous_direction}")
        elif pipe_configuration == "L":
            if previous_direction is Direction.LEFT:
                return Direction.UP
            elif previous_direction is Direction.DOWN:
                return Direction.RIGHT
            raise ValueError(f"Entered a `L` from the {previous_direction}")
        elif pipe_configuration == "S":
            return None
        raise ValueError(f"Unexpected pipe: {pipe_configuration} at {position} with direction {previous_direction}")

    def _get_pipe_configuration(self, position: Position) -> str:
        return self.full_map[position.y][position.x]


def get_direction(first_position: Position, second_position: Position):
    if first_position.x == second_position.x:
        assert first_position.y != second_position.y
        return Direction.UP if first_position.y > second_position.y else Direction.DOWN
    assert first_position.y == second_position.y
    return Direction.LEFT if first_position.x > second_position.x else Direction.RIGHT


def determine_next_position(position: Position, direction: Direction) -> Position:
    match direction:
        case Direction.UP:
            return Position(position.x, position.y - 1)
        case Direction.DOWN:
            return Position(position.x, position.y + 1)
        case Direction.RIGHT:
            return Position(position.x + 1, position.y)
        case Direction.LEFT:
            return Position(position.x - 1, position.y)
    raise ValueError(f"Expected a valid direction, got {direction}")


def touches(this_position: Position, positions: set[Position]) -> bool:
    for position in positions:
        if (
            this_position.x == position.x
            and abs(this_position.y - position.y) == 1
            or this_position.y == position.y
            and abs(this_position.x - position.x) == 1
        ):
            return True
    return False


def do_part_one(filename: str) -> int:
    with open(filename, "r") as file:
        pipe_map = PipeMap(file.read().splitlines())
    pipe_map.follow_loop()
    return math.floor(pipe_map.loop_length / 2)


def do_part_two(filename: str) -> int:
    with open(filename, "r") as file:
        pipe_map = PipeMap(file.read().splitlines())
    pipe_map.follow_loop()
    pipe_map.simplify()
    return pipe_map.size_of_contained_area()


def main():
    assert do_part_one("input_10_test") == 4
    assert do_part_one("input_10_test_2") == 8
    print(do_part_one("input_10_full"))
    assert do_part_two("input_10_test_3") == 4
    assert do_part_two("input_10_test_4") == 4
    assert do_part_two("input_10_test_5") == 8
    assert do_part_two("input_10_test_6") == 10
    print(do_part_two("input_10_full"))


if __name__ == "__main__":
    main()

import math
import re
from itertools import cycle
from typing import Final

PATTERN = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")
START_NODE: Final[str] = "AAA"
END_NODE: Final[str] = "ZZZ"


class MapTraverser:
    location_maps: dict[str, tuple[str, str]]
    directions: str
    number_of_steps: int

    def __init__(self, lines: list[str]):
        self.location_maps = dict()
        line_iterator = iter(lines)
        self.directions = next(line_iterator)
        next(line_iterator)
        for line in line_iterator:
            key, value = parse_line(line)
            self.location_maps[key] = value

    def traverse(self):
        self.number_of_steps = 1
        self._do_traverse(START_NODE, {END_NODE})

    def _do_traverse(self, start_node: str, end_nodes: set[str]):
        this_node = start_node
        for direction in cycle(self.directions):
            if direction == "L":
                this_node = self.location_maps[this_node][0]
            elif direction == "R":
                this_node = self.location_maps[this_node][1]
            else:
                raise ValueError(f"Expected direction, got {direction}")

            if this_node in end_nodes:
                return
            self.number_of_steps += 1

    def traverse_part_two(self):
        numbers_of_steps = []
        start_nodes = [node for node in self.location_maps.keys() if node[-1] == "A"]
        end_nodes = {node for node in self.location_maps.keys() if node[-1] == "Z"}
        for start_node in start_nodes:
            self.number_of_steps = 1
            self._do_traverse(start_node, end_nodes)
            numbers_of_steps.append(self.number_of_steps)
        self.number_of_steps = math.lcm(*numbers_of_steps)


def parse_line(line: str) -> tuple[str, tuple[str, str]]:
    matches = PATTERN.search(line)
    assert matches is not None
    return matches.group(1), (matches.group(2), matches.group(3))


def do_part_one(filename: str) -> int:
    with open(filename, "r") as file:
        map_traverser = MapTraverser(file.read().splitlines())
    map_traverser.traverse()
    return map_traverser.number_of_steps


def do_part_two(filename: str) -> int:
    with open(filename, "r") as file:
        map_traverser = MapTraverser(file.read().splitlines())
    map_traverser.traverse_part_two()
    return map_traverser.number_of_steps


def main():
    assert do_part_one("input_8_test") == 2
    assert do_part_one("input_8_test_2") == 6
    print(do_part_one("input_8_full"))
    assert do_part_two("input_8_test_3") == 6
    print(do_part_two("input_8_full"))


if __name__ == "__main__":
    main()

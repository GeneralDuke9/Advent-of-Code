from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Galaxy:
    row: int
    col: int

    def manhattan_distance(self, other: Galaxy) -> int:
        return abs(self.row - other.row) + (abs(self.col - other.col))


@dataclass(slots=True, frozen=True)
class Universe:
    galaxies: list[Galaxy]
    dimensions: tuple[int, int]

    @classmethod
    def from_file(cls, lines: list[str]):
        galaxies = [Galaxy(row, col) for row, line in enumerate(lines) for col, char in enumerate(line) if char == "#"]
        dimensions = len(lines), len(lines[0])
        return cls(galaxies, dimensions)

    def expand(self, factor: int):
        used_rows = {galaxy.row for galaxy in self.galaxies}
        used_cols = {galaxy.col for galaxy in self.galaxies}
        n_rows, n_cols = self.dimensions
        empty_rows = set(range(n_rows)) - used_rows
        empty_cols = set(range(n_cols)) - used_cols
        for galaxy in self.galaxies:
            empty_rows_above = len([row for row in empty_rows if row < galaxy.row])
            empty_cols_to_the_left = len([col for col in empty_cols if col < galaxy.col])
            galaxy.row += empty_rows_above * factor
            galaxy.col += empty_cols_to_the_left * factor

    def shortest_path_between_galaxies(self):
        sum_of_shortest_paths = 0
        for idx, galaxy in enumerate(self.galaxies):
            for j in range(idx + 1, len(self.galaxies)):
                sum_of_shortest_paths += galaxy.manhattan_distance(self.galaxies[j])
        return sum_of_shortest_paths


def do_part_one(filename: str) -> int:
    with open(filename, "r") as file:
        universe_map = Universe.from_file(file.read().splitlines())
    universe_map.expand(factor=1)
    return universe_map.shortest_path_between_galaxies()


def do_part_two(filename: str, factor: int) -> int:
    with open(filename, "r") as file:
        universe_map = Universe.from_file(file.read().splitlines())
    universe_map.expand(factor)
    return universe_map.shortest_path_between_galaxies()


def main():
    assert do_part_one("input_11_test") == 374, do_part_one("input_11_test")
    print(do_part_one("input_11_full"))
    assert do_part_two("input_11_test", factor=9) == 1030
    assert do_part_two("input_11_test", factor=99) == 8410
    print(do_part_two("input_11_full", factor=999999))


if __name__ == "__main__":
    main()

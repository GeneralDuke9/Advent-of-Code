import itertools
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True, slots=True)
class SeedRange:
    start: int
    length: int


@dataclass(frozen=True, slots=True)
class ItemTypeMap:
    destination_range_start: int
    source_range_start: int
    range_length: int


@dataclass(slots=True)
class ItemTypeMapper:
    item_type_maps: list[ItemTypeMap]
    item_type_map_by_source_range_start: dict[int, ItemTypeMap] | None = None
    item_type_map_by_destination_range_start: dict[int, ItemTypeMap] | None = None

    @classmethod
    def from_lines(cls, line_iterator: Iterator[str]):
        item_type_maps = []
        try:
            while (line := next(line_iterator)) != "":
                destination_range_start, source_range_start, range_length = [int(entry) for entry in line.split(" ")]
                item_type_maps.append(ItemTypeMap(destination_range_start, source_range_start, range_length))
            return cls(item_type_maps)
        except StopIteration:
            return cls(item_type_maps)

    @property
    def source_range_starts(self) -> list[int]:
        return sorted((item_type_map.source_range_start for item_type_map in self.item_type_maps), reverse=True)

    def get_item_type_map(self, source_range_start: int) -> ItemTypeMap:
        if self.item_type_map_by_source_range_start is None:
            self.item_type_map_by_source_range_start = {
                item_type_map.source_range_start: item_type_map for item_type_map in self.item_type_maps
            }
        return self.item_type_map_by_source_range_start[source_range_start]

    def get_item_type_map_from_destination_range_start(self, destination_range_start: int) -> ItemTypeMap:
        if self.item_type_map_by_destination_range_start is None:
            self.item_type_map_by_destination_range_start = {
                item_type_map.destination_range_start: item_type_map for item_type_map in self.item_type_maps
            }
        return self.item_type_map_by_destination_range_start[destination_range_start]

    def map(self, value: int) -> int:
        if self.should_be_mapped(value):
            return self.mapped_value(value)
        return value

    def map_and_get_range(self, value: int, current_range: int | None) -> tuple[int, int]:
        mapped_value = self.map(value)
        source_range_start = find_closest_number_smaller_or_equals(value, self.source_range_starts)
        if source_range_start is None:
            this_range = min(self.source_range_starts) - value
            return mapped_value, safe_min(this_range, current_range)
        item_type_map = self.get_item_type_map(source_range_start)
        if value - item_type_map.source_range_start < item_type_map.range_length:
            this_range = item_type_map.source_range_start + item_type_map.range_length - value
            return mapped_value, safe_min(this_range, current_range)

        next_source_range_start = find_closest_number_larger(value, self.source_range_starts)
        if next_source_range_start is None:
            assert current_range is not None
            return mapped_value, current_range
        next_item_type_map = self.get_item_type_map(next_source_range_start)
        this_range = next_item_type_map.source_range_start - value
        return mapped_value, safe_min(this_range, current_range)

    def should_be_mapped(self, value: int) -> bool:
        source_range_start = find_closest_number_smaller_or_equals(value, self.source_range_starts)
        if source_range_start is None:
            return False
        item_type_map = self.get_item_type_map(source_range_start)
        assert source_range_start == item_type_map.source_range_start
        return value - item_type_map.source_range_start < item_type_map.range_length

    def mapped_value(self, value: int) -> int:
        source_range_start = find_closest_number_smaller_or_equals(value, self.source_range_starts)
        assert source_range_start is not None
        item_type_map = self.get_item_type_map(source_range_start)
        return item_type_map.destination_range_start + (value - item_type_map.source_range_start)


class AlmanacDataABC(ABC):
    seeds: list
    seed_to_soil: ItemTypeMapper
    soil_to_fertilizer: ItemTypeMapper
    fertilizer_to_water: ItemTypeMapper
    water_to_light: ItemTypeMapper
    light_to_temperature: ItemTypeMapper
    temperature_to_humidity: ItemTypeMapper
    humidity_to_location: ItemTypeMapper

    def __init__(self, lines: list[str]):
        line_iterator = iter(lines)
        self.seeds = self.parse_seeds(next(line_iterator))
        next(line_iterator)
        self.seed_to_soil = self.parse_block(line_iterator)
        self.soil_to_fertilizer = self.parse_block(line_iterator)
        self.fertilizer_to_water = self.parse_block(line_iterator)
        self.water_to_light = self.parse_block(line_iterator)
        self.light_to_temperature = self.parse_block(line_iterator)
        self.temperature_to_humidity = self.parse_block(line_iterator)
        self.humidity_to_location = self.parse_block(line_iterator)

    @staticmethod
    @abstractmethod
    def parse_seeds(line: str) -> list:
        pass

    @staticmethod
    def parse_block(line_iterator: Iterator[str]) -> ItemTypeMapper:
        next(line_iterator)
        return ItemTypeMapper.from_lines(line_iterator)


class AlmanacDataPartOne(AlmanacDataABC):
    @staticmethod
    def parse_seeds(line: str) -> list[int]:
        return [int(number) for number in line.split(":")[-1].strip().split(" ")]

    def get_lowest_location_number_for_seeds(self) -> int:
        return min(self.get_location_for_seed(seed) for seed in self.seeds)

    def get_location_for_seed(self, seed: int) -> int:
        return self.find_location("seed", seed)

    def find_location(self, item_type: str, value: int) -> int:
        match item_type:
            case "seed":
                return self.find_location("soil", self.seed_to_soil.map(value))
            case "soil":
                return self.find_location("fertilizer", self.soil_to_fertilizer.map(value))
            case "fertilizer":
                return self.find_location("water", self.fertilizer_to_water.map(value))
            case "water":
                return self.find_location("light", self.water_to_light.map(value))
            case "light":
                return self.find_location("temperature", self.light_to_temperature.map(value))
            case "temperature":
                return self.find_location("humidity", self.temperature_to_humidity.map(value))
            case "humidity":
                return self.humidity_to_location.map(value)
        raise ValueError(f"{item_type} not a valid item type")


class AlmanacDataPartTwo(AlmanacDataABC):
    seed_range_by_seed_range_start: dict[int, SeedRange] | None = None

    @staticmethod
    def parse_seeds(line: str) -> list[SeedRange]:
        numbers = [int(number) for number in line.split(":")[-1].strip().split(" ")]
        return [SeedRange(start=start, length=length) for start, length in itertools.batched(numbers, 2)]

    @property
    def seed_range_starts(self) -> list[int]:
        return sorted([seed_range.start for seed_range in self.seeds], reverse=True)

    @property
    def max_seed_value(self) -> int:
        return max(seed_range.start + seed_range.length - 1 for seed_range in self.seeds)

    def get_seed_range(self, seed_range_start: int) -> SeedRange:
        if self.seed_range_by_seed_range_start is None:
            self.seed_range_by_seed_range_start = {seed_range.start: seed_range for seed_range in self.seeds}
        return self.seed_range_by_seed_range_start[seed_range_start]

    def is_valid_seed_number(self, seed_number: int) -> bool:
        seed_range_start = find_closest_number_smaller_or_equals(seed_number, self.seed_range_starts)
        if seed_range_start is None:
            return False
        seed_range = self.get_seed_range(seed_range_start)
        assert seed_range.start == seed_range_start
        return seed_number - seed_range.start < seed_range.length

    def find_current_seed_range(self, seed: int) -> int:
        seed_range_start = find_closest_number_smaller_or_equals(seed, self.seed_range_starts)
        assert seed_range_start is not None
        seed_range = self.get_seed_range(seed_range_start)
        return seed_range.start + seed_range.length - seed

    def get_lowest_location_number_for_seeds(self) -> int:
        locations = []
        seed = min(self.seed_range_starts)
        while seed <= self.max_seed_value:
            current_seed_range = self.find_current_seed_range(seed)
            location, current_range = self.find_location_and_current_range("seed", seed, current_seed_range)
            locations.append(location)
            seed += current_range
            if not self.is_valid_seed_number(seed):
                next_seed = find_closest_number_larger(seed, self.seed_range_starts)
                if next_seed is None:
                    return min(locations)
                seed = next_seed
        return min(locations)

    def find_location_and_current_range(self, item_type: str, value: int, current_range: int) -> tuple[int, int]:
        match item_type:
            case "seed":
                return self.find_location_and_current_range(
                    "soil", *self.seed_to_soil.map_and_get_range(value, current_range)
                )
            case "soil":
                return self.find_location_and_current_range(
                    "fertilizer", *self.soil_to_fertilizer.map_and_get_range(value, current_range)
                )
            case "fertilizer":
                return self.find_location_and_current_range(
                    "water", *self.fertilizer_to_water.map_and_get_range(value, current_range)
                )
            case "water":
                return self.find_location_and_current_range(
                    "light", *self.water_to_light.map_and_get_range(value, current_range)
                )
            case "light":
                return self.find_location_and_current_range(
                    "temperature", *self.light_to_temperature.map_and_get_range(value, current_range)
                )
            case "temperature":
                return self.find_location_and_current_range(
                    "humidity", *self.temperature_to_humidity.map_and_get_range(value, current_range)
                )
            case "humidity":
                return self.humidity_to_location.map_and_get_range(value, current_range)
        raise ValueError(f"{item_type} not a valid item type")


def find_closest_number_smaller_or_equals(value_to_match: int, available_values: list[int]) -> int | None:
    for value in available_values:
        if value > value_to_match:
            continue
        return value
    return None


def find_closest_number_larger(value_to_match: int, available_values: list[int]) -> int | None:
    for value in sorted(available_values):
        if value <= value_to_match:
            continue
        return value
    return None


def safe_min(a: int | None, b: int | None) -> int:
    if a is None and b is None:
        raise ValueError("Both values are None")
    assert a is not None
    assert b is not None
    if a is None:
        return b
    if b is None:
        return a
    return min(a, b)


def do_part_one(filename: str) -> int:
    with open(filename, "r") as file:
        data = AlmanacDataPartOne(file.read().splitlines())
    return data.get_lowest_location_number_for_seeds()


def do_part_two(filename: str) -> int:
    with open(filename, "r") as file:
        data = AlmanacDataPartTwo(file.read().splitlines())
    return data.get_lowest_location_number_for_seeds()


def main():
    assert do_part_one("input_5_test") == 35
    print(do_part_one("input_5_full"))
    assert do_part_two("input_5_test") == 46
    print(do_part_two("input_5_full"))


if __name__ == "__main__":
    main()

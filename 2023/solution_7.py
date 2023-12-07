from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Self, Tuple


class HandType(Enum):
    FIVE_OF_A_KIND = "Five of a kind"
    FOUR_OF_A_KIND = "Four of a kind"
    FULL_HOUSE = "Full house"
    THREE_OF_A_KIND = "Three of a kind"
    TWO_PAIR = "Two pair"
    ONE_PAIR = "One pair"
    HIGH_CARD = "High card"

    def __lt__(self, other: Self) -> bool:
        return HandTypeOrder.index(self) > HandTypeOrder.index(other)


CardOrderPartOne = ("A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2")
CardOrderPartTwo = ("A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J")
HandTypeOrder = (
    HandType.FIVE_OF_A_KIND,
    HandType.FOUR_OF_A_KIND,
    HandType.FULL_HOUSE,
    HandType.THREE_OF_A_KIND,
    HandType.TWO_PAIR,
    HandType.ONE_PAIR,
    HandType.HIGH_CARD,
)
Cards = Tuple[str, ...]


@dataclass(slots=True)
class HandABC(ABC):
    cards: Cards
    bid: int
    type: HandType | None = None

    @classmethod
    def from_line(cls, line: str):
        cards, bid = line.split()
        return cls(cards=tuple(cards), bid=int(bid))

    def __post_init__(self):
        assert len(self.cards) == 5, "Expected hand of length 5"
        self.type = self.determine_hand_type(self.cards)
        assert self.type is not None

    def __lt__(self, other: Self) -> bool:
        assert self.type is not None
        assert other.type is not None
        if self.type is other.type:
            for this_card, other_card in zip(self.cards, other.cards):
                if this_card != other_card:
                    return self.compare_cards(this_card, other_card)
            return False
        return self.type < other.type

    @staticmethod
    @abstractmethod
    def determine_hand_type(cards: Cards) -> HandType:
        pass

    @staticmethod
    @abstractmethod
    def compare_cards(this: str, other: str) -> bool:
        pass


class HandPartOne(HandABC):
    @staticmethod
    def determine_hand_type(cards: Cards) -> HandType:
        return get_hand_type_from_cards(cards)

    @staticmethod
    def compare_cards(this: str, other: str) -> bool:
        return CardOrderPartOne.index(this) > CardOrderPartOne.index(other)


class HandPartTwo(HandABC):
    @staticmethod
    def determine_hand_type(cards: Cards) -> HandType:
        original_hand_type = get_hand_type_from_cards(cards)
        card_counter = Counter(cards)
        number_of_jokers = card_counter.get("J")
        if number_of_jokers == 0:
            return original_hand_type
        if number_of_jokers == 1:
            match original_hand_type:
                case HandType.HIGH_CARD:
                    return HandType.ONE_PAIR
                case HandType.ONE_PAIR:
                    return HandType.THREE_OF_A_KIND
                case HandType.TWO_PAIR:
                    return HandType.FULL_HOUSE
                case HandType.THREE_OF_A_KIND:
                    return HandType.FOUR_OF_A_KIND
                case HandType.FULL_HOUSE:
                    return HandType.FOUR_OF_A_KIND
                case HandType.FOUR_OF_A_KIND:
                    return HandType.FIVE_OF_A_KIND
            raise ValueError(f"Didn't expect a {original_hand_type} with 1 joker")
        elif number_of_jokers == 2:
            match original_hand_type:
                case HandType.ONE_PAIR:
                    return HandType.THREE_OF_A_KIND
                case HandType.TWO_PAIR:
                    return HandType.FOUR_OF_A_KIND
                case HandType.FULL_HOUSE:
                    return HandType.FIVE_OF_A_KIND
            raise ValueError(f"Didn't expect a {original_hand_type} with 2 jokers")
        elif number_of_jokers == 3:
            match original_hand_type:
                case HandType.THREE_OF_A_KIND:
                    return HandType.FOUR_OF_A_KIND
                case HandType.FULL_HOUSE:
                    return HandType.FIVE_OF_A_KIND
            raise ValueError(f"Didn't expect a {original_hand_type} with 3 jokers")
        elif number_of_jokers == 4:
            if original_hand_type is HandType.FOUR_OF_A_KIND:
                return HandType.FIVE_OF_A_KIND
            raise ValueError(f"Didn't expect a {original_hand_type} with 4 jokers")
        else:
            return original_hand_type

    @staticmethod
    def compare_cards(this: str, other: str) -> bool:
        return CardOrderPartTwo.index(this) > CardOrderPartTwo.index(other)


def get_hand_type_from_cards(cards: Cards) -> HandType:
    card_counts = tuple(sorted(Counter(cards).values(), reverse=True))
    if 5 in card_counts:
        return HandType.FIVE_OF_A_KIND
    if 4 in card_counts:
        return HandType.FOUR_OF_A_KIND
    if card_counts == (3, 2):
        return HandType.FULL_HOUSE
    if 3 in card_counts:
        return HandType.THREE_OF_A_KIND
    if card_counts == (2, 2, 1):
        return HandType.TWO_PAIR
    if 2 in card_counts:
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD


def do_part_one(filename: str) -> int:
    with open(filename, "r") as file:
        hands = [HandPartOne.from_line(line) for line in file.read().splitlines()]
    sorted_hands = sorted(hands)
    return sum(rank * hand.bid for rank, hand in enumerate(sorted_hands, start=1))


def do_part_two(filename: str) -> int:
    with open(filename, "r") as file:
        hands = [HandPartTwo.from_line(line) for line in file.read().splitlines()]
    sorted_hands = sorted(hands)
    return sum(rank * hand.bid for rank, hand in enumerate(sorted_hands, start=1))


def main():
    assert do_part_one("input_7_test") == 6440
    print(do_part_one("input_7_full"))
    assert do_part_two("input_7_test") == 5905
    print(do_part_two("input_7_full"))


if __name__ == "__main__":
    main()

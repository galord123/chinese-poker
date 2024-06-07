from copy import deepcopy
from enum import Enum, IntEnum
from typing import List
from game_card import Card


class HandValue(IntEnum):
    ILLEGAL = 0,
    HIGHEST_CARD = 1,
    PAIR = 2,
    TWO_PAIR = 3,
    THREE_OF_A_KIND = 4,
    STRAIGHT = 5,
    FLUSH = 6,
    FULL_HOUSE = 7,
    FOUR_OF_A_KIND = 8,
    STRAIGHT_FLUSH = 9,
    ROYAL_STRAIGHT_FLUSH = 10


def calculate_two_pairs(cards: List[Card]) -> tuple:
    values = [card.number for card in cards]

    pairs = sorted((x for x in values if values.count(x) == 2), reverse=True)
    return pairs


def calculate_full_house(cards: List[Card]) -> tuple:
    values = [card.number for card in cards]

    three = max(x for x in values if values.count(x) == 3)
    pair = max(x for x in values if values.count(x) == 2)
    if pair == 1:
        pair = 14

    if three == 1:
        three = 14
    return three, pair


def calculate_pair(cards: List[Card]) -> int:
    values = [card.number for card in cards]
    pair = max(x for x in values if values.count(x) == 2)
    if pair == 1:
        pair = 14
    return pair


def check_straight(values: List[int]) -> bool:
    is_straight = values == list(range(values[0], values[0] - 5, -1))
    if not is_straight:
        if values[-1] == 1:
            temp_values = deepcopy(values)
            temp_values[-1] = 14
            temp_values = sorted(temp_values, reverse=True)
            is_straight = temp_values == list(
                range(temp_values[0], temp_values[0] - 5, -1))
    return is_straight


class Hand:
    def __init__(self):
        self.cards: List[Card] = []

    @staticmethod
    def kind_count(values, n):
        return any(values.count(x) == n for x in values)

    def potential_strength(self, card: Card) -> HandValue:
        self.cards.append(card)
        hand_strength = self.calculate_hand_value()
        self.cards.remove(card)
        return hand_strength

    def calculate_hand_value(self) -> HandValue:
        if len(self.cards) == 0:
            return HandValue.ILLEGAL

        suits = [card.suit for card in self.cards]
        sorted_cards = sorted(
            self.cards, key=lambda card: card.number, reverse=True)
        values = [card.number for card in sorted_cards]
        is_flush = len(set(suits)) == 1
        is_straight = check_straight(values)

        if is_flush and is_straight:
            # TODO: add a check for royal straight flush
            return HandValue.STRAIGHT_FLUSH

        if is_flush:
            return HandValue.FLUSH

        if is_straight:
            return HandValue.STRAIGHT

        if len(set(x for x in values if values.count(x) == 2)) == 2:
            return HandValue.TWO_PAIR

        if self.kind_count(values, 4):
            return HandValue.FOUR_OF_A_KIND

        if self.kind_count(values, 3) and self.kind_count(values, 2):
            three = max(x for x in values if values.count(x) == 3)
            pair = max(x for x in values if values.count(x) == 2)
            return HandValue.FULL_HOUSE

        if self.kind_count(values, 3):
            return HandValue.THREE_OF_A_KIND

        if self.kind_count(values, 2):
            return HandValue.PAIR

        return HandValue.HIGHEST_CARD

    def __repr__(self) -> str:
        return " ".join([str(card) for card in self.cards])

    def get_highest_card(self) -> Card:
        for card in self.cards:
            if card.number == 1:
                highest_card = deepcopy(card)
                highest_card .number = 14
                return highest_card
        return max(self.cards, key=lambda x: x.number)

    def __gt__(self, other: "Hand"):
        hand_value = self.calculate_hand_value()
        other_hand_value = other.calculate_hand_value()

        if len(self.cards) == 0 or len(other.cards) == 0:
            return False

        if hand_value != other_hand_value:
            return hand_value.value > other_hand_value.value
        else:
            if hand_value == HandValue.TWO_PAIR:
                pairs = calculate_two_pairs(self.cards)
                other_pairs = calculate_two_pairs(other.cards)
                if pairs[0] > other_pairs[0]:
                    return True

                if pairs[1] > other_pairs[1]:
                    return True

            if hand_value == HandValue.PAIR:
                pair = calculate_pair(self.cards)
                other_pair = calculate_pair(other.cards)

                if pair != other_pair:
                    return pair > other_pair

            highest_card = self.get_highest_card()
            other_highest_card = other.get_highest_card()

            return highest_card > other_highest_card

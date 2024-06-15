from copy import deepcopy
from enum import IntEnum
from typing import List

from game import Card
from game.card import Suit


class HandBaseValue(IntEnum):
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


def highest_kind(card_values: List[int], number_of_repeats: int) -> int | None:
    kind_values = [x for x in card_values if card_values.count(x) == number_of_repeats]
    if len(kind_values) == 0:
        return None
    if 1 in kind_values:
        return 14
    return max(kind_values)


def calculate_two_pairs(card_values: List[int]) -> List[int]:
    pairs = list(set((x for x in card_values if card_values.count(x) == 2)))
    if 1 in pairs:
        pairs.append(14)
        pairs.remove(1)
    return sorted(pairs, reverse=True)


def calculate_full_house(card_values: List[int]) -> tuple:
    three = highest_kind(card_values, 3)
    pair = highest_kind(card_values, 2)
    if pair == 1:
        pair = 14
    if three == 1:
        three = 14
    return three, pair


def check_straight(hand_card_values: List[int]) -> bool:
    if len(hand_card_values) != 5:
        return False

    is_straight: bool = hand_card_values == list(range(hand_card_values[0], hand_card_values[0] - 5, -1))
    if not is_straight and hand_card_values[-1] == 1:
        temp_values = deepcopy(hand_card_values)
        temp_values[-1] = 14
        temp_values = sorted(temp_values, reverse=True)
        is_straight = temp_values == list(range(temp_values[0], temp_values[0] - 5, -1))
    return is_straight


def get_highest_single_card(cards: List[Card]) -> Card | None:
    card_values = [card.number for card in cards]
    cards_repeat_once = [card for card in cards if card_values.count(card.number) == 1]
    if len(cards_repeat_once) == 0:
        return None
    return max(cards_repeat_once)


def calculate_hand_base_value(cards: List[Card]) -> HandBaseValue:
    if len(cards) == 0:
        return HandBaseValue.ILLEGAL
    if len(cards) == 0:
        return HandBaseValue.HIGHEST_CARD

    suits = [card.suit for card in cards]
    sorted_cards = sorted(cards, key=lambda card: card.number, reverse=True)
    hand_card_values = [card.number for card in sorted_cards]

    is_flush = len(set(suits)) == 1 and len(cards) == 5
    is_straight = check_straight(hand_card_values)

    if is_flush and is_straight:
        return HandBaseValue.STRAIGHT_FLUSH

    if is_flush:
        return HandBaseValue.FLUSH

    if is_straight:
        return HandBaseValue.STRAIGHT

    if len(calculate_two_pairs(hand_card_values)) == 2:
        return HandBaseValue.TWO_PAIR

    if highest_kind(hand_card_values, 4) is not None:
        return HandBaseValue.FOUR_OF_A_KIND

    contains_pair = highest_kind(hand_card_values, 2) is not None
    contains_three = highest_kind(hand_card_values, 3) is not None

    if contains_pair and contains_three:
        return HandBaseValue.FULL_HOUSE

    if contains_three:
        return HandBaseValue.THREE_OF_A_KIND

    if contains_pair:
        return HandBaseValue.PAIR

    return HandBaseValue.HIGHEST_CARD


def factors_to_float(factors: List[int | Suit]) -> float:
    if len(factors) == 0:
        return 0
    factors_as_floats = [int(factor) * 10 ** (- 2 * (index + 1)) for index, factor in enumerate(factors)]
    return sum(factors_as_floats)


def extend_hand_base_value(base_value: HandBaseValue, cards: List[Card]) -> List[int]:
    if base_value == HandBaseValue.ILLEGAL or len(cards) == 0:
        return []

    card_values = [card.number for card in cards]

    if base_value == HandBaseValue.THREE_OF_A_KIND:
        return [highest_kind(card_values, 3)]
    if base_value == HandBaseValue.FOUR_OF_A_KIND:
        return [highest_kind(card_values, 4)]
    if base_value == HandBaseValue.FULL_HOUSE:
        return [highest_kind(card_values, 3)]

    highest_single_card = get_highest_single_card(cards)
    highest_single_card_number = (0 if highest_single_card is None else 14 if highest_single_card.number == 1
                                  else highest_single_card.number)

    if base_value == HandBaseValue.HIGHEST_CARD:
        return [
            highest_single_card.number if highest_single_card.number != 1 else 14,
            highest_single_card.suit
        ]

    if len(cards) != 1:
        hand_second_highest_card = sorted(card_values, reverse=True)[1]
    else:
        hand_second_highest_card = 0

    if base_value == HandBaseValue.PAIR:
        return [
            highest_kind(card_values, 2),
            # For pair-only hand:
            highest_single_card_number,
            highest_single_card.suit if highest_single_card is not None else 0
        ]
    if base_value == HandBaseValue.TWO_PAIR:
        pairs = calculate_two_pairs(card_values)
        return [
            max(pairs),
            min(pairs),
            highest_single_card_number,
            highest_single_card.suit if highest_single_card is not None else 0
        ]
    if base_value == HandBaseValue.STRAIGHT:
        return [
            hand_second_highest_card  # cause ace might be 1 here
        ]
    if base_value == HandBaseValue.FLUSH:
        return [
            highest_single_card_number,
            cards[0].suit
        ]
    if base_value == HandBaseValue.STRAIGHT_FLUSH:
        return [
            hand_second_highest_card,  # cause ace might be 1 here
            cards[0].suit
        ]


def compute_full_value(cards: List[Card]) -> float:
    base_value = calculate_hand_base_value(cards)
    return int(base_value) + factors_to_float(extend_hand_base_value(base_value, cards))


def has_better_cards(cards: List[Card], compared_cards: List[Card]) -> bool:
    cards_base_value = calculate_hand_base_value(cards)
    compared_base_value = calculate_hand_base_value(compared_cards)
    if cards_base_value == compared_base_value:
        return (factors_to_float(extend_hand_base_value(cards_base_value, cards)) >
                factors_to_float(extend_hand_base_value(compared_base_value, compared_cards)))
    return cards_base_value > compared_base_value


def get_potential_strength(starting_cards: List[Card], card: Card) -> HandBaseValue:
    cards = starting_cards + [card]
    hand_strength = calculate_hand_base_value(cards)
    cards.remove(card)
    return hand_strength

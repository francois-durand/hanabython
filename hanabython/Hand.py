# -*- coding: utf-8 -*-
"""
Copyright François Durand
fradurand@gmail.com

This file is part of Hanabython.

    Hanabython is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Hanabython is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Hanabython.  If not, see <http://www.gnu.org/licenses/>.
"""
from Card import Card
from Color import Color


class Hand:
    """
    The hand of a player.

    Is initialized as an empty hand.
    """

    def __init__(self):
        self._list = []

    def __repr__(self):
        return repr(self._list)

    def __str__(self):
        return '[' + ', '.join(str(card) for card in self._list) + ']'

    def receive(self, card: Card):
        self._list.insert(0, card)

    def give(self, i: int):
        return self._list.pop(i)

    def bool_list_from_color_clue(self, clue_color):
        return [card.match_color(clue_color) for card in self._list]

    def bool_list_from_value_clue(self, clue_value):
        return [card.match_value(clue_value) for card in self._list]

    # def bool_list_from_clue(self, action: Action):
    #     if action.clue_type == Action.COLOR:
    #         return [card.color == action.clue for card in self._list]
    #     else:
    #         return [card.value == action.clue for card in self._list]


if __name__ == '__main__':
    hand = Hand()
    hand.receive(Card(color=Color.RED, value=4))
    hand.receive(Card(color=Color.BLUE, value=2))
    hand.receive(Card(color=Color.MULTICOLOR, value=1))
    hand.receive(Card(color=Color.BLUE, value=2))
    hand.receive(Card(color=Color.YELLOW, value=3))
    print(hand)
    print(hand.give(2))
    print(hand)
    hand.receive(Card(color=Color.GREEN, value=2))
    print(hand)
    # print(hand.bool_list_from_clue(Action(
    #     category=Action.INFORM, clue_type=Action.VALUE, clue=2
    # )))

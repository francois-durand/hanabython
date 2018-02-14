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
from .Color import Color


class Card:
    """
    A card of Hanabi.

    :param Color color: the color of the card.
    :param int value: the value of the card (usually between 1 and 5).

    >>> my_card = Card(color=Color.BLUE, value=5)
    """
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return 'Card(color=%r, value=%r)' % (self.color, self.value)

    def __str__(self):
        return self.color.color_str(
            str(self.value) + ' ' + self.color.symbol
        )

    def match_color(self, clue_color):
        """
        React to a color clue

        :param Color clue_color: the color of the clue.

        :return: whether the card should react to a clue of color
            :attr:`clue_color`.
        :rtype: bool

        >>> card_blue = Card(color=Color.BLUE, value=3)
        >>> card_blue.match_color(Color.BLUE)
        True
        >>> card_blue.match_color(Color.RED)
        False
        >>> card_multi = Card(color=Color.MULTICOLOR, value=3)
        >>> card_multi.match_color(Color.BLUE)
        True
        >>> card_shadow = Card(color=Color.SHADOW, value=3)
        >>> card_shadow.match_color(Color.BLUE)
        False
        """
        return self.color.match(clue_color)

    def match_value(self, clue_value):
        """
        React to a value clue

        :param int clue_value: the value of the clue.

        :return: whether the card should react to a clue of value
            :attr:`clue_value`.
        :rtype: bool

        >>> card = Card(color=Color.BLUE, value=3)
        >>> card.match_value(3)
        True
        >>> card.match_value(4)
        False
        """
        return self.value == clue_value


if __name__ == '__main__':
    card = Card(color=Color.BLUE, value=3)
    print(repr(card))
    print(card)
    print('Is is blue?', card.match_color(Color.BLUE))
    print('Is it a 4?', card.match_value(4))

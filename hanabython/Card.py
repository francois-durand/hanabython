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
from Color import Color


class Card:
    """
    A card of Hanabi.

    :param Color color: the color of the card.
    :param int value: the value of the card (usually between 1 and 5)
    :param str s: a short string representing the card. Must use one of the
        standard colors, cf. :meth:`Color.from_string`.

    You can provide either :attr:`color` and :attr:`value`, or :attr:`s`.
    The constructor accepts several types of syntax, as illustrated below.

    >>> my_card = Card(color=Color.BLUE, value=3)
    >>> print(my_card)
    B3
    >>> my_card = Card(Color.BLUE, 3)
    >>> print(my_card)
    B3
    >>> my_card = Card(3, Color.BLUE)
    >>> print(my_card)
    B3
    >>> my_card = Card(s='B3')
    >>> print(my_card)
    B3
    >>> my_card = Card('B3')
    >>> print(my_card)
    B3
    >>> my_card = Card(s='3B')
    >>> print(my_card)
    B3
    >>> my_card = Card('3B')
    >>> print(my_card)
    B3

    Note: the string input works even if the value has several digits.
    >>> my_card = Card('B42')
    >>> print(my_card)
    B42
    >>> my_card = Card('51M')
    >>> print(my_card)
    M51
    """
    def __init__(self, *args, **kwargs):
        s = None
        if len(args) == 1:
            s = args[0]
        elif len(args) == 2:
            if type(args[0]) == Color:
                self.color = args[0]
                self.value = args[1]
            elif type(args[1]) == Color:
                self.value = args[0]
                self.color = args[1]
            else:
                raise ValueError('One argument should be a Color.')
        elif 's' in kwargs.keys():
            s = kwargs['s']
        else:
            self.color = kwargs['color']
            self.value = kwargs['value']
        if s is not None:
            try:
                self.value = int(s[1:])
                self.color = Color.from_symbol(s[0])
            except ValueError:
                try:
                    self.value = int(s[:-1])
                    self.color = Color.from_symbol(s[-1])
                except ValueError:
                    raise ValueError('Could not interpret as a card: ', s)

    def __repr__(self):
        return 'Card(color=%r, value=%r)' % (self.color, self.value)

    def __str__(self):
        return self.color.symbol + '' + str(self.value)

    def colored(self):
        """
        Colored version of :meth:`__str__`

        :return: the same string as :meth:`__str__`, but with ANSI escape codes
            to add colors where relevant.
        :rtype: str
        """
        return self.color.color_str(str(self))

    def match_color(self, clue_color):
        """
        React to a color clue

        :param Color clue_color: the color of the clue.

        :return: whether the card should react to a clue of color
            :attr:`clue_color`.
        :rtype: bool

        >>> from Color import Color
        >>> card_blue = Card('B3')
        >>> card_blue.match_color(Color.BLUE)
        True
        >>> card_blue.match_color(Color.RED)
        False
        >>> card_multi = Card('M3')
        >>> card_multi.match_color(Color.BLUE)
        True
        >>> card_colorless = Card('C3')
        >>> card_colorless.match_color(Color.BLUE)
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

        >>> card = Card('B3')
        >>> card.match_value(3)
        True
        >>> card.match_value(4)
        False
        """
        return self.value == clue_value


if __name__ == '__main__':
    card = Card(color=Color.BLUE, value=3)
    print('repr: ', repr(card))
    print('str: ', card)
    print('colored: ', card.colored())

    print('\nIs is blue?', card.match_color(Color.BLUE))
    print('Is it a 4?', card.match_value(4))

    import doctest
    doctest.testmod()

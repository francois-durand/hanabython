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
from hanabython.Classes.Colored import Colored
from hanabython.Classes.Color import Color


class Card(Colored):
    """
    A card of Hanabi.

    :param Color c: the color of the card.
    :param int v: the value of the card (usually between 1 and 5).
    :param str s: a short string representing the card. Must use one of the
        standard colors, cf. :meth:`Color.from_symbol`.

    You can provide either :attr:`c` and :attr:`v`, or :attr:`s`.
    The constructor accepts several types of syntax, as illustrated below.

    >>> my_card = Card(c=Color.BLUE, v=3)
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

    N.B.: the string input works even if the v has several digits.

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
            if type(args[0]) == int:
                self.v = args[0]
                self.c = args[1]
            elif type(args[1]) == int:
                self.c = args[0]
                self.v = args[1]
            else:
                raise ValueError('One argument should be an integer.')
        elif 's' in kwargs.keys():
            s = kwargs['s']
        else:
            self.c = kwargs['c']
            self.v = kwargs['v']
        if s is not None:
            try:
                self.v = int(s[1:])
                self.c = Color.from_symbol(s[0])
            except ValueError:
                try:
                    self.v = int(s[:-1])
                    self.c = Color.from_symbol(s[-1])
                except ValueError:
                    raise ValueError('Could not interpret as a card: ', s)

    def colored(self):
        return self.c.color_str(self.c.symbol + str(self.v))

    def match(self, clue):
        """
        React to a clue.

        :param int|Color clue: the clue (value or color).

        :return: whether the card should be pointed when giving this clue.
        :rtype: bool

        >>> from Classes.Color import Color
        >>> card_blue = Card('B3')
        >>> card_blue.match(Color.BLUE)
        True
        >>> card_blue.match(Color.RED)
        False
        >>> card_blue.match(3)
        True
        >>> card_blue.match(4)
        False
        >>> card_multi = Card('M3')
        >>> card_multi.match(Color.BLUE)
        True
        >>> card_colorless = Card('C3')
        >>> card_colorless.match(Color.BLUE)
        False
        """
        if type(clue) == int:
            return self.v == clue
        else:
            return self.c.match(clue)


if __name__ == '__main__':
    card = Card(c=Color.BLUE, v=3)
    card.test_str()

    print('\nIs is blue?', card.match(Color.BLUE))
    print('Is it a 4?', card.match(4))

    import doctest
    doctest.testmod()
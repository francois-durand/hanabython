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
from StringUtils import uncolor
import numpy as np
from Configuration import Configuration
from Card import Card


class DiscardPile:
    """
    The discard pile in a game of Hanabi.

    :param Configuration cfg: the configuration of the game.

    >>> from Configuration import Configuration
    >>> discard_pile = DiscardPile(Configuration.STANDARD)
    >>> print(discard_pile)
    No card discarded yet
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.chronological = []
        self.array = np.zeros(cfg.deck_array.shape, dtype=int)

    def __repr__(self):
        return '<DiscardPile: %s>' % self.str_as_chronological()

    def __str__(self):
        return uncolor(self.colored())

    def colored(self):
        """
        Colored version of :meth:`__str__`

        :return: the same string as :meth:`__str__`, but with ANSI escape codes
            to add colors where relevant.
        :rtype: str
        """
        return self.colored_fancy()

    def str_fancy(self):
        """
        Convert to nice string.

        :return: a representation of the discard pile. As of now, it is the
            one used for the standard method :meth:`__str__` (it might change
            in the future).
        :rtype: str

        >>> from Configuration import Configuration
        >>> discard_pile = DiscardPile(Configuration.STANDARD)
        >>> discard_pile.receive(Card('B3'))
        >>> discard_pile.receive(Card('R4'))
        >>> discard_pile.receive(Card('B1'))
        >>> print(discard_pile.str_fancy())
        B1 B3
        R4
        """
        return uncolor(self.colored_fancy())

    def colored_fancy(self):
        """
        Colored version of :meth:`str_fancy`

        :return: the same string as :meth:`str_fancy`, but with ANSI escape
            codes to add colors where relevant.
        :rtype: str
        """
        if len(self.chronological) == 0:
            return 'No card discarded yet'
        lines = []
        for i, c in enumerate(self.cfg.colors):
            if np.sum(self.array[i, :]) == 0:
                continue
            words = [str(Card(c, v))
                     for j, v in enumerate(self.cfg.values)
                     for _ in range(self.array[i, j])]
            lines.append(c.color_str(' '.join(words)))
        return '\n'.join(lines)

    def str_as_array(self):
        """
        Convert to string in an array-style layout.

        :return: a representation of the discard pile.
        :rtype: str

        >>> from Configuration import Configuration
        >>> discard_pile = DiscardPile(Configuration.STANDARD)
        >>> discard_pile.receive(Card('B3'))
        >>> discard_pile.receive(Card('R4'))
        >>> discard_pile.receive(Card('B1'))
        >>> print(discard_pile.str_as_array())
           1 2 3 4 5
        B [1 0 1 0 0]
        G [0 0 0 0 0]
        R [0 0 0 1 0]
        W [0 0 0 0 0]
        Y [0 0 0 0 0]
        """
        return uncolor(self.colored_as_array())

    def colored_as_array(self):
        """
        Colored version of :meth:`str_as_array`

        :return: the same string as :meth:`str_as_array`, but with ANSI escape
            codes to add colors where relevant.
        :rtype: str
        """
        to_join = [
            '   ' + ' '.join([str(i + 1) for i in range(self.cfg.n_values)])
        ]
        for i, c in enumerate(self.cfg.colors):
            to_join.append(
                c.color_str('%s %s' % (c.symbol, self.array[i, :]))
            )
        return '\n'.join(to_join)

    def str_as_list_ordered(self):
        """
        Convert to string in a list-style layout, ordered by color and value.

        :return: a representation of the discard pile.
        :rtype: str

        >>> from Configuration import Configuration
        >>> discard_pile = DiscardPile(Configuration.STANDARD)
        >>> discard_pile.receive(Card('B3'))
        >>> discard_pile.receive(Card('R4'))
        >>> discard_pile.receive(Card('B1'))
        >>> print(discard_pile.str_as_list_ordered())
        [B1, B3, R4]
        """
        return uncolor(self.colored_as_list_ordered())

    def colored_as_list_ordered(self):
        """
        Colored version of :meth:`str_as_list_ordered`

        :return: the same string as :meth:`str_as_list_ordered`, but with ANSI
            escape codes to add colors where relevant.
        :rtype: str
        """
        ordered = self.list_reordered
        return '[' + ', '.join([card.colored() for card in ordered]) + ']'

    def str_as_chronological(self):
        """
        Convert to string in a list-style layout, by chronological order.

        :return: a representation of the discard pile.
        :rtype: str

        >>> from Configuration import Configuration
        >>> discard_pile = DiscardPile(Configuration.STANDARD)
        >>> discard_pile.receive(Card('B3'))
        >>> discard_pile.receive(Card('R4'))
        >>> discard_pile.receive(Card('B1'))
        >>> print(discard_pile.str_as_chronological())
        [B3, R4, B1]
        """
        return uncolor(self.colored_as_chronological())

    def colored_as_chronological(self):
        """
        Colored version of :meth:`str_as_chronological`

        :return: the same string as :meth:`str_as_chronological`, but with ANSI
            escape codes to add colors where relevant.
        :rtype: str
        """
        return '[' + ', '.join([
            card.colored() for card in self.chronological
        ]) + ']'

    @property
    def list_reordered(self):
        """
        List of discarded cards, ordered by color and value

        :return: the list of discarded cards, by lexicographic order. The order
            on the colors is the one specified in :attr:`cfg`.
        :rtype: list

        >>> from Configuration import Configuration
        >>> discard_pile = DiscardPile(Configuration.STANDARD)
        >>> discard_pile.receive(Card('B3'))
        >>> discard_pile.receive(Card('R4'))
        >>> discard_pile.receive(Card('B1'))
        >>> discard_pile.list_reordered
        [<Card: B1>, <Card: B3>, <Card: R4>]
        """
        ordered = []
        for i, c in enumerate(self.cfg.colors):
            for j, v in enumerate(self.cfg.values):
                ordered.extend([Card(c, v)] * self.array[i, j])
        return ordered

    def receive(self, card):
        """
        Receive a card.

        :param Card card: the card discarded.

        Update the internal variables of the discard pile.

        >>> from Configuration import Configuration
        >>> discard_pile = DiscardPile(Configuration.STANDARD)
        >>> discard_pile.receive(Card('B3'))
        >>> print(discard_pile)
        B3
        """
        self.chronological.append(card)
        self.array[self.cfg.i_from_c(card.c), self.cfg.i_from_v(card.v)] += 1


if __name__ == '__main__':
    my_discard_pile = DiscardPile(Configuration.W_MULTICOLOR_SHORT)
    my_discard_pile.receive(Card('R3'))
    my_discard_pile.receive(Card('R3'))
    my_discard_pile.receive(Card('M1'))
    my_discard_pile.receive(Card('B4'))
    my_discard_pile.receive(Card('B1'))
    print('repr: ', repr(my_discard_pile))
    print('str:')
    print(my_discard_pile)
    print('colored:')
    print(my_discard_pile.colored())

    print('\nAs an array: ')
    print(my_discard_pile.str_as_array())
    print()
    print(my_discard_pile.colored_as_array())

    print('\nAs an ordered list: ')
    print(my_discard_pile.str_as_list_ordered())
    print(my_discard_pile.colored_as_list_ordered())

    print('\nAs a chronological list: ')
    print(my_discard_pile.str_as_chronological())
    print(my_discard_pile.colored_as_chronological())

    import doctest
    doctest.testmod()

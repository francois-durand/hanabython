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
from typing import List
import numpy as np
from hanabython.Modules.Colored import Colored
from hanabython.Modules.StringUtils import uncolor
from hanabython.Modules.Configuration import Configuration
from hanabython.Modules.Card import Card


class DiscardPile(Colored):
    """
    The discard pile in a game of Hanabi.

    :param cfg: the configuration of the game.

    >>> from hanabython import Configuration
    >>> discard_pile = DiscardPile(Configuration.STANDARD)
    >>> print(discard_pile)
    No card discarded yet
    """

    def __init__(self, cfg: Configuration):
        self.cfg = cfg
        self.chronological = []
        self.array = np.zeros(cfg.deck_array.shape, dtype=int)

    def __repr__(self) -> str:
        return '<DiscardPile: %s>' % self.str_as_chronological()

    def colored(self) -> str:
        return self.colored_fancy()

    def str_fancy(self) -> str:
        """
        Convert to nice string.

        :return: a representation of the discard pile. As of now, it is the
            one used for the standard method :meth:`__str__` (this behavior
            might be modified in the future).

        >>> from hanabython import Configuration
        >>> discard_pile = DiscardPile(Configuration.STANDARD)
        >>> discard_pile.receive(Card('B3'))
        >>> discard_pile.receive(Card('R4'))
        >>> discard_pile.receive(Card('B1'))
        >>> print(discard_pile.str_fancy())
        B1 B3
        R4
        """
        return uncolor(self.colored_fancy())

    def colored_fancy(self) -> str:
        """
        Colored version of :meth:`str_fancy`.
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

    def str_as_array(self) -> str:
        """
        Convert to string in an array-style layout.

        :return: a representation of the discard pile.

        >>> from hanabython import Configuration
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

    def colored_as_array(self) -> str:
        """
        Colored version of :meth:`str_as_array`.
        """
        to_join = [
            '   ' + ' '.join([str(i + 1) for i in range(self.cfg.n_values)])
        ]
        for i, c in enumerate(self.cfg.colors):
            to_join.append(
                c.color_str('%s %s' % (c.symbol, self.array[i, :]))
            )
        return '\n'.join(to_join)

    def str_as_list_ordered(self) -> str:
        """
        Convert to string in a list-style layout, ordered by color and value.

        :return: a representation of the discard pile.

        >>> from hanabython import Configuration
        >>> discard_pile = DiscardPile(Configuration.STANDARD)
        >>> discard_pile.receive(Card('B3'))
        >>> discard_pile.receive(Card('R4'))
        >>> discard_pile.receive(Card('B1'))
        >>> print(discard_pile.str_as_list_ordered())
        [B1, B3, R4]
        """
        return uncolor(self.colored_as_list_ordered())

    def colored_as_list_ordered(self) -> str:
        """
        Colored version of :meth:`str_as_list_ordered`.
        """
        ordered = self.list_reordered
        return '[' + ', '.join([card.colored() for card in ordered]) + ']'

    def str_as_chronological(self) -> str:
        """
        Convert to string in a list-style layout, by chronological order.

        :return: a representation of the discard pile.

        >>> from hanabython import Configuration
        >>> discard_pile = DiscardPile(Configuration.STANDARD)
        >>> discard_pile.receive(Card('B3'))
        >>> discard_pile.receive(Card('R4'))
        >>> discard_pile.receive(Card('B1'))
        >>> print(discard_pile.str_as_chronological())
        [B3, R4, B1]
        """
        return uncolor(self.colored_as_chronological())

    def colored_as_chronological(self) -> str:
        """
        Colored version of :meth:`str_as_chronological`.
        """
        return '[' + ', '.join([
            card.colored() for card in self.chronological
        ]) + ']'

    @property
    def list_reordered(self) -> List[Card]:
        """
        List of discarded cards, ordered by color and value.

        :return: the list of discarded cards, by lexicographic order. The order
            on the colors is the one specified in :attr:`cfg`.

        >>> from hanabython import Configuration
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

    def receive(self, card) -> None:
        """
        Receive a card.

        :param card: the card discarded.

        Update the internal variables of the discard pile.

        >>> from hanabython import Configuration
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
    my_discard_pile.test_str()

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

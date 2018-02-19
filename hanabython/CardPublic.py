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
from Color import Color
from PrintColor import PrintColor


class CardPublic:
    """
    The "public" part of a card.

    An object of this class represents what is known by all players, including
    the owner of the card.

    :param Configuration cfg: the configuration of the game.

    :var np.array can_be_c: a coefficient is True iff the card can be of the
        corresponding color.
    :var np.array can_be_v: a coefficient is True iff the card can be of the
        corresponding value.
    :var np.array yes_clued_c: a coefficient is True iff the card was
        explicitly clued as the corresponding color *and* it can be of
        this color (this precision is important for multicolor).
    :var np.array yes_clued_v: a coefficient is True iff the card was
        explicitly clued as value v.

    >>> from Configuration import Configuration
    >>> card = CardPublic(Configuration.EIGHT_COLORS)
    >>> print(card)
    BGRWYPMC 12345
    """
    def __init__(self, cfg):
        self.cfg = cfg
        self.can_be_c = np.ones(cfg.n_colors, dtype=bool)
        self.can_be_v = np.ones(cfg.n_values, dtype=bool)
        self.yes_clued_c = np.zeros(cfg.n_colors, dtype=bool)
        self.yes_clued_v = np.zeros(cfg.n_values, dtype=bool)

    def __repr__(self):
        return '<CardPublic: %s>' % self

    def __str__(self):
        return uncolor(self.colored())

    def colored(self):
        """
        Colored version of :meth:`__str__`

        :return: the same string as :meth:`__str__`, but with ANSI escape codes
            to add colors where relevant.
        :rtype: str
        """
        s = ''
        for i, c in enumerate(self.cfg.colors):
            if self.yes_clued_c[i]:
                s += "\033[7m" + c.color_str(c.symbol)
            elif self.can_be_c[i]:
                s += c.color_str(c.symbol)
            else:
                s += ' '
        s += ' '
        for i, v in enumerate(self.cfg.values):
            if self.yes_clued_v[i]:
                s += "\033[7m" + str(v) + PrintColor.RESET
            elif self.can_be_v[i]:
                s += str(v)
            else:
                s += ' '
        return s

    def _match_c(self, clue, b):
        """
        React to a clue by color.

        :param Color clue: the color of the clue.
        :param bool b: whether the card matched the clue or not.

        Updates the internal variables of the card.
        """
        for i, c in enumerate(self.cfg.colors):
            if c.match(clue) != b:
                self.can_be_c[i] = False
                self.yes_clued_c[i] = False  # important for multicolor
            if b and c.match(clue) and self.can_be_c[i]:
                self.yes_clued_c[i] = True

    def _match_v(self, clue, b):
        """
        React to a clue by value.

        :param int clue: the value of the clue.
        :param bool b: whether the card matched the clue or not.

        Updates the internal variables of the card.
        """
        i = self.cfg.i_from_v(clue)
        if b:
            self.yes_clued_v[i] = True
            self.can_be_v[:] = False
            self.can_be_v[i] = True
        else:
            self.can_be_v[i] = False

    def match(self, clue, b):
        """
        React to a clue.

        :param int|Color clue: the clue (value or color).
        :param bool b: whether the card matched the clue or not.

        Updates the internal variables of the card.

        >>> from Configuration import Configuration
        >>> cfg = Configuration.EIGHT_COLORS
        >>> card = CardPublic(cfg)
        >>> print(card)
        BGRWYPMC 12345
        >>> card.match(clue=Color.RED, b=False)
        >>> print(card)
        BG WYP C 12345
        >>> card.match(clue=Color.BLUE, b=True)
        >>> print(card)
        B        12345

        Let us try with the clues in the opposite order:

        >>> from Configuration import Configuration
        >>> card = CardPublic(Configuration.EIGHT_COLORS)
        >>> print(card)
        BGRWYPMC 12345
        >>> card.match(clue=Color.BLUE, b=True)
        >>> print(card)
        B     M  12345
        >>> card.match(clue=Color.RED, b=False)
        >>> print(card)
        B        12345

        Now with clues by value:

        >>> from Configuration import Configuration
        >>> card = CardPublic(Configuration.EIGHT_COLORS)
        >>> print(card)
        BGRWYPMC 12345
        >>> card.match(clue=3, b=False)
        >>> print(card)
        BGRWYPMC 12 45
        >>> card.match(clue=5, b=True)
        >>> print(card)
        BGRWYPMC     5
        """
        if type(clue) == int:
            self._match_v(clue, b)
        else:
            self._match_c(clue, b)


if __name__ == '__main__':
    my_card = CardPublic(Configuration.EIGHT_COLORS)
    print('repr: ', repr(my_card))
    print('str:', my_card)
    print('colored: ', my_card.colored())

    print('\nIt is not red, then it is blue:')
    print(my_card.colored())
    my_card.match(clue=Color.RED, b=False)
    print(my_card.colored())
    my_card.match(clue=Color.BLUE, b=True)
    print(my_card.colored())

    print('\nIt is blue, then it is not red:')
    my_card = CardPublic(Configuration.EIGHT_COLORS)
    print(my_card.colored())
    my_card.match(clue=Color.BLUE, b=True)
    print(my_card.colored())
    my_card.match(clue=Color.RED, b=False)
    print(my_card.colored())

    print('\nIt is not 3, then it is 5:')
    my_card = CardPublic(Configuration.EIGHT_COLORS)
    print(my_card.colored())
    my_card.match(clue=3, b=False)
    print(my_card.colored())
    my_card.match(clue=5, b=True)
    print(my_card.colored())

    print('\nIt is 5, then it is not 3:')
    my_card = CardPublic(Configuration.EIGHT_COLORS)
    print(my_card.colored())
    my_card.match(clue=5, b=True)
    print(my_card.colored())
    my_card.match(clue=3, b=False)
    print(my_card.colored())

    import doctest
    doctest.testmod()

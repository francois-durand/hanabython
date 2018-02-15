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
    >>> card = CardPublic(Configuration.CONFIG_EIGHT)
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
        s = ''
        for i in range(self.cfg.n_colors):
            c = self.cfg.c_from_i(i)
            if self.can_be_c[i]:
                s += c.symbol
            else:
                s += ' '
        s += ' '
        for i in range(self.cfg.n_values):
            v = self.cfg.v_from_i(i)
            if self.can_be_v[i]:
                s += str(v)
            else:
                s += ' '
        return s

    def colored(self):
        """
        Colored version of :meth:`__str__`

        :return: the same string as :meth:`__str__`, but with ANSI escape codes
            to add colors where relevant.
        :rtype: str
        """
        s = ''
        for i in range(self.cfg.n_colors):
            c = self.cfg.c_from_i(i)
            if self.yes_clued_c[i]:
                s += "\033[7m" + c.color_str(c.symbol)
            elif self.can_be_c[i]:
                s += c.color_str(c.symbol)
            else:
                s += ' '
        s += ' '
        for i in range(self.cfg.n_values):
            v = self.cfg.v_from_i(i)
            if self.yes_clued_v[i]:
                s += "\033[7m" + str(v) + PrintColor.RESET
            elif self.can_be_v[i]:
                s += str(v)
            else:
                s += ' '
        return s

    def match_c(self, clue_c, b):
        """
        React to a clue by color.

        :param Color clue_c: the color of the clue.
        :param bool b: whether the card matched the clue or not.

        Updates the internal variables of the card.

        >>> from Configuration import Configuration
        >>> card = CardPublic(Configuration.CONFIG_EIGHT)
        >>> print(card)
        BGRWYPMC 12345
        >>> card.match_c(clue_c=Color.RED, b=False)
        >>> print(card)
        BG WYP C 12345
        >>> card.match_c(clue_c=Color.BLUE, b=True)
        >>> print(card)
        B        12345

        >>> card = CardPublic(Configuration.CONFIG_EIGHT)
        >>> print(card)
        BGRWYPMC 12345
        >>> card.match_c(clue_c=Color.BLUE, b=True)
        >>> print(card)
        B     M  12345
        >>> card.match_c(clue_c=Color.RED, b=False)
        >>> print(card)
        B        12345
        """
        for i, c in enumerate(self.cfg.colors):
            if c.match(clue_c) != b:
                self.can_be_c[i] = False
                self.yes_clued_c[i] = False  # important for multicolor
            if b and c.match(clue_c) and self.can_be_c[i]:
                self.yes_clued_c[i] = True

    def match_v(self, clue_v, b):
        """
        React to a clue by value.

        :param int clue_v: the value of the clue.
        :param bool b: whether the card matched the clue or not.

        Updates the internal variables of the card.

        >>> from Configuration import Configuration
        >>> card = CardPublic(Configuration.CONFIG_EIGHT)
        >>> print(card)
        BGRWYPMC 12345
        >>> card.match_v(3, b=False)
        >>> print(card)
        BGRWYPMC 12 45
        >>> card.match_v(5, b=True)
        >>> print(card)
        BGRWYPMC     5
        """
        i = self.cfg.i_from_v(clue_v)
        if b:
            self.yes_clued_v[i] = True
            self.can_be_v[:] = False
            self.can_be_v[i] = True
        else:
            self.can_be_v[i] = False


if __name__ == '__main__':
    cfg = Configuration.CONFIG_EIGHT
    card = CardPublic(cfg)
    print('repr: ', repr(card))
    print('str:', card)
    print('colored: ', card.colored())

    print('\nIt is not red, then it is blue:')
    print(card.colored())
    card.match_c(clue_c=Color.RED, b=False)
    print(card.colored())
    card.match_c(clue_c=Color.BLUE, b=True)
    print(card.colored())

    print('\nIt is blue, then it is not red:')
    card = CardPublic(cfg)
    print(card.colored())
    card.match_c(clue_c=Color.BLUE, b=True)
    print(card.colored())
    card.match_c(clue_c=Color.RED, b=False)
    print(card.colored())

    print('\nIt is not 3, then it is 5:')
    card = CardPublic(cfg)
    print(card.colored())
    card.match_v(clue_v=3, b=False)
    print(card.colored())
    card.match_v(clue_v=5, b=True)
    print(card.colored())

    print('\nIt is 5, then it is not 3:')
    card = CardPublic(cfg)
    print(card.colored())
    card.match_v(clue_v=5, b=True)
    print(card.colored())
    card.match_v(clue_v=3, b=False)
    print(card.colored())

    import doctest
    doctest.testmod()

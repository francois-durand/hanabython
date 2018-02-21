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
from hanabython.Modules.Clue import Clue
from hanabython.Modules.Colored import Colored
from hanabython.Modules.Configuration import Configuration
from hanabython.Modules.Color import Color
from hanabython.Modules.StringAnsi import StringAnsi


class CardPublic(Colored):
    """
    The "public" part of a card.

    An object of this class represents what is known by all players, including
    the owner of the card.

    :param cfg: the configuration of the game.

    :var np.array can_be_c: a coefficient is True iff the card can be of the
        corresponding color.
    :var np.array can_be_v: a coefficient is True iff the card can be of the
        corresponding value.
    :var np.array yes_clued_c: a coefficient is True iff the card was
        explicitly clued as the corresponding color *and* it can be of
        this color (this precision is important for multicolor).
    :var np.array yes_clued_v: a coefficient is True iff the card was
        explicitly clued as value v.

    >>> from Modules.Configuration import Configuration
    >>> card = CardPublic(Configuration.EIGHT_COLORS)
    >>> print(card)
    BGRWYPMC 12345
    """
    def __init__(self, cfg: Configuration):
        self.cfg = cfg
        self.can_be_c = np.ones(cfg.n_colors, dtype=bool)       # type: np.array
        self.can_be_v = np.ones(cfg.n_values, dtype=bool)       # type: np.array
        self.yes_clued_c = np.zeros(cfg.n_colors, dtype=bool)   # type: np.array
        self.yes_clued_v = np.zeros(cfg.n_values, dtype=bool)   # type: np.array

    def colored(self) -> str:
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
                s += "\033[7m" + str(v) + StringAnsi.RESET
            elif self.can_be_v[i]:
                s += str(v)
            else:
                s += ' '
        return s

    def _match_c(self, x: Color, b: bool) -> None:
        """
        React to a clue by color.

        Updates the internal variables of the card.

        :param x: the color of the clue.
        :param b: whether the card matched the clue or not.
        """
        for i, c in enumerate(self.cfg.colors):
            if c.match(x) != b:
                self.can_be_c[i] = False
                self.yes_clued_c[i] = False  # important for multicolor
            if b and c.match(x) and self.can_be_c[i]:
                self.yes_clued_c[i] = True

    def _match_v(self, x: int, b: bool) -> None:
        """
        React to a clue by value.

        Updates the internal variables of the card.

        :param x: the value of the clue.
        :param b: whether the card matched the clue or not.
        """
        i = self.cfg.i_from_v(x)
        if b:
            self.yes_clued_v[i] = True
            self.can_be_v[:] = False
            self.can_be_v[i] = True
        else:
            self.can_be_v[i] = False

    def match(self, clue: Clue, b: bool) -> None:
        """
        React to a clue.

        Updates the internal variables of the card.

        :param clue: the clue.
        :param b: whether the card matches or not.

        >>> from hanabython import Configuration
        >>> cfg = Configuration.EIGHT_COLORS
        >>> card = CardPublic(cfg)
        >>> print(card)
        BGRWYPMC 12345
        >>> card.match(clue=Clue(Color.RED), b=False)
        >>> print(card)
        BG WYP C 12345
        >>> card.match(clue=Clue(Color.BLUE), b=True)
        >>> print(card)
        B        12345

        Let us try with the clues in the opposite order:

        >>> from hanabython import Configuration
        >>> card = CardPublic(Configuration.EIGHT_COLORS)
        >>> print(card)
        BGRWYPMC 12345
        >>> card.match(clue=Clue(Color.BLUE), b=True)
        >>> print(card)
        B     M  12345
        >>> card.match(clue=Clue(Color.RED), b=False)
        >>> print(card)
        B        12345

        Now with clues by value:

        >>> from Modules.Configuration import Configuration
        >>> card = CardPublic(Configuration.EIGHT_COLORS)
        >>> print(card)
        BGRWYPMC 12345
        >>> card.match(clue=Clue(3), b=False)
        >>> print(card)
        BGRWYPMC 12 45
        >>> card.match(clue=Clue(5), b=True)
        >>> print(card)
        BGRWYPMC     5
        """
        if clue.category == Clue.VALUE:
            self._match_v(clue.x, b)
        else:
            self._match_c(clue.x, b)


if __name__ == '__main__':
    my_card = CardPublic(Configuration.EIGHT_COLORS)
    my_card.test_str()

    print('\nIt is not red, then it is blue:')
    print(my_card.colored())
    my_card.match(clue=Clue(Color.RED), b=False)
    print(my_card.colored())
    my_card.match(clue=Clue(Color.BLUE), b=True)
    print(my_card.colored())

    print('\nIt is blue, then it is not red:')
    my_card = CardPublic(Configuration.EIGHT_COLORS)
    print(my_card.colored())
    my_card.match(clue=Clue(Color.BLUE), b=True)
    print(my_card.colored())
    my_card.match(clue=Clue(Color.RED), b=False)
    print(my_card.colored())

    print('\nIt is not 3, then it is 5:')
    my_card = CardPublic(Configuration.EIGHT_COLORS)
    print(my_card.colored())
    my_card.match(clue=Clue(3), b=False)
    print(my_card.colored())
    my_card.match(clue=Clue(5), b=True)
    print(my_card.colored())

    print('\nIt is 5, then it is not 3:')
    my_card = CardPublic(Configuration.EIGHT_COLORS)
    print(my_card.colored())
    my_card.match(clue=Clue(5), b=True)
    print(my_card.colored())
    my_card.match(clue=Clue(3), b=False)
    print(my_card.colored())

    import doctest
    doctest.testmod()

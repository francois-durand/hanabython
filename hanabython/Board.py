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
from Card import Card


class Board:
    """
    The board (cards successfully played) in a game of Hanabi.

    :param Configuration cfg: the configuration of the game.

    :var np.array altitude: indicates the highest card played in each color.
        E.g. with color ``c`` of index ``i``, ``altitude[i]`` is the value
        of the highest card played in color ``c``. The correspondence between
        colors and indexes is the one provided by :attr:`cfg`.

    >>> from Configuration import Configuration
    >>> board = Board(Configuration.CONFIG_STANDARD)
    >>> print(board.altitude)
    [0 0 0 0 0]
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.altitude = np.zeros(self.cfg.n_colors, dtype=int)

    def __repr__(self):
        return '<Board: %s>' % self.str_compact()

    def __str__(self):
        return self.str_fixed_space()

    def colored(self):
        """
        Colored version of :meth:`__str__`

        :return: the same string as :meth:`__str__`, but with ANSI escape codes
            to add colors where relevant.
        :rtype: str
        """
        return self.colored_fixed_space()

    def str_compact(self):
        """
        Convert to string in "compact" layout

        :return: a representation of the board.
        :rtype: str

        >>> from Configuration import Configuration
        >>> board = Board(Configuration.CONFIG_STANDARD)
        >>> for s in ['G1', 'G2', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5']:
        ...     _ = board.try_to_play(Card(s))
        >>> print(board.str_compact())
        G1 G2 Y1 Y2 Y3 Y4 Y5
        """
        return ' '.join([
            self._str_one_color(i, c)
            for i, c in enumerate(self.cfg.colors)
            if self.altitude[i] > 0
        ])

    def colored_compact(self):
        """
        Colored version of :meth:`str_compact`

        :return: the same string as :meth:`str_compact`, but with ANSI escape
            codes to add colors where relevant.
        :rtype: str
        """
        return ' '.join([
            c.color_str(self._str_one_color(i, c))
            for i, c in enumerate(self.cfg.colors)
            if self.altitude[i] > 0
        ])

    def str_fixed_space(self):
        """
        Convert to string in "fixed-space" layout

        :return: a representation of the board.
        :rtype: str

        >>> from Configuration import Configuration
        >>> board = Board(Configuration.CONFIG_STANDARD)
        >>> for s in ['G1', 'G2', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5']:
        ...     _ = board.try_to_play(Card(s))
        >>> print(board.str_fixed_space())
        B -         G 1 2       R -         W -         Y 1 2 3 4 5
        """
        length = 1 + 2 * self.cfg.n_values
        return ' '.join([
            self._str_one_color_factorized(i, c).ljust(length)
            for i, c in enumerate(self.cfg.colors)
        ])

    def colored_fixed_space(self):
        """
        Colored version of :meth:`str_fixed_space`

        :return: the same string as :meth:`str_fixed_space`, but with ANSI
            escape codes to add colors where relevant.
        :rtype: str
        """
        length = 1 + 2 * self.cfg.n_values
        return ' '.join([
            c.color_str(self._str_one_color_factorized(i, c).ljust(length))
            for i, c in enumerate(self.cfg.colors)
        ])

    def str_multi_line(self):
        """
        Convert to string in "multi-line" layout

        :return: a representation of the board.
        :rtype: str

        >>> from Configuration import Configuration
        >>> board = Board(Configuration.CONFIG_STANDARD)
        >>> for s in ['G1', 'G2', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5']:
        ...     _ = board.try_to_play(Card(s))
        >>> print(board.str_multi_line())
        -
        G1 G2
        -
        -
        Y1 Y2 Y3 Y4 Y5
        """
        return '\n'.join([
            self._str_one_color(i, c)
            for i, c in enumerate(self.cfg.colors)
        ])

    def colored_multi_line(self):
        """
        Colored version of :meth:`str_multi_line`

        :return: the same string as :meth:`str_multi_line`, but with ANSI
            escape codes to add colors where relevant.
        :rtype: str
        """
        return '\n'.join([
            c.color_str(self._str_one_color(i, c))
            for i, c in enumerate(self.cfg.colors)
        ])

    def str_multi_line_compact(self):
        """
        Convert to string in "compact multi-line" layout

        :return: a representation of the board.
        :rtype: str

        >>> from Configuration import Configuration
        >>> board = Board(Configuration.CONFIG_STANDARD)
        >>> for s in ['G1', 'G2', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5']:
        ...     _ = board.try_to_play(Card(s))
        >>> print(board.str_multi_line_compact())
        G1 G2
        Y1 Y2 Y3 Y4 Y5
        """
        return '\n'.join([
            self._str_one_color(i, c)
            for i, c in enumerate(self.cfg.colors)
            if self.altitude[i] > 0
        ])

    def colored_multi_line_compact(self):
        """
        Colored version of :meth:`str_multi_line_compact`

        :return: the same string as :meth:`str_multi_line_compact`, but with
            ANSI escape codes to add colors where relevant.
        :rtype: str
        """
        return '\n'.join([
            c.color_str(self._str_one_color(i, c))
            for i, c in enumerate(self.cfg.colors)
            if self.altitude[i] > 0
        ])

    # noinspection PyProtectedMember
    def _str_one_color(self, i, c):
        """
        Convert one color to string

        :param int i: index of the color.
        :param Color c: the color.

        :return: a representation of the cards played in this color.
        :rtype: str

        >>> from Configuration import Configuration
        >>> cfg = Configuration.CONFIG_STANDARD
        >>> board = Board(cfg)
        >>> for s in ['G1', 'G2', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5']:
        ...     _ = board.try_to_play(Card(s))
        >>> print(board._str_one_color(i=4, c=cfg.colors[4]))
        Y1 Y2 Y3 Y4 Y5
        """
        if self.altitude[i] == 0:
            return '-'
        return ' '.join([
            str(Card(c, j)) for j in range(1, self.altitude[i] + 1)
        ])

    # noinspection PyProtectedMember
    def _str_one_color_factorized(self, i, c):
        """
        Same as :meth:`_str_one_color`, but with the color symbol only once.

        :param int i: index of the color.
        :param Color c: the color.

        :return: a representation of the cards played in this color.
        :rtype: str

        >>> from Configuration import Configuration
        >>> cfg = Configuration.CONFIG_STANDARD
        >>> board = Board(cfg)
        >>> for s in ['G1', 'G2', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5']:
        ...     _ = board.try_to_play(Card(s))
        >>> print(board._str_one_color_factorized(i=4, c=cfg.colors[4]))
        Y 1 2 3 4 5
        """
        if self.altitude[i] == 0:
            return c.symbol + ' -'
        return c.symbol + ' ' + ' '.join([
            str(j) for j in range(1, self.altitude[i] + 1)
        ])

    def try_to_play(self, card):
        """
        Try to play a card on the board.

        :param Card card: the card.

        :return: True if the card is successfully played on the board, False
            otherwise (i.e. if it leads to a strike).
        :rtype: bool

        >>> from Configuration import Configuration
        >>> from Card import Card
        >>> board = Board(Configuration.CONFIG_STANDARD)
        >>> for s in ['B1', 'B2', 'Y1', 'Y3', 'B1']:
        ...     board.try_to_play(Card(s))
        True
        True
        True
        False
        False
        """
        i_c = self.cfg.i_from_c(card.c)
        if card.v == self.altitude[i_c] + 1:
            self.altitude[i_c] += 1
            return True
        else:
            return False


if __name__ == '__main__':
    my_board = Board(Configuration.CONFIG_W_MULTICOLOR_SHORT)
    for s in ['B1', 'B2', 'M1', 'M3', 'B1']:
        print('Try to play %s: ' % s, my_board.try_to_play(Card(s)))
    print('repr: ', repr(my_board))
    print('str: \n' + str(my_board))
    print('colored: \n' + my_board.colored())

    print('\nAll layout styles (str)')
    print('Compact: ')
    print(my_board.str_compact())
    print('Fixed space: ')
    print(my_board.str_fixed_space())
    print('Multi-line compact: ')
    print(my_board.str_multi_line_compact())
    print('Multi-line: ')
    print(my_board.str_multi_line())

    print('\nAll layout styles (colored)')
    print('Compact: ')
    print(my_board.colored_compact())
    print('Fixed space: ')
    print(my_board.colored_fixed_space())
    print('Multi-line compact: ')
    print(my_board.colored_multi_line_compact())
    print('Multi-line: ')
    print(my_board.colored_multi_line())

    import doctest
    doctest.testmod()

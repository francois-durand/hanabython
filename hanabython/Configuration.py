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
from Color import Color


class Configuration:
    """
    A configuration for a game of Hanabi.

    :param list colors: a list of Color objects. The order matters because it
        will be used in many occasions, including display.
    :param dict deck: a dictionary. For each color from :attr:`colors`,
        it gives a list stating the number of copies for each card.
        For example, [3, 2, 2, 2, 1] means there are 3 ones, 2 twos, etc.
        Each integer in this list must be strictly positive.
    :param int n_clues: the number of clue chips that players have.
    :param int n_misfires: the number of misfire chips that players have.
        If :attr:`n_misfires` misfire chips are used, then the game is lost
        immediately (it is not a final warning but really the end of the
        game).
    :param lambda hand_size: a function to maps the number of players to the
        number of cards in hand.

    :var int n_colors: the number of colors.
    :var dict highest: a dictionary. For each color from :attr:`colors`,
        it gives the number on the highest card in that color.
    :var int n_values: the number on the highest card in the whole deck.
    :var np.array deck_array: a numpy array of size :attr:`n_colors` *
        :attr:`n_values`. Each row represents the distribution of card in a
        color. Typically, a row is [3, 2, 2, 2, 1], meaning that there are 3
        ones, 2 twos, etc. Please note that column 0 corresponds to card
        value 1, etc.

    >>> cfg = Configuration()
    >>> print(cfg)
    B [3 2 2 2 1]
    G [3 2 2 2 1]
    R [3 2 2 2 1]
    W [3 2 2 2 1]
    Y [3 2 2 2 1]
    n_clues = 8
    n_misfires = 3
    hand_size: {2: 5, 3: 5, 4: 4, 5: 4}
    >>> c = cfg.colors[0]
    >>> print(c)
    Blue (B)
    >>> cfg.deck[c]
    [3, 2, 2, 2, 1]
    >>> cfg.n_colors
    5
    >>> cfg.highest[c]
    5
    >>> cfg.n_values
    5
    >>> print(cfg.deck_array)
    [[3 2 2 2 1]
     [3 2 2 2 1]
     [3 2 2 2 1]
     [3 2 2 2 1]
     [3 2 2 2 1]]

    Use one of the standard configurations:

    >>> cfg = Configuration.CONFIG_W_MULTICOLOR_SHORT
    >>> print(cfg)
    B [3 2 2 2 1]
    G [3 2 2 2 1]
    R [3 2 2 2 1]
    W [3 2 2 2 1]
    Y [3 2 2 2 1]
    M [1 1 1 1 1]
    n_clues = 8
    n_misfires = 3
    hand_size: {2: 5, 3: 5, 4: 4, 5: 4}

    Design a configuration manually:

    >>> from Color import Color
    >>> cfg = Configuration(
    ...     colors=[Color.BLUE, Color.MULTICOLOR],
    ...     deck={
    ...         Color.BLUE:         [3, 2, 1, 1],
    ...         Color.MULTICOLOR:   [2, 1],
    ...     },
    ...     n_clues=4, n_misfires=1,
    ...     hand_size=lambda n: 3 if n <= 3 else 2
    ... )
    >>> print(cfg)
    B [3 2 1 1]
    M [2 1 0 0]
    n_clues = 4
    n_misfires = 1
    hand_size: {2: 3, 3: 3, 4: 2, 5: 2}
    """

    #: Normal rule for hand size (5 for 3- players, 4 for 4+ players)
    HAND_SIZE_NORMAL_RULE = lambda n: 5 if n <= 3 else 4
    #: Variant for hand size (6 for 2p, 5 for 3p, 4 for 4p, 3 for 5+ players)
    HAND_SIZE_VARIANT_63 = lambda n: 3 if n >= 5 else 8 - n

    #: Five colors of the base game
    COLORS_STANDARD = [
        Color.BLUE, Color.GREEN, Color.RED, Color.WHITE, Color.YELLOW]
    #: Five colors + sixth normal color
    COLORS_W_SIXTH = [
        Color.BLUE, Color.GREEN, Color.RED, Color.WHITE, Color.YELLOW,
        Color.SIXTH
    ]
    #: Five colors + Multicolor
    COLORS_W_MULTI = [
        Color.BLUE, Color.GREEN, Color.RED, Color.WHITE, Color.YELLOW,
        Color.MULTICOLOR
    ]

    #: Standard deck of a color (1 1 1 2 2 3 3 4 5)
    COLOR_DECK_STANDARD = [3, 2, 2, 2, 1]
    #: Contents of a "short" color (1 2 3 4 5)
    COLOR_DECK_SHORT = [1, 1, 1, 1, 1]

    #: Normal deck (5 colors of 10 cards)
    DECK_STANDARD = {
        Color.BLUE:     COLOR_DECK_STANDARD,
        Color.GREEN:    COLOR_DECK_STANDARD,
        Color.RED:      COLOR_DECK_STANDARD,
        Color.WHITE:    COLOR_DECK_STANDARD,
        Color.YELLOW:   COLOR_DECK_STANDARD,
    }
    #: Deck with long sixth color (6 colors of 10 cards)
    DECK_SIXTH_LONG = DECK_STANDARD.copy()
    DECK_SIXTH_LONG[Color.SIXTH] = COLOR_DECK_STANDARD
    #: Deck with short sixth color (5 colors of 10 cards + 1 color of 5 cards)
    DECK_SIXTH_SHORT = DECK_STANDARD.copy()
    DECK_SIXTH_SHORT[Color.SIXTH] = COLOR_DECK_SHORT
    #: Deck with long multicolor (5 colors of 10 cards + 1 multi of 10 cards)
    DECK_MULTICOLOR_LONG = DECK_STANDARD.copy()
    DECK_MULTICOLOR_LONG[Color.MULTICOLOR] = COLOR_DECK_STANDARD
    #: Deck with short multicolor (5 colors of 10 cards + 1 multi of 5 cards)
    DECK_MULTICOLOR_SHORT = DECK_STANDARD.copy()
    DECK_MULTICOLOR_SHORT[Color.MULTICOLOR] = COLOR_DECK_SHORT

    def __init__(self, colors=COLORS_STANDARD, deck=DECK_STANDARD,
                 n_clues=8, n_misfires=3,
                 hand_size=HAND_SIZE_NORMAL_RULE):
        # Parameters
        self.colors = colors
        self.deck = deck
        self.n_clues = n_clues
        self.n_misfires = n_misfires
        self.hand_size = hand_size
        # Other attributes
        self.n_colors = len(colors)
        self.highest = {c: len(deck[c]) for c in colors}
        self.n_values = max(self.highest.values())
        self.deck_array = np.array([
            deck[c] + [0] * (self.n_values - len(deck[c])) for c in colors])
        # Conversions
        self._i_from_c = {colors[i]: i for i in range(len(colors))}
        self._i_from_v = lambda x: x - 1
        self._v_from_i = lambda x: x + 1

    def __repr__(self):
        return (
            'Configuration(colors=%r, deck=%r, n_clues=%r, n_misfires=%r, '
            'hand_size=%r)'
            % (self.colors, self.deck, self.n_clues, self.n_misfires,
               self.hand_size)
        )

    def __str__(self):
        s = ''
        for i in range(self.n_colors):
            s += (
                '%s %s\n' % (
                    self.colors[i].symbol, self.deck_array[i, :])
            )
        s += 'n_clues = %s\n' % self.n_clues
        s += 'n_misfires = %s\n' % self.n_misfires
        s += 'hand_size: ' + str({n: self.hand_size(n) for n in range(2, 6)})
        return s

    def colored(self):
        s = ''
        for i in range(self.n_colors):
            s += self.colors[i].color_str(
                '%s %s\n' % (
                    self.colors[i].symbol, self.deck_array[i, :])
            )
        s += 'n_clues = %s\n' % self.n_clues
        s += 'n_misfires = %s\n' % self.n_misfires
        s += 'hand_size: ' + str({n: self.hand_size(n) for n in range(2, 6)})
        return s

    def i_from_c(self, c):
        """
        Finds index from a color (for example in :attr:`deck_array`).

        :param Color c: a color.

        :return: the corresponding index.
        :rtype: Color

        >>> from Color import Color
        >>> cfg = Configuration()
        >>> cfg.i_from_c(Color.BLUE)
        0
        """
        return self._i_from_c[c]

    def i_from_v(self, v):
        """
        Finds index from a value (for example in :attr:`deck_array`).

        :param int v: the value (typically 1 to 5).

        :return: the corresponding index (typically 0 to 4).
        :rtype: int

        >>> cfg = Configuration()
        >>> cfg.i_from_v(1)
        0
        """
        return self._i_from_v(v)

    def c_from_i(self, i):
        """
        Finds color from an index (for example in :attr:`deck_array`).

        This is simply an alias for `self.colors[i]`, created for homogeneity
        with other similar methods.

        :param int i: an index.

        :return: the corresponding color.
        :rtype: Color

        >>> cfg = Configuration()
        >>> print(cfg.c_from_i(0))
        Blue (B)
        """
        return self.colors[i]

    def v_from_i(self, i: int) -> int:
        """
        Finds value from an index (for example in :attr:`deck_array`).

        :param int i: an index (typically 0 to 4).

        :return: the corresponding value (typically 1 to 5).
        :rtype: int

        >>> cfg = Configuration()
        >>> cfg.v_from_i(0)
        1
        """
        return self._v_from_i(i)

    #: Standard configuration
    CONFIG_STANDARD = None
    #: Configuration with long sixth color
    CONFIG_W_SIXTH_LONG = None
    #: Configuration with short sixth color
    CONFIG_W_SIXTH_SHORT = None
    #: Configuration with long multicolor
    CONFIG_W_MULTICOLOR_LONG = None
    #: Configuration with short multicolor
    CONFIG_W_MULTICOLOR_SHORT = None


Configuration.CONFIG_STANDARD = Configuration()
Configuration.CONFIG_W_SIXTH_LONG = Configuration(
    colors=Configuration.COLORS_W_SIXTH,
    deck=Configuration.DECK_SIXTH_LONG,
)
Configuration.CONFIG_W_SIXTH_SHORT = Configuration(
    colors=Configuration.COLORS_W_SIXTH,
    deck=Configuration.DECK_SIXTH_SHORT,
)
Configuration.CONFIG_W_MULTICOLOR_LONG = Configuration(
    colors=Configuration.COLORS_W_MULTI,
    deck=Configuration.DECK_MULTICOLOR_LONG,
)
Configuration.CONFIG_W_MULTICOLOR_SHORT = Configuration(
    colors=Configuration.COLORS_W_MULTI,
    deck=Configuration.DECK_MULTICOLOR_SHORT,
)


if __name__ == '__main__':
    cfg = Configuration()
    print('repr: ', repr(cfg))
    print('\nstr: ')
    print(cfg)
    print('\ncolored: ')
    print(cfg.colored())

    print('\nAttributes: ')
    for k in cfg.__dict__.keys():
        if not k.startswith('_'):
            print(k + ': ', cfg.__dict__[k])

    print('\nOther standard configurations: ')
    print(Configuration.CONFIG_W_SIXTH_LONG.colored() + '\n')
    print(Configuration.CONFIG_W_SIXTH_SHORT.colored() + '\n')
    print(Configuration.CONFIG_W_MULTICOLOR_LONG.colored() + '\n')
    print(Configuration.CONFIG_W_MULTICOLOR_SHORT.colored() + '\n')

    import doctest
    doctest.testmod()

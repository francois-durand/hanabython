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
from typing import List, Dict
from hanabython.Modules.Colored import Colored
from hanabython.Modules.Color import Color
from hanabython.Modules.ConfigurationDeck import ConfigurationDeck
from hanabython.Modules.ConfigurationHandSize import ConfigurationHandSize
from hanabython.Modules.ConfigurationEndRule import ConfigurationEndRule


class Configuration(Colored):
    """
    A configuration for a game of Hanabi.

    :param deck: the configuration of the deck.
    :param n_clues: the number of clue chips that players have.
    :param n_misfires: the number of misfire chips that players have.
        If :attr:`n_misfires` misfire chips are used, then the game is lost
        immediately (it is not a final warning but really the end of the
        game).
    :param hand_size_rule: the rule used for the initial
        size of the hands.
    :param end_rule: the rule used to determine when
        then game is finished.

    :var list colors: a list of Color objects. It is the list of keys
        of :attr:`deck`.
    :var int n_colors: the number of colors.
    :var list highest: For each color from :attr:`colors`, it gives the number
        on the highest card in that color.
    :var int n_values: the number on the highest card in the whole deck.
    :var list values: the list of possible values (from 1 to :attr:`n_values`).
    :var np.array deck_array: a numpy array of size :attr:`n_colors` *
        :attr:`n_values`. Each row represents the distribution of cards in a
        color. Typically, a row is [3, 2, 2, 2, 1], meaning that there are 3
        ones, 2 twos, etc. Please note that column 0 corresponds to card
        value 1, etc.
    :var int n_cards: the total number of cards in the deck (50 in the
        standard configuration).
    :var int max_score: the maximum possible score (25 in the standard
        configuration).

    >>> cfg = Configuration.W_MULTICOLOR_SHORT
    >>> print(cfg)
    Deck: with short multicolor (5 cards).
    Number of clues: 8.
    Number of misfires: 3.
    End rule: normal.
    >>> print(cfg.hand_size_rule)
    normal
    >>> print(cfg.colors)
    [<Color: B>, <Color: G>, <Color: R>, <Color: W>, <Color: Y>, <Color: M>]
    >>> print(cfg.n_colors)
    6
    >>> print(cfg.highest)
    [5, 5, 5, 5, 5, 5]
    >>> print(cfg.n_values)
    5
    >>> print(cfg.values)
    [1, 2, 3, 4, 5]
    >>> print(cfg.deck_array)
    [[3 2 2 2 1]
     [3 2 2 2 1]
     [3 2 2 2 1]
     [3 2 2 2 1]
     [3 2 2 2 1]
     [1 1 1 1 1]]
    >>> print(cfg.n_cards)
    55
    >>> print(cfg.max_score)
    30

    Design a configuration manually:

    >>> from hanabython import ConfigurationDeck
    >>> from hanabython import Color
    >>> from hanabython import ConfigurationColorContents
    >>> cfg = Configuration(
    ...     deck=ConfigurationDeck(contents=[
    ...         (Color.BLUE, ConfigurationColorContents([3, 2, 1, 1])),
    ...         (Color.RED, ConfigurationColorContents([2, 1])),
    ...     ]),
    ...     n_clues=4,
    ...     n_misfires=1,
    ...     hand_size_rule=ConfigurationHandSize.VARIANT_6_3,
    ...     end_rule=ConfigurationEndRule.CROWNING_PIECE
    ... )
    >>> print(cfg)
    Deck: B [3, 2, 1, 1], R [2, 1].
    Number of clues: 4.
    Number of misfires: 1.
    End rule: Crowning Piece.
    """
    def __init__(
        self,
        deck: ConfigurationDeck = ConfigurationDeck.NORMAL,
        n_clues: int = 8,
        n_misfires: int = 3,
        hand_size_rule: ConfigurationHandSize = ConfigurationHandSize.NORMAL,
        end_rule: ConfigurationEndRule = ConfigurationEndRule.NORMAL
    ):
        # Parameters
        self.deck = deck
        self.n_clues = n_clues
        self.n_misfires = n_misfires
        self.hand_size_rule = hand_size_rule
        self.end_rule = end_rule
        # Other attributes
        self.colors = list(deck.keys())                     # type: List[Color]
        self.n_colors = len(self.colors)                    # type: int
        self.highest = [len(deck[c]) for c in self.colors]  # type: List[int]
        self.n_values = max(self.highest)                   # type: int
        self.values = list(range(1, self.n_values + 1))     # type: List[int]
        self.deck_array = np.array([
            deck[c] + [0] * (self.n_values - len(deck[c]))
            for c in self.colors
        ])                                                  # type: np.array
        self.n_cards = np.sum(self.deck_array)              # type: int
        self.max_score = sum(self.highest)                  # type: int
        # Conversion
        self._i_from_c_name = {
            c.name: i for i, c in enumerate(self.colors)
        }                                               # type: Dict[Color, int]

    def __repr__(self) -> str:
        return (
            '<Configuration: %r, n_clues=%s, n_misfires=%s, '
            '%r, %r>'
            % (self.deck, self.n_clues, self.n_misfires,
               self.hand_size_rule, self.end_rule)
        )

    def colored(self) -> str:
        return '\n'.join([
            'Deck: %s.' % self.deck.colored(),
            'Number of clues: %s.' % self.n_clues,
            'Number of misfires: %s.' % self.n_misfires,
            'End rule: %s.' % self.end_rule.colored()
        ])

    def i_from_c(self, c: Color) -> int:
        """
        Finds index from a color (for example in :attr:`deck_array`).

        :param c: a color.

        :return: the corresponding index.

        >>> from Modules.Color import Color
        >>> Configuration.STANDARD.i_from_c(Color.BLUE)
        0
        """
        return self._i_from_c_name[c.name]

    # noinspection PyMethodMayBeStatic
    def i_from_v(self, v: int) -> int:
        """
        Finds index from a value (for example in :attr:`deck_array`).

        :param v: the value (typically 1 to 5).

        :return: the corresponding index (typically 0 to 4).

        >>> Configuration.STANDARD.i_from_v(1)
        0
        """
        return v - 1

    #: Standard configuration.
    STANDARD = None
    #: Configuration with long sixth color.
    W_SIXTH = None
    #: Configuration with short sixth color.
    W_SIXTH_SHORT = None
    #: Configuration with long multicolor.
    W_MULTICOLOR = None
    #: Configuration with short multicolor.
    W_MULTICOLOR_SHORT = None
    #: Configuration with 8 long colors (6 normal + multicolor + colorless).
    EIGHT_COLORS = None


Configuration.STANDARD = Configuration()
Configuration.W_SIXTH = Configuration(
    deck=ConfigurationDeck.W_SIXTH)
Configuration.W_SIXTH_SHORT = Configuration(
    deck=ConfigurationDeck.W_SIXTH_SHORT)
Configuration.W_MULTICOLOR = Configuration(
    deck=ConfigurationDeck.W_MULTICOLOR)
Configuration.W_MULTICOLOR_SHORT = Configuration(
    deck=ConfigurationDeck.W_MULTICOLOR_SHORT)
Configuration.EIGHT_COLORS = Configuration(
    deck=ConfigurationDeck.EIGHT_COLORS)


if __name__ == '__main__':
    my_cfg = Configuration.EIGHT_COLORS
    my_cfg.test_str()

    print('\nAttributes: ')
    for k in my_cfg.__dict__.keys():
        if not k.startswith('_'):
            print(k + ': ', my_cfg.__dict__[k])

    print('\nOther standard configurations: ')
    print(Configuration.W_SIXTH.colored() + '\n')
    print(Configuration.W_SIXTH_SHORT.colored() + '\n')
    print(Configuration.W_MULTICOLOR.colored() + '\n')
    print(Configuration.W_MULTICOLOR_SHORT.colored() + '\n')

    print('\nA manual configuration: ')
    from Modules.ConfigurationColorContents import ConfigurationColorContents
    my_cfg = Configuration(
        deck=ConfigurationDeck(contents=[
            (Color.BLUE, ConfigurationColorContents([3, 2, 1, 1])),
            (Color.RED, ConfigurationColorContents([2, 1])),
        ]),
        n_clues=4,
        n_misfires=1,
        hand_size_rule=ConfigurationHandSize.VARIANT_6_3,
        end_rule=ConfigurationEndRule.CROWNING_PIECE
    )
    print(my_cfg.colored())

    import doctest
    doctest.testmod()

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
from hanabython.Classes.Color import Colored
from hanabython.Classes.Configuration import Configuration
from hanabython.Classes.CardPublic import CardPublic


class HandPublic(Colored, list):
    """
    The "public" part of a hand.

    An object of this class represents what is known by all players, including
    the owner of the hand.

    We use the same convention as in Board Game Arena: newest cards are on the
    left (i.e. at the beginning of the list) and oldest cards are on the right
    (i.e. at the end of the list).

    Basically, a HandPublic is a list of CardPublic objects.

    :param Configuration cfg: the configuration of the game.
    :param int n_cards: the number of cards in the hand. N.B.: this parameter
        is mostly used for examples and tests. In contrast, at the beginning of
        a game, the hand should be initialized with 0 cards, because cards will
        be given to the players during the initial dealing of hands.

    >>> from Classes.Configuration import Configuration
    >>> hand = HandPublic(cfg=Configuration.STANDARD, n_cards=4)
    >>> print(hand)
    [BGRWY 12345, BGRWY 12345, BGRWY 12345, BGRWY 12345]
    """
    def __init__(self, cfg, n_cards=0):
        super().__init__()
        self.cfg = cfg
        for i in range(n_cards):
            self.receive()

    def colored(self):
        return '[' + ', '.join([card.colored() for card in self]) + ']'

    def receive(self):
        """
        Receive a card.

        An unknown card is added on the left, i.e. at the beginning of the list.

        >>> from Classes.Configuration import Configuration
        >>> hand = HandPublic(cfg=Configuration.STANDARD, n_cards=4)
        >>> hand.match(clue=5, bool_list=[True, True, False, False])
        >>> print(hand)
        [BGRWY     5, BGRWY     5, BGRWY 1234 , BGRWY 1234 ]
        >>> hand.receive()
        >>> print(hand)
        [BGRWY 12345, BGRWY     5, BGRWY     5, BGRWY 1234 , BGRWY 1234 ]
        """
        self.insert(0, CardPublic(self.cfg))

    def give(self, i):
        """
        Give a card.

        :param int i: the position of the card in the hand (0 = newest).

        The card is simply suppressed from the hand.

        >>> from Classes.Configuration import Configuration
        >>> hand = HandPublic(cfg=Configuration.STANDARD, n_cards=4)
        >>> hand.match(clue=5, bool_list=[False, True, False, False])
        >>> hand.match(clue=4, bool_list=[True, False, False, False])
        >>> print(hand)
        [BGRWY    4 , BGRWY     5, BGRWY 123  , BGRWY 123  ]
        >>> hand.give(1)
        >>> print(hand)
        [BGRWY    4 , BGRWY 123  , BGRWY 123  ]
        """
        self.pop(i)

    def match(self, clue, bool_list):
        """
        React to a clue

        :param int|Color clue: the clue (value or Color).
        :param list bool_list: a list of booleans. The ``i``-th coefficient is
            ``True`` iff the ``i``-th card of the hand matches the clue given.

        Updates the internal variables of the hand.

        >>> from Classes.Configuration import Configuration
        >>> hand = HandPublic(cfg=Configuration.STANDARD, n_cards=4)
        >>> hand.match(clue=3, bool_list=[False, True, False, False])
        >>> print(hand)
        [BGRWY 12 45, BGRWY   3  , BGRWY 12 45, BGRWY 12 45]
        >>> from Classes.Color import Color
        >>> hand.match(clue=Color.RED, bool_list=[False, True, False, False])
        >>> print(hand)
        [BG WY 12 45,   R     3  , BG WY 12 45, BG WY 12 45]
        """
        for i, card in enumerate(self):
            card.match(clue=clue, b=bool_list[i])


if __name__ == '__main__':
    my_hand = HandPublic(cfg=Configuration(), n_cards=4)
    my_hand.test_str()

    from Classes.Color import Color
    print("\nLet's give some clues: ")
    print(my_hand.colored())
    my_hand.match(clue=Color.RED, bool_list=[True, False, True, False, False])
    print(my_hand.colored())
    my_hand.match(clue=Color.BLUE, bool_list=[False, True, False, False, False])
    print(my_hand.colored())
    my_hand.match(clue=3, bool_list=[True, False, False, True, False])
    print(my_hand.colored())

    print("\nGive card in position 2: ")
    my_hand.give(2)
    print(my_hand.colored())
    print("Receive a new card: ")
    my_hand.receive()
    print(my_hand.colored())

    import doctest
    doctest.testmod()
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
from Configuration import Configuration
from CardPublic import CardPublic


class HandPublic(list):
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

    >>> from Configuration import Configuration
    >>> hand = HandPublic(cfg=Configuration.CONFIG_STANDARD, n_cards=4)
    >>> print(hand)
    [BGRWY 12345, BGRWY 12345, BGRWY 12345, BGRWY 12345]
    """
    def __init__(self, cfg, n_cards=0):
        super().__init__()
        self.cfg = cfg
        for i in range(n_cards):
            self.receive()

    def __repr__(self):
        return '<HandPublic: %s>' % str(self)

    def __str__(self):
        return '[' + ', '.join([str(card) for card in self]) + ']'

    def colored(self):
        """
        Colored version of :meth:`__str__`

        :return: the same string as :meth:`__str__`, but with ANSI escape codes
            to add colors where relevant.
        :rtype: str
        """
        return '[' + ', '.join([card.colored() for card in self]) + ']'

    def receive(self):
        """
        Receive a card.

        An unknown card is added on the left, i.e. at the beginning of the list.

        >>> from Configuration import Configuration
        >>> hand = HandPublic(cfg=Configuration.CONFIG_STANDARD, n_cards=4)
        >>> hand.match_v(clue_v=5, bool_list=[True, True, False, False])
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

        >>> from Configuration import Configuration
        >>> hand = HandPublic(cfg=Configuration.CONFIG_STANDARD, n_cards=4)
        >>> hand.match_v(clue_v=5, bool_list=[False, True, False, False])
        >>> hand.match_v(clue_v=4, bool_list=[True, False, False, False])
        >>> print(hand)
        [BGRWY    4 , BGRWY     5, BGRWY 123  , BGRWY 123  ]
        >>> hand.give(1)
        >>> print(hand)
        [BGRWY    4 , BGRWY 123  , BGRWY 123  ]
        """
        self.pop(i)

    def match_c(self, clue_c, bool_list):
        """
        React to a clue by color

        :param Color clue_c: the color of the clue.
        :param list bool_list: a list of booleans. The ``i``-th coefficient is
            ``True`` iff the ``i``-th card of the hand matches the clue given.

        Updates the internal variables of the hand.

        >>> from Configuration import Configuration
        >>> from Color import Color
        >>> hand = HandPublic(cfg=Configuration.CONFIG_STANDARD, n_cards=4)
        >>> hand.match_c(clue_c=Color.RED,
        ...              bool_list=[False, True, False, False])
        >>> print(hand)
        [BG WY 12345,   R   12345, BG WY 12345, BG WY 12345]
        """
        for i, card in enumerate(self):
            card.match_c(clue_c=clue_c, b=bool_list[i])

    def match_v(self, clue_v, bool_list):
        """
        React to a clue by value

        :param int clue_v: the value of the clue.
        :param list bool_list: a list of booleans. The ``i``-th coefficient is
            ``True`` iff the ``i``-th card of the hand matches the clue given.

        Updates the internal variables of the hand.

        >>> from Configuration import Configuration
        >>> hand = HandPublic(cfg=Configuration.CONFIG_STANDARD, n_cards=4)
        >>> hand.match_v(clue_v=3, bool_list=[False, True, False, False])
        >>> print(hand)
        [BGRWY 12 45, BGRWY   3  , BGRWY 12 45, BGRWY 12 45]
        """
        for i, card in enumerate(self):
            card.match_v(clue_v=clue_v, b=bool_list[i])


if __name__ == '__main__':
    my_hand = HandPublic(cfg=Configuration(), n_cards=4)
    print('repr:', repr(my_hand))
    print('str:', my_hand)
    print('colored: ', my_hand.colored())

    from Color import Color
    print("\nLet's give some clues: ")
    print(my_hand.colored())
    my_hand.match_c(clue_c=Color.RED,
                    bool_list=[True, False, True, False, False])
    print(my_hand.colored())
    my_hand.match_c(clue_c=Color.BLUE,
                    bool_list=[False, True, False, False, False])
    print(my_hand.colored())
    my_hand.match_v(clue_v=3,
                    bool_list=[True, False, False, True, False])
    print(my_hand.colored())

    print("\nGive card in position 2: ")
    my_hand.give(2)
    print(my_hand.colored())
    print("Receive a new card: ")
    my_hand.receive()
    print(my_hand.colored())

    import doctest
    doctest.testmod()

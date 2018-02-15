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
from Card import Card
from Color import Color


class Hand(list):
    """
    The hand of a player.

    We use the same convention as in Board Game Arena: newest cards are on the
    left (i.e. at the beginning of the list) and oldest cards are on the right
    (i.e. at the end of the list).

    Basically, a Hand is a list of Card objects. It can be constructed as such,
    or using a list of strings which will be automatically converted to cards.

    >>> hand = Hand([Card('Y3'), Card('M1'), Card('B2'), Card('R4')])
    >>> print(hand)
    [Y3, M1, B2, R4]
    >>> hand = Hand(['Y3', 'M1', 'B2', 'R4'])
    >>> print(hand)
    [Y3, M1, B2, R4]
    """
    def __init__(self, source=None):
        super().__init__()
        if source is not None:
            for item in source:
                if type(item) == Card:
                    self.append(item)
                else:
                    self.append(Card(item))

    def __str__(self):
        return '[' + ', '.join(str(card) for card in self) + ']'

    def colored(self):
        """
        Colored version of :meth:`__str__`

        :return: the same string as :meth:`__str__`, but with ANSI escape codes
            to add colors where relevant.
        :rtype: str
        """
        return '[' + ', '.join(card.colored() for card in self) + ']'

    def receive(self, card):
        """
        Receive a card

        :param Card card: the card received.

        The card is added on the left, i.e. at the beginning of the list.

        >>> hand = Hand(['Y3', 'M1', 'B2', 'R4'])
        >>> hand.receive(Card('G2'))
        >>> print(hand)
        [G2, Y3, M1, B2, R4]
        """
        self.insert(0, card)

    def give(self, i):
        """
        Give a card

        :param int i: the position of the card in the hand (0 = newest).

        :return: the card given.
        :rtype: Card

        >>> hand = Hand(['Y3', 'B1', 'M1', 'B2', 'R4'])
        >>> card = hand.give(1)
        >>> print(card)
        B1
        """
        return self.pop(i)

    def match_c(self, clue_c):
        """
        React to a clue by color

        :param Color clue_c: the color of the clue.

        :return: a list of booleans. The ``i``-th coefficient is ``True``
            iff the ``i``-th card of the hand matches the clue given.
        :rtype: list

        >>> hand = Hand(['G2', 'Y3', 'M1', 'B2', 'R4'])
        >>> hand.match_c(Color.RED)
        [False, False, True, False, True]
        """
        return [card.match_c(clue_c) for card in self]

    def match_v(self, clue_v):
        """
        React to a clue by value

        :param int clue_v: the value of the clue.

        :return: a list of booleans. The ``i``-th coefficient is ``True``
            iff the ``i``-th card of the hand matches the clue given.
        :rtype: list

        >>> hand = Hand(['G2', 'Y3', 'M1', 'B2', 'R4'])
        >>> hand.match_v(2)
        [True, False, False, True, False]
        """
        return [card.match_v(clue_v) for card in self]

    # def match_clue(self, action: Action):
    #     if action.clue_type == Action.COLOR:
    #         return self.match_c(action.clue)
    #     else:
    #         return self.match_v(action.clue)


if __name__ == '__main__':
    hand = Hand(['Y3', 'B1', 'M1', 'B2', 'R4'])
    print('repr: ', repr(hand))
    print('str: ', hand)
    print('colored: ', hand.colored())

    my_card = hand.give(1)
    print('\nCard given: ', my_card.colored())
    print(hand.colored())

    my_card = Card(color=Color.GREEN, value=2)
    hand.receive(my_card)
    print('\nCard received: ', my_card.colored())
    print(hand.colored())

    print('\nMatch red clue:')
    print(hand.match_c(Color.RED))

    print('\nMatch clue 2:')
    print(hand.match_v(2))
    # print(hand.bool_list_from_clue(Action(
    #     category=Action.INFORM, clue_type=Action.VALUE, clue=2
    # )))

    import doctest
    doctest.testmod()

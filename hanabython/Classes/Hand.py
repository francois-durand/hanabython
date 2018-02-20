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
from hanabython.Classes.Colored import Colored
from hanabython.Classes.Card import Card
from hanabython.Classes.Color import Color


class Hand(Colored, list):
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

    def colored(self):
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

    def match(self, clue):
        """
        React to a clue.

        :param int|Color clue: the clue (value or color).

        :return: a list of booleans. The ``i``-th coefficient is ``True``
            iff the ``i``-th card of the hand matches the clue given.
        :rtype: list

        >>> hand = Hand(['G2', 'Y3', 'M1', 'B2', 'R4'])
        >>> hand.match(Color.RED)
        [False, False, True, False, True]
        >>> hand.match(2)
        [True, False, False, True, False]
        """
        return [card.match(clue) for card in self]


if __name__ == '__main__':
    my_hand = Hand(['Y3', 'B1', 'M1', 'B2', 'R4'])
    my_hand.test_str()

    my_card = my_hand.give(1)
    print('\nCard given: ', my_card.colored())
    print(my_hand.colored())

    my_card = Card('G2')
    my_hand.receive(my_card)
    print('\nCard received: ', my_card.colored())
    print(my_hand.colored())

    print('\nMatch red clue:')
    print(my_hand.match(Color.RED))

    print('\nMatch clue 2:')
    print(my_hand.match(2))
    # print(hand.bool_list_from_clue(Action(
    #     category=Action.INFORM, clue_type=Action.VALUE, clue=2
    # )))

    import doctest
    doctest.testmod()

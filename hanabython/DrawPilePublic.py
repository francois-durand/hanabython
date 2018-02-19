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
from Configuration import Configuration


class DrawPilePublic:
    """
    The public part of a draw pile.

    An object of this class represents what is known by all players. In the
    normal version of the game and all official variants, it is only the number
    of cards left.

    :param Configuration cfg: the configuration of the game.

    >>> from Configuration import Configuration
    >>> draw_pile = DrawPilePublic(cfg=Configuration.STANDARD)
    >>> print(draw_pile)
    50 cards left
    """
    def __init__(self, cfg):
        self.cfg = cfg
        self.n_cards = cfg.n_cards

    def __repr__(self):
        return '<DrawPilePublic: %s>' % self

    def __str__(self):
        return uncolor(self.colored())

    def colored(self):
        if self.n_cards == 0:
            return 'No card left'
        if self.n_cards == 1:
            return '1 card left'
        return str(self.n_cards) + ' cards left'

    def give(self):
        """
        Give the card from the top of pile.

        Updates the internal variables of the pile.

        >>> from Configuration import Configuration
        >>> draw_pile = DrawPilePublic(cfg=Configuration.STANDARD)
        >>> print(draw_pile)
        50 cards left
        >>> while draw_pile.n_cards >= 2:
        ...     draw_pile.give()
        >>> print(draw_pile)
        1 card left
        >>> draw_pile.give()
        >>> print(draw_pile)
        No card left
        """
        if self.n_cards > 0:
            self.n_cards -= 1


if __name__ == '__main__':
    my_draw_pile = DrawPilePublic(Configuration.STANDARD)
    print('repr: ', repr(my_draw_pile))
    print('str: ', my_draw_pile)
    print('colored: ', my_draw_pile.colored())

    print('\nDraw a card: ')
    my_draw_pile.give()
    print(my_draw_pile)
    while my_draw_pile.n_cards >= 2:
        my_draw_pile.give()
    print('\nOnce many cards are drawn..')
    print(my_draw_pile)
    print('Draw the last card...')
    my_draw_pile.give()
    print(my_draw_pile)
    print('Try to draw another card...')
    my_draw_pile.give()
    print(my_draw_pile)

    import doctest
    doctest.testmod()

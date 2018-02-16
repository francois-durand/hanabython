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
from Action import Action


class ActionDiscard(Action):
    """
    An action of a player: discard.

    :param int k: position of the card in the hand (between 0 and #cards - 1).
        Be careful: as of now, :attr:`__str__` expresses the position in
        "user-friendly" format, i.e. between 1 and #cards (this behavior might
        change in the future).

    >>> action = ActionDiscard(k=2)
    >>> print(repr(action))
    <ActionDiscard: 2>
    >>> print(action)
    Discard card in position 3
    """
    def __init__(self, k):
        super().__init__(Action.DISCARD)
        self.k = k

    def __repr__(self):
        return '<ActionDiscard: %s>' % self.k

    def __str__(self):
        return 'Discard card in position %s' % (self.k + 1)


if __name__ == '__main__':
    my_action = ActionDiscard(k=2)
    print('repr: ', repr(my_action))
    print('str: ', str(my_action))
    print('colored: ', my_action.colored())

    import doctest
    doctest.testmod()
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
class Action:
    """
    An action performed by a player (Discard, Play, Clue or Forfeit)

    :param int category: can be :attr:`Action.DISCARD`, :attr:`Action.PLAY`,
        :attr:`Action.CLUE` or :attr:`Action.FORFEIT`.

    Generally, only subclasses are instantiated. Cf. :class:`ActionDiscard`,
    :class:`ActionPlay`, :class:`ActionClue` and :class:`ActionForfeit`.
    """

    #:
    DISCARD = 0
    #:
    PLAY = 1
    #:
    CLUE = 2
    #:
    FORFEIT = 3
    #: Possibles categories of action.
    CATEGORIES = {DISCARD, PLAY, CLUE, FORFEIT}

    def __init__(self, category):
        self.category = category
        if category not in Action.CATEGORIES:
            raise ValueError('Unknown action category: ', category)

    def colored(self):
        """
        Colored version of :meth:`__str__`

        :return: the same string as :meth:`__str__`, but with ANSI escape codes
            to add colors where relevant.
        :rtype: str
        """
        return str(self)
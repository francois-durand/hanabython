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


class ActionClue(Action):
    """
    An action of a player: give a clue.

    :param int player_relative_position: the position of the concerned player,
        relatively (i.e. 1 for next player, 2 for second next player, etc.).
    :param Color|int clue: a Color object or a card value.

    >>> action = ActionClue(player_relative_position=1, clue=2)
    >>> print(action)
    Clue 2 to player in relative position 1
    >>> from Color import Color
    >>> action = ActionClue(player_relative_position=2, clue=Color.BLUE)
    >>> print(action)
    Clue Blue (B) to player in relative position 2
    """

    def __init__(self, player_relative_position, clue):
        super().__init__(Action.CLUE)
        self.player_relative_position = player_relative_position
        self.clue = clue

    def __repr__(self):
        return '<ActionClue: %s to player %s>' % (
            self.clue, self.player_relative_position)

    def __str__(self):
        return 'Clue %s to player in relative position %s' % (
            self.clue, self.player_relative_position)

    def colored(self):
        """
        Colored version of :meth:`__str__`

        :return: the same string as :meth:`__str__`, but with ANSI escape codes
            to add colors where relevant.
        :rtype: str
        """
        if type(self.clue) == int:
            return str(self)
        else:
            return 'Clue %s to player in relative position %s' % (
                self.clue.colored(), self.player_relative_position)


if __name__ == '__main__':
    my_action = ActionClue(player_relative_position=1, clue=3)
    print('repr: ', repr(my_action))
    print('str: ', str(my_action))
    print('colored: ', my_action.colored())

    from Color import Color
    my_action = ActionClue(player_relative_position=1, clue=Color.BLUE)
    print('\nrepr: ', repr(my_action))
    print('str: ', str(my_action))
    print('colored: ', my_action.colored())

    import doctest
    doctest.testmod()

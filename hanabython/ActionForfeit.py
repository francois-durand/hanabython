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
from Action import Action
from PrintColor import PrintColor


class ActionForfeit(Action):
    """
    An action of a player: forfeit (lose the game immediately).

    >>> action = ActionForfeit()
    >>> print(repr(action))
    <ActionForfeit>
    >>> print(action)
    Forfeit
    """

    def __init__(self):
        super().__init__(Action.FORFEIT)

    def __repr__(self):
        return '<ActionForfeit>'

    def __str__(self):
        return uncolor(self.colored())

    def colored(self):
        return PrintColor.RED_BOLD + 'Forfeit' + PrintColor.RESET


if __name__ == '__main__':
    my_action = ActionForfeit()
    print('repr: ', repr(my_action))
    print('str: ', str(my_action))
    print('colored: ', my_action.colored())

    import doctest
    doctest.testmod()

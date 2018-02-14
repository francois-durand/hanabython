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


class PrintColor:
    """
    An ANSI escape code that modifies the printing color
    """

    #: ANSI code used to return to the default color.
    RESET = "\033[0;0m"
    #: ANSI code for blue
    BLUE = "\033[0;94m"
    #: ANSI code for cyan
    CYAN = "\033[1;96m"
    #: ANSI code for green
    GREEN = "\033[0;32m"
    #: ANSI code for magenta
    MAGENTA = "\033[0;35m"
    #: ANSI code for red
    RED = "\033[0;31m"
    #: ANSI code for white
    WHITE = "\033[0;30m"
    #: ANSI code for yellow
    YELLOW = "\033[0;93m"

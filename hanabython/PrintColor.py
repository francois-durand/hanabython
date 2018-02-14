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

    :attr RESET:    ANSI code to return to the default color.
    :attr BLUE:     blue.
    :attr CYAN:     cyan.
    :attr GREEN:    green.
    :attr MAGENTA:  magenta.
    :attr RED:      red.
    :attr WHITE:    white (actually it's white on black background, and black
        on white background).
    :attr YELLOW:   yellow.
    """

    RESET = "\033[0;0m"
    BLUE = "\033[0;94m"
    CYAN = "\033[1;96m"
    GREEN = "\033[0;32m"
    MAGENTA = "\033[0;35m"
    RED = "\033[0;31m"
    WHITE = "\033[0;30m"
    YELLOW = "\033[0;93m"

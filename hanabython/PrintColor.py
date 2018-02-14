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

    #: This escape code is special: it is used to return to the default color.
    RESET = "\033[0;0m"

    #: This should be white on black background, and vice-versa.
    WHITE_NOT_BRIGHT = "\033[0;30m"
    WHITE_BRIGHT = "\033[0;90m"
    WHITE = WHITE_NOT_BRIGHT
    #:
    RED_NOT_BRIGHT = "\033[0;31m"
    RED_BRIGHT = "\033[0;91m"
    RED = RED_NOT_BRIGHT
    #:
    GREEN_NOT_BRIGHT = "\033[0;32m"
    GREEN_BRIGHT = "\033[0;92m"
    GREEN = GREEN_NOT_BRIGHT
    #:
    YELLOW_NOT_BRIGHT = "\033[0;33m"
    YELLOW_BRIGHT = "\033[0;93m"
    YELLOW = YELLOW_BRIGHT
    BROWN = YELLOW_NOT_BRIGHT
    #:
    BLUE_NOT_BRIGHT = "\033[0;34m"
    BLUE_BRIGHT = "\033[0;94m"
    BLUE = BLUE_BRIGHT
    #:
    MAGENTA_NOT_BRIGHT = "\033[0;35m"
    MAGENTA_BRIGHT = "\033[0;95m"
    MAGENTA = MAGENTA_NOT_BRIGHT
    #:
    CYAN_NOT_BRIGHT = "\033[1;36m"
    CYAN_BRIGHT = "\033[1;96m"
    CYAN = CYAN_BRIGHT


if __name__ == '__main__':
    for k in PrintColor.__dict__.keys():
        if not k.startswith('_'):
            print(PrintColor.__dict__[k] + k + PrintColor.RESET)

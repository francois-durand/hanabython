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
import PrintColor


class Color:
    r"""
    A Color.

    :param str name: The full name of the color.
    :param str symbol: The short name of the color.
    :param str print_color: an ANSI escape code that modifies the printing
        color. See the constants in module PrintColor.

    >>> BLUE.name
    'Blue'
    >>> BLUE.symbol
    'B'
    >>> BLUE.print_color
    '\x1b[0;94m'
    """

    def __init__(self, name: str, symbol: str, print_color: str):
        self.name = name
        self.symbol = symbol
        self.print_color = print_color

    def color_repr(self, o: object) -> str:
        r"""
        Convert an object to a colored representation

        :param object o: any object.

        :return: the ``__repr__`` of this object, with an ANSI color-modifying
            escape code at the beginning and its cancellation at the end.

        >>> BLUE.color_repr('some text')
        "\x1b[0;94m'some text'\x1b[0;0m"
        >>> BLUE.color_repr('42')
        "\x1b[0;94m'42'\x1b[0;0m"
        """
        return self.print_color + repr(o) + PrintColor.RESET

    def color_str(self, o: object) -> str:
        r"""
        Convert an object to a colored string

        :param object o: any object.

        :return: the ``__str__`` of this object, with an ANSI color-modifying
            escape code at the beginning and its cancellation at the end.

        >>> BLUE.color_str('some text')
        '\x1b[0;94msome text\x1b[0;0m'
        >>> BLUE.color_str('42')
        '\x1b[0;94m42\x1b[0;0m'
        """
        return self.print_color + str(o) + PrintColor.RESET

    def print(self, o: object) -> None:
        r"""
        Print an object in color

        :param object o: any object.

        :return: None. Prints the object in color.
        """
        print(self.color_str(o))

    def __repr__(self) -> str:
        return self.color_str(
            '%s (%s)' % (self.name, self.symbol))


BLUE = Color(name='Blue', symbol='B', print_color=PrintColor.BLUE)
GREEN = Color(name='Green', symbol='G', print_color=PrintColor.GREEN)
RED = Color(name='Red', symbol='R', print_color=PrintColor.RED)
WHITE = Color(name='White', symbol='W', print_color=PrintColor.WHITE)
YELLOW = Color(name='Yellow', symbol='Y', print_color=PrintColor.YELLOW)
MULTI = Color(name='Multi', symbol='M', print_color=PrintColor.CYAN)


if __name__ == '__main__':
    print(BLUE)
    print(GREEN)
    print(RED)
    print(WHITE)
    print(YELLOW)
    print(MULTI)
    print([BLUE, GREEN])

    import doctest
    doctest.testmod()

    print(Color.__doc__)

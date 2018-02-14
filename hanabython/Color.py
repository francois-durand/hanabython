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
from PrintColor import PrintColor


class Color:
    r"""
    A color

    :param str name: The full name of the color.
    :param str symbol: The short name of the color.
    :param str print_color: an ANSI escape code that modifies the printing
        color. See :class:`PrintColor`.

    >>> Color.BLUE.name
    'Blue'
    >>> Color.BLUE.symbol
    'B'
    >>> Color.BLUE.print_color
    '\x1b[0;94m'
    """

    def __init__(self, name, symbol, print_color):
        self.name = name
        self.symbol = symbol
        self.print_color = print_color

    def color_repr(self, o):
        r"""
        Convert an object to a colored representation

        :param object o: any object.

        :return: the ``__repr__`` of this object, with an ANSI color-modifying
            escape code at the beginning and its cancellation at the end.
        :rtype: str

        >>> Color.BLUE.color_repr('some text')
        "\x1b[0;94m'some text'\x1b[0;0m"
        >>> Color.BLUE.color_repr('42')
        "\x1b[0;94m'42'\x1b[0;0m"
        """
        return self.print_color + repr(o) + PrintColor.RESET

    def color_str(self, o):
        r"""
        Convert an object to a colored string

        :param object o: any object.

        :return: the ``__str__`` of this object, with an ANSI color-modifying
            escape code at the beginning and its cancellation at the end.
        :rtype: str

        >>> Color.BLUE.color_str('some text')
        '\x1b[0;94msome text\x1b[0;0m'
        >>> Color.BLUE.color_str('42')
        '\x1b[0;94m42\x1b[0;0m'
        """
        return self.print_color + str(o) + PrintColor.RESET

    def __repr__(self):
        return 'Color(name=%r, symbol=%r, print_color=%r)' % (
            self.name, self.symbol, self.print_color)

    def __str__(self):
        return self.color_str('%s (%s)' % (self.name, self.symbol))

    # The actual definitions of the following constants are outside the class.
    #:
    BLUE = None
    #:
    GREEN = None
    #:
    RED = None
    #:
    WHITE = None
    #:
    YELLOW = None
    #: Use this for multicolor cards (the actual color might change in future
    #: implementations).
    MULTICOLOR = None
    #: Use this for the sixth color (the actual color might change in future
    #: implementations).
    SIXTH = None
    #: Use this for the seventh color (the actual color might change in future
    #: implementations).
    SEVENTH = None


Color.BLUE = Color(name='Blue', symbol='B', print_color=PrintColor.BLUE)
Color.GREEN = Color(name='Green', symbol='G', print_color=PrintColor.GREEN)
Color.RED = Color(name='Red', symbol='R', print_color=PrintColor.RED)
Color.WHITE = Color(name='White', symbol='W', print_color=PrintColor.WHITE)
Color.YELLOW = Color(name='Yellow', symbol='Y', print_color=PrintColor.YELLOW)
Color.MULTICOLOR = Color(
    name='Multicolor', symbol='M', print_color=PrintColor.CYAN)
Color.SIXTH = Color(
    name='Pink', symbol='P', print_color=PrintColor.MAGENTA)
Color.SEVENTH = Color(
    name='Dark', symbol='D', print_color=PrintColor.BROWN)


if __name__ == '__main__':
    print(Color.BLUE)
    print(Color.SEVENTH)
    print(Color.GREEN)
    print(Color.SIXTH)
    print(Color.RED)
    print(Color.WHITE)
    print(Color.YELLOW)
    print(Color.MULTICOLOR)
    print([Color.BLUE, Color.GREEN])

    import doctest
    doctest.testmod()

    print(Color.__doc__)

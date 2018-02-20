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
from hanabython.Classes.Colored import Colored
from hanabython.Classes.StringAnsi import StringAnsi
from hanabython.Classes.ColorClueBehavior import ColorClueBehavior


class Color(Colored):
    r"""
    A color in Hanabi.

    :param str name: The full name of the color. In a game, two distinct
        colors must have different names.
    :param str symbol: The short name of the color. For standard colors
        (defined as constants in this class), it is always 1 character, and
        no two standard colors have the same symbol. For user-defined colors,
        it is recommended to do the same, but not necessary.
    :param str print_color: an ANSI escape code that modifies the printing
        color. See :class:`StringAnsi`.
    :param ColorClueBehavior clue_behavior: how this color behaves regarding
        color clues.

    >>> Color.BLUE.name
    'Blue'
    >>> Color.BLUE.symbol
    'B'
    >>> Color.BLUE.print_color
    '\x1b[94m'
    >>> Color.BLUE.clue_behavior == ColorClueBehavior.NORMAL
    True
    >>> Color.MULTICOLOR.clue_behavior == ColorClueBehavior.MULTICOLOR
    True
    """

    def __init__(self, name:str, symbol, print_color,
                 clue_behavior=ColorClueBehavior.NORMAL):
        self.name = name
        self.symbol = symbol
        self.print_color = print_color
        self.clue_behavior = clue_behavior

    @classmethod
    def from_symbol(cls, s):
        """
        Find one of the standard colors from its symbol.

        :param str s: the symbol of the color.

        :return: the corresponding color. It must be one of the constants
            defined in the class Color, e.g. :attr:`BLUE`, :attr:`MULTICOLOR`,
            etc.
        :rtype: Color

        >>> my_color = Color.from_symbol('B')
        >>> print(my_color.name)
        Blue
        """
        for k in Color.__dict__.keys():
            try:
                symbol = Color.__dict__[k].symbol
            except AttributeError:
                continue
            if symbol == s:
                return Color.__dict__[k]
        raise ValueError('Could not find color with symbol: ', s)

    def colored(self):
        return self.color_str(self.symbol)

    def color_str(self, o) -> str:
        r"""
        Convert an object to a colored string.

        :param object o: any object.

        :return: the ``__str__`` of this object, with an ANSI color-modifying
            escape code at the beginning and its cancellation at the end.
        :rtype: str

        >>> Color.BLUE.color_str('some text')
        '\x1b[94msome text\x1b[0;0m'
        >>> Color.BLUE.color_str(42)
        '\x1b[94m42\x1b[0;0m'
        """
        return self.print_color + str(o) + StringAnsi.RESET

    def match(self, clue_color):
        """
        React to a color clue.

        :param Color clue_color: the color of the clue.

        :return: whether a card of the current color should react to a clue of
            color :attr:`clue_color`.
        :rtype: bool

        >>> Color.BLUE.match(clue_color=Color.BLUE)
        True
        >>> Color.BLUE.match(clue_color=Color.RED)
        False
        >>> Color.MULTICOLOR.match(clue_color=Color.BLUE)
        True
        >>> Color.COLORLESS.match(clue_color=Color.BLUE)
        False
        """
        if self.clue_behavior == ColorClueBehavior.MULTICOLOR:
            return True
        if self.clue_behavior == ColorClueBehavior.COLORLESS:
            return False
        return self.name == clue_color.name

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
    #: Use this for the sixth color. As of now, it is brown but the display
    #: color might change in future implementations).
    SIXTH = None
    #: Use this for multicolor cards. As of now, it is cyan but the display
    #: color might change in future implementations).
    MULTICOLOR = None
    #: Use this for the colorless cards. As of now, it is pink but the display
    #: color might change in future implementations).
    COLORLESS = None


Color.BLUE = Color(name='Blue', symbol='B', print_color=StringAnsi.BLUE)
Color.GREEN = Color(name='Green', symbol='G', print_color=StringAnsi.GREEN)
Color.RED = Color(name='Red', symbol='R', print_color=StringAnsi.RED)
Color.WHITE = Color(name='White', symbol='W', print_color=StringAnsi.WHITE)
Color.YELLOW = Color(name='Yellow', symbol='Y', print_color=StringAnsi.YELLOW)
Color.SIXTH = Color(name='Pink', symbol='P', print_color=StringAnsi.MAGENTA)
Color.MULTICOLOR = Color(
    name='Multicolor', symbol='M',
    print_color=(
        StringAnsi.CYAN + StringAnsi.STYLE_BOLD + StringAnsi.STYLE_UNDERLINE),
    clue_behavior=ColorClueBehavior.MULTICOLOR
)
Color.COLORLESS = Color(
    name='Colorless', symbol='C',
    print_color=(
        StringAnsi.RED + StringAnsi.STYLE_BOLD + StringAnsi.STYLE_UNDERLINE),
    clue_behavior=ColorClueBehavior.COLORLESS
)


if __name__ == '__main__':
    Color.BLUE.test_str()

    my_color = Color.from_symbol('B')
    print('\n' + my_color.colored())
    try:
        my_color = Color.from_symbol('Z')
        print(my_color.colored())
    except ValueError as e:
        print(e)

    print('\n' + Color.BLUE.colored())
    print(Color.GREEN.colored())
    print(Color.RED.colored())
    print(Color.WHITE.colored())
    print(Color.YELLOW.colored())
    print(Color.SIXTH.colored())
    print(Color.MULTICOLOR.colored())
    print(Color.COLORLESS.colored())

    print(Color.__doc__)

    import doctest
    doctest.testmod()

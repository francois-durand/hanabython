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
class ColorClueBehavior:
    """
    A type of behavior regarding color clues.
    """

    #: Normal behavior (you can clue this color, and the card catches only the
    #: clues of its own color).
    NORMAL = 0
    #: Multicolor behavior (you cannot clue this color, and the card catches the
    #: clues of all colors).
    MULTICOLOR = 1
    #: Colorless behavior (you cannot clue this color, and the card catches the
    #: clues of no color).
    COLORLESS = 2

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


class MyClass2:
    """A whatever-you-are-doing.

    :param Number a: the `a` of the system.
    :param int|float b: the `b` of the system.

    >>> my_object = MyClass2(a = 5, b = 3)
    """

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def addition(self):
        """
        Add :attr:`a` and :attr:`b`

        :return: :attr:`a` + :attr:`b`.
        :rtype: Number

        >>> my_object = MyClass2(a=5, b=3)
        >>> my_object.addition()
        8
        """
        return self.a + self.b


if __name__ == '__main__':
    print('Do some little tests here')
    test = MyClass2(a=42, b=51)
    print(test.addition())

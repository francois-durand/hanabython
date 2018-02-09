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

    :ivar a: something that can be added, subtracted, etc.
        It is the `a` of the system.
    :ivar b: something that can be added, subtracted, etc.
        It is the `b` of the system.

    >>> my_object = MyClass2(a = 4, b = 3)
    """

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def addition(self):
        """
        Add :attr:`a` and :attr:`b`

        :return: the sum.

        >>> my_object = MyClass2(a = 4, b = 3)
        >>> my_object.addition()
        7
        """
        return self.a + self.b

    def subtraction(self):
        """
        Subtract :attr:`b` from :attr:`a`

        :return: the difference.

        >>> my_object = MyClass2(a = 4, b = 3)
        >>> my_object.subtraction()
        1
        """
        return self.a - self.b

    def multiplication(self):
        """
        Multiply :attr:`a` and :attr:`b`

        :return: the multiplication.

        >>> my_object = MyClass2(a = 4, b = 3)
        >>> my_object.multiplication()
        12
        """
        return self.a * self.b

    def _auxiliary_function(self):
        """
        Divide :attr:`a` by :attr:`b`

        :return: the division.

        >>> my_object = MyClass2(a = 6, b = 3)
        >>> # noinspection PyProtectedMember
        >>> my_object._auxiliary_function()
        2
        """
        return self.a // self.b


if __name__ == '__main__':
    print('Do some little tests here')
    test = MyClass2(a=42, b=51)
    print(test.addition())

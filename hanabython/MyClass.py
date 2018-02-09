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


class MyClass:
    """A whatever-you-are-doing.

    :ivar a: something that can be added, subtracted, etc.
        It is the `a` of the system.
    :ivar b: something that can be added, subtracted, etc.
        It is the `b` of the system.

    Note: document the :meth:`__init__` method in the docstring of the class
    itself, because the docstring of the :meth:`__init__` method does not
    appear in the documentation.

    A hyperlink to a method: :meth:`add_a_and_c`.

    A hyperlink to an attribute: :attr:`a` and :attr:`w`.

    >>> my_object = MyClass(a = 4, b = 3)
    """

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def addition(self):
        """
        Add :attr:`~hanabython.MyClass.a` and :attr:`~hanabython.MyClass.b`

        :return: the sum.

        >>> my_object = MyClass(a = 4, b = 3)
        >>> my_object.addition()
        7
        """
        return self.a + self.b

    def subtraction(self):
        """
        Subtract :attr:`~hanabython.MyClass.b` from
        :attr:`~hanabython.MyClass.a`

        :return: the difference.

        >>> my_object = MyClass(a = 4, b = 3)
        >>> my_object.subtraction()
        1
        """
        return self.a - self.b

    def add_a_and_c(self, c):
        """
        Subtract :attr:`~hanabython.MyClass.a` and something

        :param c: something that can be added.

        :return: py:attr:`~hanabython.MyClass.a` + :param:`c`

        >>> my_object = MyClass(a = 4, b = 3)
        >>> my_object.add_a_and_c(c = 2)
        6
        """
        return self.a + c


if __name__ == '__main__':
    print('Do some little tests here')
    test = MyClass(a=42, b=51)
    print(test.addition())

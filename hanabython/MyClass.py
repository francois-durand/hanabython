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
    :attr my_string: a nice string.

    Note: document the :meth:`__init__` method in the docstring of the class
    itself, because the docstring of the :meth:`__init__` method does not
    appear in the documentation.

    Refer to a class this way: :class:`MyClass2`.

    Refer to a method this way: :meth:`addition`.

    Refer to a method in another class: :meth:`MyClass2.addition`.

    Refer to an attribute this way: :attr:`a`.

    >>> my_object = MyClass(a = 4, b = 3)
    """

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.my_string = 'My string'

    def addition(self):
        """
        Add :attr:`a` and :attr:`b`

        :return: the sum.

        >>> my_object = MyClass(a = 4, b = 3)
        >>> my_object.addition()
        7
        """
        return self.a + self.b

    def subtraction(self):
        """
        Subtract :attr:`b` from :attr:`a`

        :return: the difference.

        >>> my_object = MyClass(a = 4, b = 3)
        >>> my_object.subtraction()
        1
        """
        return self.a - self.b

    def add_a_and_c(self, c):
        """
        Add :attr:`a` and something

        :param c: something that can be added.

        :return: :attr:`a` + :data:`c`

        >>> my_object = MyClass(a = 4, b = 3)
        >>> my_object.add_a_and_c(c = 2)
        6
        """
        return self.a + c


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print('Do some little tests here')
    test = MyClass(a=42, b=51)
    print(test.addition())

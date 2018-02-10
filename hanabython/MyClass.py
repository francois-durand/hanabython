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

    :param Number a: the `a` of the system. Must be nonnegative.
    :param int|float b: the `b` of the system.

    :var str my_string: a nice string.

    :raise ValueError: if :attr:`a` is negative.

    Note: document the :meth:`__init__` method in the docstring of the class
    itself, because the docstring of the :meth:`__init__` method does not
    appear in the documentation.

    * Refer to a class this way: :class:`MyClass2`.
    * Refer to a method this way: :meth:`addition`.
    * Refer to a method in another class: :meth:`MyClass2.addition`.
    * Refer to an parameter or variable this way: :attr:`a`.

    >>> my_object = MyClass(a=5, b=3)
    """

    def __init__(self, a, b):
        if a < 0:
            raise ValueError('Expected nonnegative a, got: ', a)
        self.a = a
        self.b = b
        self.my_string = 'a = %s and b = %s' % (a, b)

    def divide_a_by_c_and_add_d(self, c, d):
        """
        Divide :attr:`a` by something and add something else

        :param Number c: a non-zero number. If you want to say many
            things about this parameter, it is good practice to indent the
            following lines, like this.
        :param d: a beautiful number.
        :type d: a type specified differently.

        :return: :attr:`a` / :attr:`c` + :attr:`d`.
        :rtype: Number

        :raise ZeroDivisionError: if :attr:`c` = 0.

        This function gives an example of Sphinx documentation with typical
        features.

        >>> my_object = MyClass(a=5, b=3)
        >>> my_object.divide_a_by_c_and_add_d(c=2, d=10)
        12.5
        """
        return self.a / c + d

    def addition(self):
        """
        Add :attr:`a` and :attr:`b`

        :return: :attr:`a` + :attr:`b`.
        :rtype: Number

        >>> my_object = MyClass(a=5, b=3)
        >>> my_object.addition()
        8
        """
        return self.a + self.b

    def _secret_function(self):
        """
        Give :attr:`b`

        :return: :attr:`b`.
        :rtype: Number

        Since the name of this function starts with _, it does not appear in
        the Sphinx documentation.

        >>> my_object = MyClass(a=5, b=3)
        >>> my_object._secret_function()
        3
        """
        return self.b


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print('Do some little tests here')
    test = MyClass(a=42, b=51)
    print(test.addition())

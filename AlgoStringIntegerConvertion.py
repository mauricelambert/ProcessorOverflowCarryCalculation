#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    POC: string/integerconversation
#    Copyright (C) 2022  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
Algorithm for string/integer convertion.

https://stackoverflow.com/questions/7123490/how-compiler-is-converting-integer-to-string-and-vice-versa
Mark Ransom and APerson
"""

from string import digits

ZERO_CHAR: int = ord('0')
CHAR_CODES: dict[str, int] = {i: ord(i) for i in digits}
CODE_CHARS: dict[int, str] = {int(k): k for k in CHAR_CODES.keys()}

def string_to_int(s: str) -> int:
    """
    Convert string to integer.
    >>> string_to_int("1234567890")
    123
    >>>
    """
    i = 0
    sign = 1
    if s[0] == '-':
        sign = -1
        s = s[1:]
    for c in s:
        if not ('0' <= c <= '9'):
            raise ValueError
        i = 10 * i + CHAR_CODES[c] - ZERO_CHAR
    return sign * i

def int_to_string(i: int) -> str:
    """
    Convert integer to string.
    >>> int_to_string(1234567890)
    '1234567890'
    >>>
    """
    s = ''
    sign = ''
    if i < 0:
        sign = '-'
        i = -i
    while i != 0:
        remainder = i % 10
        i //= 10
        s = CODE_CHARS[remainder] + s
    return sign + s

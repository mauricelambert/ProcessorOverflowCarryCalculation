#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    POC: pseudo random numbers generator
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
This module generates pseudo random numbers.
"""

from dataclasses import dataclass
from time import time
from sys import exit

@dataclass
class State:

	_0: int
	_1: int


def xorshift128p(state: State, max_: int = 1000) -> int:

	"""
	This function generates pseudo random numbers.
	"""

	_0 = state._0
	_1 = state._1
	state._0 = _1

	_0 ^= _0 << 23
	_0 ^= _0 >> 18
	_0 ^= _1 ^ (_1 >> 5)

	state._1 = _0

	return (_0 + _1) % max_

def random(max_: int = 1000) -> int:

	"""
	This function generates pseudo random numbers.
	"""

	global state
	return xorshift128p(state, max_)


def test(_0: int, _1: int) -> None:

	"""
	This function prints pseudo random numbers.
	"""

	state = State(_0, _1)
	print(xorshift128p(state))
	print(xorshift128p(state))
	print(xorshift128p(state))
	print(xorshift128p(state))

global state
t = int(time() * 10000000)
state: State = State(t, id(t))

if __name__ == "__main__":
	print([random() for x in range(5)])
	print("Pseudo random:")
	test(t, id(t))
	print("Not random init:")
	test(64, 256)
	print("Replay precedent:")
	test(64, 256)
	exit(0)
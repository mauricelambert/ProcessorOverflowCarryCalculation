#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    POC: crash a python script with thread deadlock
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

from threading import Semaphore, Thread
from time import sleep

# Create 2 threads and 2 shared values
# First thread take the first shared value and sleep
# Second thread take the second value and sleep
# First take the second value (first is blocked because second value is blocked by the second process)
# Second take the first value (second is blocked because first value is blocked by the first process)
# Don't crash

def task(semaphore1: Semaphore, semaphore2: Semaphore):
    # attempt to acquire the semaphore
    print("Acquire Semaphore1")
    with semaphore1:
        print("Waiting...")
        sleep(5)
        print("Acquire Semaphore2...")
        semaphore2.acquire(blocking=True)
        print("Release Semaphore2")
        semaphore2.release()
        print('Pass')
    print("Release Semaphore2")

semaphore1 = Semaphore(2)
semaphore2 = Semaphore(2)

thread1 = Thread(target=task, args=(semaphore1, semaphore2))
thread2 = Thread(target=task, args=(semaphore2, semaphore1))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

'''
Acquire Semaphore1
Waiting...
Acquire Semaphore1
Waiting...
Acquire Semaphore2...
Release Semaphore2
Pass
Release Semaphore2
Acquire Semaphore2...
Release Semaphore2
Pass
Release Semaphore2
'''

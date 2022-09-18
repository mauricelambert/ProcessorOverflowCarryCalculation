#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    POC: crash a python script with multiprocess deadlock
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

from multiprocessing import Semaphore, Process
from time import sleep

# Create 2 process and 2 shared values
# First process take the first shared value and sleep
# Second process take the second value and sleep
# First take the second value (first is blocked because second value is blocked by the second process)
# Second take the first value (second is blocked because first value is blocked by the first process)
# Crash

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

process1 = Process(target=task, args=(semaphore1, semaphore2))
process2 = Process(target=task, args=(semaphore2, semaphore1))

process1.start()
process2.start()

process1.join()
process2.join()

'''
Traceback (most recent call last):
Traceback (most recent call last):
  File "/usr/lib/python3.10/multiprocessing/process.py", line 314, in _bootstrap
    self.run()
  File "/usr/lib/python3.10/multiprocessing/process.py", line 314, in _bootstrap
    self.run()
  File "/usr/lib/python3.10/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "/usr/lib/python3.10/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "test_DOS_blocked_process_share_value.py", line 17, in task
    semaphore2.acquire(blocking=True)
  File "test_DOS_blocked_process_share_value.py", line 17, in task
    semaphore2.acquire(blocking=True)
TypeError: 'blocking' is an invalid keyword argument for acquire()
TypeError: 'blocking' is an invalid keyword argument for acquire()
'''

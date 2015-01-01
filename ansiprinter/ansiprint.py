#!/usr/bin/env python2.7
from __future__ import print_function

import io
import os
import sys

def showart(filename):
    with io.open(filename, encoding='cp437', errors='ignore') as source:
        for line in source:
            print(line, end='')

showart(sys.argv[1])

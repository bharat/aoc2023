#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
from pprint import pprint
from functools import cmp_to_key, cache
from itertools import product

def load():
    acc = []
    m = []
    for line in [x.strip() for x in sys.stdin]:
        if line:
            m.append(line)
        else:
            acc.append(m)
            m = []
    acc.append(m)
    return acc


def transpose(m):
    m_2d = [[x for x in l] for l in m]
    return ["".join(x) for x in np.transpose(m_2d)]


def vsplit(m):
    for i in range(len(m)):
        if i + 1 == len(m):
            return None

        if m[i] == m[i+1]:
            left = m[i::-1]
            right = m[i+1:]
            if not False in [x == y for x, y in zip(left, right)]:
                return i+1


def hsplit(m):
    return vsplit(transpose(m))


def pm(m, r=None, c=None):
    if not c is None:
        print("  ", " " * c, "><")
    for i, row in enumerate(m):
        pfx = " "
        if not r is None:
            if i == r-1:
                pfx = "v"
            elif i == r:
                pfx = "^"
        print("%-2d" % (i), pfx, row, pfx, i+1)
    if not c is None:
        print("  ", " " * c, "><")


def main():
    maps = load()

    acc = 0
    for m in maps:
        r = vsplit(m)
        c = hsplit(m)
        pm(m, r=r, c=c)

        if r:
            acc += r * 100
        elif c:
            acc += c
        else:
            pprint(('error', r, c))
            pm(m)
            sys.exit(1)
        print('')

    pprint(acc)

if __name__ == "__main__":
    main()

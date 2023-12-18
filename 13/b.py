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


def delta(str1, str2):
    return sum(1 for c1, c2 in zip(str1, str2) if c1 != c2)


def vsplit(m):
    #pm(m)
    for i in range(len(m)):
        #pprint(('check', i))
        if i + 1 == len(m):
            return None

        if delta(m[i], m[i+1]) <= 1:
            #pprint(('match at', i, 'and', i+1, m[i]))

            left = m[i::-1]
            right = m[i+1:]
            deltas = [delta(x, y) for x, y in zip(left, right)]
            # pprint(('left and right', [(x, y) for x, y in zip(left, right)], deltas))
            if sum(deltas) == 1:
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
        # pm(m, r=r, c=c)

        if r:
            acc += r * 100
        elif c:
            acc += c
        else:
            pprint(('error', r, c))
            pm(m)
            sys.exit(1)

    pprint(acc)

if __name__ == "__main__":
    main()

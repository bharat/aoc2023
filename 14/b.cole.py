#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
from pprint import pprint
from functools import cmp_to_key, cache
from itertools import product

def load():
    return np.array([[c for c in x.strip()] for x in sys.stdin])


def pm(m):
    cnt = len(m)
    for i, row in enumerate(m):
        print(row, "%-2d" % (cnt-i))
    print('')


def compact(r):
    groups = r.split("#")
    for i, g in enumerate(groups):
        o_cnt = g.count("O")
        groups[i] = "O" * o_cnt + "." * (len(g) - o_cnt)
    return "#".join(groups)


def tilt_left(m):
    for i, r in enumerate(m):
        row = "".join(r)
        row = compact(row)
        m[i] = [c for c in row]
    return m


def score(map):
    acc = 0
    for i, r in enumerate(map):
        acc += r.count('O') * (len(map) - i)
    return acc


def tilt_next(map):
    np.rot90(map, k=-1)
    map = tilt_left(map)
    return map


def main():
    map = load()
    pm(map)
    print('')


    for cycle in range(3):
        pprint(('prime', cycle))
        map = np.rot90(map, k=1)
        pm(map)

        for i in range(4):
            pprint('tilt_next')
            map = tilt_next(map)

        #undo prime
        map = np.rot90(map, k=1)

        pm(map)

    pm(map)


    #s = score(map)
    #print(s)

if __name__ == "__main__":
    main()

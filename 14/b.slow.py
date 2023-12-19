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


def score(map):
    acc = 0
    for i, r in enumerate(map):
        s = "".join(r)
        acc += s.count('O') * (len(map) - i)
    return acc

def tilt_up(map):
    m = np.transpose(map)
    for i in range(len(m)):
        m[i] = [c for c in compact("".join(m[i]))]
    m = np.transpose(m)
    return m


def tilt_right(map):
    m = np.rot90(map)
    m = tilt_up(m)
    m = np.rot90(m, k=-1)
    return m


def tilt_down(map):
    m = np.flipud(map)
    m = tilt_up(m)
    m = np.flipud(m)
    return m


def tilt_left(map):
    m = np.rot90(map, k=-1)
    m = tilt_up(m)
    m = np.rot90(m)
    return m


def main():
    map = load()
    pm(map)
    print('')

    for cycle in range(1000000000):
        if cycle % 1000 == 0:
            print(cycle)

        map = tilt_up(map)
        map = tilt_left(map)
        map = tilt_down(map)
        map = tilt_right(map)

    pm(map)

    s = score(map)
    print(s)

if __name__ == "__main__":
    main()

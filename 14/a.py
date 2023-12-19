#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
from pprint import pprint
from functools import cmp_to_key, cache
from itertools import product

def load():
    return [x.strip() for x in sys.stdin]


def pm(m):
    cnt = len(m)
    for i, row in enumerate(m):
        print(row, "%-2d" % (cnt-i))


def transpose(m):
    m_2d = [[x for x in l] for l in m]
    return ["".join(x) for x in np.transpose(m_2d)]


def compact(r):
    groups = r.split("#")
    for i, g in enumerate(groups):
        o_cnt = g.count("O")
        groups[i] = "O" * o_cnt + "." * (len(g) - o_cnt)
    return "#".join(groups)


def tilt(m):
    m = transpose(m)
    for i in range(len(m)):
        m[i] = compact(m[i])
    return transpose(m)


def score(map):
    acc = 0
    for i, r in enumerate(map):
        acc += r.count('O') * (len(map) - i)
    return acc


def main():
    map = load()
    #pm(map)
    map = tilt(map)
    pm(map)
    s = score(map)
    print(s)

if __name__ == "__main__":
    main()

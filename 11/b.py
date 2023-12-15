#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
from pprint import pprint
from functools import cmp_to_key
from itertools import product
from math import copysign

def load():
    lines = [x.strip() for x in sys.stdin]
    map = [[c for c in x] for x in lines]
    return map


def calc_idx(rows):
    idx = []
    for i, row in enumerate(rows):
        if '#' in row:
            idx.append(1)
        else:
            idx.append(1000000)
    return idx


def transpose(arr):
    return [list(row) for row in zip(*arr)]


def expand(map):
    r_idx = calc_idx(map)
    c_idx = calc_idx(transpose(map))
    return r_idx, c_idx


def find_galaxies(map):
    gs = []
    for y, row in enumerate(map):
        for x, c in enumerate(row):
            if c == '#':
                gs.append((y, x))
    return gs


def pairings(values):
    pairings = [tuple(sorted((x, y))) for x in values for y in values if x != y]
    return list(set(pairings))


def distance(pair, r_idx, c_idx):
    a, b = pair

    r_step = int(copysign(1, b[0] - a[0]))
    c_step = int(copysign(1, b[1] - a[1]))

    r_d = [r_idx[r] for r in list(range(a[0], b[0], r_step))]
    c_d = [c_idx[c] for c in list(range(a[1], b[1], c_step))]

    return sum(r_d) + sum(c_d)


def main():
    map = load()

    r_idx, c_idx = expand(map)
    gs = find_galaxies(map)
    pairs = pairings(gs)
    distances = [distance(pair, r_idx, c_idx) for pair in pairs]

    print(sum(distances))


if __name__ == "__main__":
    main()

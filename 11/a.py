#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
from pprint import pprint
from functools import cmp_to_key
from itertools import product

def load():
    lines = [x.strip() for x in sys.stdin]
    map = [[c for c in x] for x in lines]
    return map


def expand_empty_rows(rows):
    new_rows = []
    for row in rows:
        new_rows.append(row)
        if '#' not in row:
            new_rows.append(row)
    return new_rows


def transpose(arr):
    return [list(row) for row in zip(*arr)]


def expand(map):
    new_map = expand_empty_rows(map)
    new_map = transpose(expand_empty_rows(transpose(new_map)))
    return new_map


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


def distance(pair):
    a, b = pair
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def main():
    map = load()
    #pprint(map)
    #print('')

    map = expand(map)
    #pprint(map)

    gs = find_galaxies(map)
    #pprint(gs)

    pairs = pairings(gs)
    #pprint(len(pairs))

    distances = [distance(pair) for pair in pairs]
    #pprint(distances)

    print(sum(distances))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
import heapq
from pprint import pprint
from functools import cmp_to_key, cache
from itertools import product
import hashlib

LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

ALL_DIRS = [DOWN, RIGHT, LEFT, UP]

def tuple_add(a, b):
    return a[0] + b[0], a[1] + b[1]


def load():
    return [[int(c) for c in l.strip()] for l in sys.stdin]

costmap = {}

def show(map, path):
    dirs = {
        UP: "^",
        LEFT: "<",
        RIGHT: ">",
        DOWN: "v",
    }

    out = [[[0, " "] for e in r] for r in map]
    for (y, x, dir, consec), c in costmap.items():
        e = out[y][x]
        if e[0] == 0 or c < e[0]:
            e[0] = c

    for y, x, dir in path.trail:
        out[y][x][1] = dirs[dir]

    for y, row in enumerate(out):
        for x, cell in enumerate(row):
            print(cell[0] % 10, end='')
        print('')


class Path:
    def __init__(self, y, x, dir, consec=1, trail=[]):
        self.y = y
        self.x = x
        self.dir = dir
        self.consec = consec
        self.trail = trail[:]
        self.trail.append((self.y, self.x, self.dir))

    def walk(self, map):
        acc = []
        key = (self.y, self.x, self.dir, self.consec)
        cost = costmap[key] if key in costmap else 0

        for ndir in ALL_DIRS:
            if tuple_add(self.dir, ndir) == (0, 0):  # can't reverse dir
                continue

            ny, nx = tuple_add((self.y, self.x), ndir)
            if ny not in range(len(map)) or nx not in range(len(map[1])):
                continue

            nconsec = self.consec + 1 if self.dir == ndir else 1
            if nconsec > 3:
                continue

            ncost = cost + map[ny][nx]
            nkey = (ny, nx, ndir, nconsec)

            if nkey not in costmap or ncost < costmap[nkey]:
                costmap[nkey] = ncost
                acc.append(Path(ny, nx, ndir, nconsec, self.trail))

        return acc

    def __str__(self):
        return f"Path<y,x={(self.y, self.x)}, dir={self.dir}, consec={self.consec}>"

    def __repr__(self):
        return self.__str__()


def main():
    map = load()

    paths = [Path(0, 0, RIGHT, 0)]
    target = (len(map)-1, len(map[0])-1)

    i = 0
    while paths:
        i += 1
        p = paths.pop(0)
        if (p.y, p.x) == target:
            print(costmap[(p.y, p.x, p.dir, p.consec)])
            quit()

        paths.extend(p.walk(map))
        paths.sort(key=lambda p: costmap[(p.y, p.x, p.dir, p.consec)])
        if i % 10000 == 0:
            print(i, len(paths))

    print('')
    for (y, x, dir, consec), c in costmap.items():
        if not (y == target[0] and x == target[1]):
            continue
        print(c)


if __name__ == "__main__":
    main()
# 851

#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
from pprint import pprint
from functools import cmp_to_key, cache
from itertools import product
import hashlib

LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

def tuple_add(a, b):
    return a[0] + b[0], a[1] + b[1]

class Beam:
    def __init__(self, loc, dir):
        self.loc = loc
        self.dir = dir
        pass

    def move(self):
        return Beam((self.loc[0] + self.dir[0], self.loc[1] + self.dir[1]), self.dir)

    def up(self):
        return tuple_add(self.loc, UP)

    def down(self):
        return tuple_add(self.loc, DOWN)

    def left(self):
        return tuple_add(self.loc, LEFT)

    def right(self):
        return tuple_add(self.loc, RIGHT)

    def __str__(self):
        return f"Beam<loc={self.loc}>, dir={self.dir}>"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Beam) and self.loc == other.loc and self.dir == other.dir

    def __hash__(self):
        return hash((self.loc, self.dir))

class Cell:
    def __init__(self, ch):
        self.ch = ch
        self.energized = False

    def __str__(self):
        if self.energized:
            return "#"
        else:
            return f"{self.ch}"

    def __repr__(self):
        return self.__str__()


def pm(map):
    for row in map:
        for cell in row:
            print(cell, end="")
        print("")
    print("")


def load():
    return [[Cell(c) for c in line.strip()] for line in sys.stdin]


def walk(map, b):
    y, x = b.loc
    if not y in range(len(map)) or not x in range(len(map[0])):
        return []

    c = map[y][x]
    c.energized = True

    if c.ch == '.' or \
       (c.ch == '-' and b.dir in [LEFT, RIGHT]) or \
       (c.ch == '|' and b.dir in [UP, DOWN]):
        return [b.move()]
    elif c.ch == "|":
        return [Beam(b.up(), UP), Beam(b.down(), DOWN)]
    elif c.ch == '-':
        return [Beam(b.left(), LEFT), Beam(b.right(), RIGHT)]
    elif c.ch == '\\':
        if b.dir == UP: return [Beam(b.left(), LEFT)]
        if b.dir == DOWN: return [Beam(b.right(), RIGHT)]
        if b.dir == LEFT: return [Beam(b.up(), UP)]
        if b.dir == RIGHT: return [Beam(b.down(), DOWN)]
    elif c.ch == '/':
        if b.dir == UP: return [Beam(b.right(), RIGHT)]
        if b.dir == DOWN: return [Beam(b.left(), LEFT)]
        if b.dir == LEFT: return [Beam(b.down(), DOWN)]
        if b.dir == RIGHT: return [Beam(b.up(), UP)]

def main():
    map = load()

    all_beams = [Beam((0, x), DOWN) for x in range(len(map[0]))] + \
        [Beam((len(map)-1, x), UP) for x in range(len(map[0]))] + \
        [Beam((y, 0), RIGHT) for y in range(len(map))] + \
        [Beam((y, len(map[0])-1), LEFT) for y in range(len(map))]
    acc = []

    for beam in all_beams:
        seen = {}
        beams = [beam]

        for row in map:
            for c in row:
                c.energized = False

        while beams:
            b = beams.pop(0)
            seen[b] = 1
            beams.extend([b for b in walk(map, b) if b not in seen])

        s = sum([sum([int(c.energized) for c in row]) for row in map])
        acc.append((s, b))

    acc = sorted(acc, key=lambda x: x[0])
    pprint(acc[-1][0])

if __name__ == "__main__":
    main()

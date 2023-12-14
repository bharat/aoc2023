#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
from pprint import pprint
from functools import cmp_to_key

# y/x transform
txf = {
        '.': [[0,  0], [0,  0]],
        '-': [[0, -1], [0, +1]],
        '7': [[0, -1], [+1, 0]],
        '|': [[-1, 0], [+1, 0]],
        'J': [[-1, 0], [0, -1]],
        'L': [[-1, 0], [0, +1]],
        'F': [[+1, 0], [0, +1]],
        'S': [[0,  0], [0,  0]],
}

box = {
    'L': '└', # '┗',
    'J': '┘', # '┛',
    'F': '┌', # '┏',
    '7': '┐', # '┓',
    '-': '─', # '━',
    '|': '│', # '┃',
}

UNKNOWN = 0
ON_PATH = 1
INSIDE = 2
OUTSIDE = 3

LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3


class Grid:
    def __init__(self, y, x):
        self.max_y = y - 1
        self.max_x = x - 1
        self.grid = [[None for _ in range(x)] for _ in range(y)]

    def add_cell(self, ch, y, x):
        self.grid[y][x] = Cell(self, ch, y, x)

    def at(self, y, x):
        return self.grid[y][x]

    def rows(self):
        return self.grid


class Cell:
    def __init__(self, grid, ch, y, x):

        self.cross = None
        self.grid = grid
        self.ch = ch
        self.y = y
        self.x = x
        self.t = UNKNOWN
        self.distance = None
        self.scanned = False
        self.inside_or_outside = None
        self.n = None

    def neighbors(self):
        if self.n is None:
            off1, off2 = txf[self.ch][0], txf[self.ch][1]
            y, x = self.y, self.x
            self.n = [
                self.grid.at(off1[0] + y, off1[1] + x),
                self.grid.at(off2[0] + y, off2[1] + x)
            ]
        return self.n

    def left(self):
        if self.x == 0:
            return None
        return self.grid.at(self.y, self.x-1)

    def right(self):
        if self.x >= self.grid.max_x:
            return None
        return self.grid.at(self.y, self.x+1)

    def above(self):
        if self.y == 0:
            return None
        return self.grid.at(self.y-1, self.x)

    def below(self):
        if self.y >= self.grid.max_y:
            return None
        return self.grid.at(self.y+1, self.x)

    def __str__(self):
        if self.n is None:
            n_yx = None
        else:
            n_yx = [(n.y, n.x) for n in self.n]
        return f"Cell({self.ch}, [{self.y}, {self.x}], {self.t}, {self.distance}, {self.scanned}, n={n_yx}"

    def __repr__(self):
        return self.__str__()


def pg(grid, highlight=None, distance=False):
    # os.system('clear')
    print('')
    #if highlight != None:
    #  pprint(('highlight', highlight))
    for y, row in enumerate(grid.rows()):
        print(f" {y % 10} ", end="")
        for x, cell in enumerate(row):
            ch = cell.ch
            if ch in box:
                ch = box[ch]

            if highlight == cell:
                print('*', end="")
            elif cell.t == ON_PATH:
                if distance:
                    print(cell.distance % 10, end="")
                else:
                    print(ch, end="")
            elif cell.t == OUTSIDE:
                print('O', end="")
            elif cell.t == INSIDE:
                print(cell.cross%10, end="")
            elif cell.t == UNKNOWN:
                print(ch, end="")
            else:
                raise 'unknown'
        print("")

    print("")
    print("   ", end="")
    for x in range(0, len(grid.rows()[0])):
        print(x % 10, end="")
    print("")
    print("")

def load():
    lines = [x.strip() for x in sys.stdin]

    grid = Grid(len(lines), len(lines[0]))
    for y, l in enumerate(lines):
        for x, ch in enumerate(l):
            grid.add_cell(ch, y, x)

    for y, row in enumerate(grid.rows()):
        for x, cell in enumerate(row):
            if cell.ch == 'S':
                cell.t = ON_PATH
                cell.distance = 0
                cell.n = []
                start = cell

    if start.left() != None and start in start.left().neighbors():
        if start.above() != None and start in start.above().neighbors():
            start.n = [start.left(), start.above()]
            start.ch = 'J'
        else:
            start.n = [start.left(), start.below()]
            start.ch = '7'
    else:
        if start.above() != None and start in start.above().neighbors():
            start.n = [start.left(), start.above()]
            start.ch = 'L'
        else:
            start.n = [start.left(), start.below()]
            start.ch = 'F'

    return start, grid


def walk_path(lvl, cells):
    new_cells = []
    for cell in cells:
        for n in cell.neighbors():
            if not n.scanned:
                n.scanned = True
                n.t = ON_PATH
                n.distance = lvl+1
                new_cells.append(n)
    return new_cells


def calc_inside(grid):
    for y in range(len(grid.rows())):
        cross = 0
        for x in range(len(grid.rows()[0])):
            c = grid.at(y, x)
            c.cross = cross
            if c.t == ON_PATH:
                # our point of reference is the top left corner of the cell
                if c.ch not in ['.', '-', 'F', '7']:
                    cross += 1
            else:
                c.t = [OUTSIDE, INSIDE][cross % 2]

def main():
    start, grid = load()
    pg(grid, highlight=start)

    level = 0
    cells = [start]
    while True:
        cells = walk_path(level, cells)
        if len(cells) > 0:
            level += 1
        else:
            break

    pg(grid)
    calc_inside(grid)
    pg(grid)

    inside_cnt = 0
    for r in grid.rows():
        for c in r:
            if c.t == INSIDE:
                inside_cnt += 1

    print('Inside: ', inside_cnt)

if __name__ == "__main__":
    main()

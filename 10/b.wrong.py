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

        self.grid = grid
        self.ch = ch
        self.y = y
        self.x = x
        self.t = UNKNOWN
        self.distance = None
        self.scanned = False
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

    def can_squeeze_by(self, n, sides):
        if n == self.above():
            if self.ch == '-' and BOTTOM in sides: return None
            if n.ch == 'J': return [BOTTOM, RIGHT]
            if n.ch == 'L': return [BOTTOM, LEFT]
            if n.ch == '|':
                if LEFT in sides: return [LEFT]
                if RIGHT in sides: return [RIGHT]
            if n.ch == '7' and RIGHT in sides: return [TOP, RIGHT]
            if n.ch == 'F' and LEFT in sides: return [TOP, LEFT]
            if n.ch == '.': return [TOP, BOTTOM, LEFT, RIGHT]
            return None

        if n == self.left():
            if self.ch == '|' and RIGHT in sides: return None
            if n.ch == '7': return [TOP, RIGHT]
            if n.ch == 'J': return [BOTTOM, RIGHT]
            if n.ch == '-':
                if TOP in sides: return [TOP]
                if BOTTOM in sides: return [BOTTOM]
            if n.ch == 'F' and TOP in sides: return [TOP, LEFT]
            if n.ch == 'L' and BOTTOM in sides: return [BOTTOM, LEFT]
            if n.ch == '.': return [TOP, BOTTOM, LEFT, RIGHT]
            return None

        if n == self.right():
            if self.ch == '|' and LEFT in sides: return None
            if n.ch == 'F': return [TOP, LEFT]
            if n.ch == 'L': return [BOTTOM, LEFT]
            if n.ch == '-':
                if TOP in sides: return [TOP]
                if BOTTOM in sides: return [BOTTOM]
            if n.ch == '7' and TOP in sides: return [TOP, RIGHT]
            if n.ch == 'J' and BOTTOM in sides: return [BOTTOM, RIGHT]
            if n.ch == '.': return [TOP, BOTTOM, LEFT, RIGHT]
            return None

        if n == self.below():
            if self.ch == '-' and TOP in sides: return None
            if n.ch == 'F': return [TOP, LEFT]
            if n.ch == '7': return [TOP, RIGHT]
            if n.ch == '|':
                if LEFT in sides: return [LEFT]
                if RIGHT in sides: return [RIGHT]
            if n.ch == 'J' and RIGHT in sides: return [BOTTOM, RIGHT]
            if n.ch == 'L' and LEFT in sides: return [BOTTOM, LEFT]
            if n.ch == '.': return [TOP, BOTTOM, LEFT, RIGHT]
            return None

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
                print('I', end="")
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

    for cell in [start.left(), start.right(), start.above(), start.below()]:
        if cell is None:
            continue
        if start in cell.neighbors():
            start.n.append(cell)

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


def remove_outside(cells):
    new_cells = []
    for cell, sides in cells:
        # print(('check cell', cell))
        if not cell.t == ON_PATH:
            cell.scanned = True
            cell.t = OUTSIDE
            #pprint(('outside', cell))

        for n in [cell.above(), cell.below(), cell.right(), cell.left()]:
            if n is None: continue
            if n.scanned: continue
            n.scanned = True
            if cell.t == ON_PATH or n.t == ON_PATH:
                ns = cell.can_squeeze_by(n, sides)
                #pprint(('squeeze', cell, sides, n, ns))
                if ns != None:
                    new_cells.append((n, ns))
                continue
            #pprint(('add neighbor', cell, n))
            new_cells.append((n, [TOP, BOTTOM, LEFT, RIGHT]))
    return new_cells


def unscan(grid):
    for row in grid.rows():
        for cell in row:
            cell.scanned = False


def main():
    start, grid = load()
    pg(grid)

    level = 0
    cells = [start]
    unscan(grid)
    while True:
        cells = walk_path(level, cells)
        if len(cells) > 0:
            level += 1
        else:
            break
    pg(grid, distance=True)
    print('Max distance: ', level)

    # for row in grid.rows():
    #     for cell in row:
    #         if cell.t != ON_PATH:
    #             cell.ch = '.'
    # pg(grid)

    cells = [(x, [TOP, BOTTOM, LEFT, RIGHT]) for x in [grid.at(0, 0), grid.at(0, -1), grid.at(-1, 0), grid.at(-1, -1)]]
    unscan(grid)
    while True:
        cells = remove_outside(cells)
        if len(cells) == 0:
            break
    pg(grid)

    inside_cnt = 0
    for row in grid.rows():
        for cell in row:
            if not cell.t in [ON_PATH, OUTSIDE]:
                cell.t = INSIDE
                inside_cnt += 1

    pg(grid)
    print('Inside: ', inside_cnt)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
from pprint import pprint
from functools import cmp_to_key

# y/x transform
txf = {
        '.': [[0, 0],  [0, 0]],
        '-': [[0, -1], [0, +1]],
        '7': [[0, -1], [+1, 0]],
        '|': [[-1, 0], [+1, 0]],
        'J': [[-1, 0], [0, -1]],
        'L': [[-1, 0], [0, +1]],
        'F': [[+1, 0], [0, +1]],
        'S': [[0, 0],  [0, 0]],
}

def pg(grid):
    os.system('clear')
    for row in grid:
        for n in row:
            if n[0] == -1:
                print(n[1], end="")
            else:
                print(n[0] % 10, end="")
        print('')
    print('')

def load():
    lines = [x.strip() for x in sys.stdin]
    grid = [[txf[x] for x in l] for l in lines]
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            g = grid[y][x]
            grid[y][x] = [-1, c, [g[0][0]+y, g[0][1]+x], [g[1][0]+y, g[1][1]+x]]

    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == 'S':
                start = [y, x]
                grid[y][x] = [0, c]
                for ny, row in enumerate(grid):
                    for nx, ts in enumerate(row):
                        if [y, x] in ts:
                            grid[y][x].append([ny, nx])

    return start, grid


def walk_grid(lvl, locs, grid):
    new_locs = []
    for loc in locs:
        g = grid[loc[0]][loc[1]]
        for yx in [g[2], g[3]]:
            if grid[yx[0]][yx[1]][0] == -1:
                grid[yx[0]][yx[1]][0] = lvl+1
                new_locs.append(yx)

    return new_locs, grid


def main():
    start, grid = load()
    pg(grid)

    level = 0
    cur = [start]
    while True:
        cur, grid = walk_grid(level, cur, grid)
        if level % 1000 == 0:
            pg(grid)
        if len(cur) > 0:
            level += 1
        else:
            break

    print(level)

if __name__ == "__main__":
    main()

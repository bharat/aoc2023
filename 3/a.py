#!/usr/bin/env python3

import sys
import re
from pprint import pprint

def load_schematic():
    schematic = []
    for line in [x.strip() for x in sys.stdin]:
        schematic.append(line)
    return schematic


def find_symbols(s):
    syms = []
    for y, row in enumerate(s):
        for x, col in enumerate(row):
            c = s[y][x]
            if not c.isdigit() and not c == '.' and not c == '|':
                syms.append((y, x))
    return syms


def get_neighbors(len_y, len_x, sym):
    n = []
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dy == dx == 0:
                continue
            ny = sym[0] + dy
            nx = sym[1] + dx
            if ny > -1 and ny < len_y and nx > -1 and nx < len_x:
                n.append((ny, nx))
    return n


def is_digit_at(s, pos):
    return s[pos[0]][pos[1]].isdigit()


def extract_num_at(s, len_x, pos):
    y = pos[0]
    start_x = pos[1]
    end_x = pos[1]
    while start_x > 0 and is_digit_at(s, (y, start_x - 1)):
        start_x -= 1

    while end_x < len_x and is_digit_at(s, (y, end_x)):
        end_x += 1

    num = s[y][start_x:end_x]
    s[y] = s[y][:start_x] + '|' * (end_x - start_x) + s[y][end_x:]

    return (s, num)


def get_nums(s, syms):
    len_x = len(s)
    len_y = len(s[0])
    nums = []
    for sym in syms:
        for n in get_neighbors(len_y, len_x, sym):
            #pprint(("neighbor", n))
            if is_digit_at(s, n):
                s, num = extract_num_at(s, len_x, n)
                nums.append(int(num))
                #print('extracted %s' % num)
                #pprint(s)
    return (s, nums)


def main():
    s = load_schematic()
    #pprint(s)
    syms = find_symbols(s)
    #pprint(syms)

    new_s, nums = get_nums(s, syms)
    #pprint(nums)
    #print()
    #pprint(new_s)
    print(sum(nums))

if __name__ == "__main__":
    main()

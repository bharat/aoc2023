#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
from pprint import pprint
from functools import cmp_to_key, cache
from itertools import product
import hashlib

def load():
    return sys.stdin.readline().strip().split(',')


def hash(str):
    acc = 0
    for c in str:
        acc += ord(c)
        acc *= 17
        acc %= 256
    return acc


def pm(boxes):
    for i, b in enumerate(boxes):
        if len(b):
            print(f"Box {i}: {b}")


def score(boxes, h, l):
    for i, b in enumerate(boxes[h]):
        if b[0] == l:
            return (h + 1) * (i + 1) * b[1]
    return 0


def main():
    seq = load()
    #pprint(seq)

    lenses = {}
    boxes = [[] for x in range(256)]
    for s in seq:
        m = re.match(r"(.*)([-=])(.*)", s)
        label, action, value = m.groups()
        h = hash(label)
        lenses[label] = h
        if action == '-':
            boxes[h] = [b for b in boxes[h] if b[0] != label]
        else:
            found = False
            for i, b in enumerate(boxes[h]):
                if b[0] == label:
                    boxes[h][i] = (label, int(value))
                    found = True
                    break
            if not found:
                boxes[h].append((label, int(value)))

    acc = 0
    for l, h in lenses.items():
        s = score(boxes, h, l)
        acc += s
        # pprint((boxes[h], l, s))

    print(acc)
    # pm(boxes)

if __name__ == "__main__":
    main()

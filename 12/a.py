#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
from pprint import pprint
from functools import cmp_to_key
from itertools import product

class Record:
    def __init__(self, line):
        l = line.split(' ')
        self.springs = l[0]
        self.groups = [int(x) for x in l[1].split(',')]

    def __str__(self):
        return f"springs: {self.springs}, groups: {self.groups}"

    def __repr__(self):
        return self.__str__()


def expand(lvl, lines):
    acc = []
    while True:
        if len(lines) == 0:
            break
        line = lines.pop(0)
        try:
            i = line.index('?')
            for c in ['.', '#']:
                lines.append(line[:i] + c + line[i+1:])
        except ValueError:
            acc.append(line)

    return acc


def score(springs):
    return [len(y) for y in [x for x in springs.split('.') if x]]


def load():
    lines = [x.strip() for x in sys.stdin]
    return [Record(l) for l in lines]


def main():
    records = load()
    pprint(records)

    total = 0
    for record in records:
        pprint(('record', record))
        candidates = expand(0, [record.springs])
        scores = [score(c) for c in candidates]
        scores = [s for s in scores if s == record.groups]
        total += len(scores)

    print(total)

if __name__ == "__main__":
    main()

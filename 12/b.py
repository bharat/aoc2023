#!/usr/bin/env python3

import sys
import re
import os
import numpy as np
from pprint import pprint
from functools import cmp_to_key, cache
from itertools import product

def load():
    lines = [x.strip() for x in sys.stdin]
    return [(l.split(' ')[0], eval(l.split(' ')[1])) for l in lines]


@cache
def score(springs, groups):
    if not groups:
        return 0 if "#" in springs else 1
    if not springs:
        return 1 if not groups else 0

    acc = 0
    g = groups[0]
    if springs[0] in ".?":
        acc += score(springs[1:], groups)
    if springs[0] in "#?":
        if g <= len(springs):
            if "." not in springs[:g]:
                if g == len(springs) or springs[g] != "#":
                    acc += score(springs[g+1:], groups[1:])
    return acc


def main():
    records = load()
    pprint(records)

    total = 0
    for springs, groups in records:
        total += score("?".join([springs] * 5), groups * 5)

    print(total)

if __name__ == "__main__":
    main()

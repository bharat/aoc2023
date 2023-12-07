#!/usr/bin/env python3

import sys
import re
from pprint import pprint

def load():
    lines = [x.strip() for x in sys.stdin]

    times = [int(x) for x in re.findall('(\d+)', lines[0])]
    distances = [int(x) for x in re.findall('(\d+)', lines[1])]

    return [x for x in zip(times, distances)]


def win(race):
    t = race[0]
    d = race[1]

    all_d = [i * (t - i) for i in range(t+1)]
    better_d = [i for i in all_d if i > d]
    return len(better_d)


def main():
    races = load()
    acc = 1
    for r in races:
        acc *= win(r)
    print(acc)

if __name__ == "__main__":
    main()

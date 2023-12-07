#!/usr/bin/env python3

import sys
import re
from pprint import pprint

def load():
    lines = [x.strip() for x in sys.stdin]
    lines = [l.replace(" ", "") for l in lines]
    t = int(re.findall('(\d+)', lines[0])[0])
    d = int(re.findall('(\d+)', lines[1])[0])
    return t, d


def win(t, d):
    all_d = [i * (t - i) for i in range(t+1)]
    better_d = [i for i in all_d if i > d]
    return len(better_d)


def main():
    t, d = load()
    r = win(t, d)
    pprint(r)

if __name__ == "__main__":
    main()

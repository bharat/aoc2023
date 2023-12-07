#!/usr/bin/env python3

import sys
import re
from pprint import pprint
from functools import cmp_to_key

def load():
    lines = [x.strip() for x in sys.stdin]
    hands = []
    for l in lines:
        h, b = l.split(' ')
        hands.append((h, int(b)))
    return hands


def val(c):
    lookup = { 'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10 }
    if c in lookup:
        return lookup[c]
    return int(c)


def score_hab(hab):
    hand = hab[0]
    hist = {}
    for c in hand:
        if c not in hist:
            hist[c] = 0
        hist[c] += 1

    j = 0
    if 'J' in hist:
        j = hist['J']
        del hist['J']

    if j == 5 or j + max(hist.values()) == 5:
        ret = 7
    elif j + max(hist.values()) == 4:
        ret = 6
    elif len(hist.values()) == 2: # full house
        ret = 5
    elif j + max(hist.values()) == 3:
        ret = 4
    elif j > 1 or (2 in hist.values() and len(hist.values()) == 3): # 2 pairs
        ret = 3
    elif j == 1 or len(hist.values()) == 4:
        ret = 2
    else:
        ret = 1

    ret = [ret] + [val(c) for c in hand]
    return ret


def main():
    hands_and_bids = load()

    sorted_hands_and_bids = sorted(hands_and_bids, key=score_hab)

    acc = 0
    for i, hab in enumerate(sorted_hands_and_bids):
        acc += ((i + 1) * hab[1])

    print(acc)

if __name__ == "__main__":
    main()

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
    lookup = { 'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10 }
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

    if 5 in hist.values():
        ret = 7
    elif 4 in hist.values():
        ret = 6
    elif 3 in hist.values() and 2 in hist.values():
        ret = 5
    elif 3 in hist.values():
        ret = 4
    elif 2 in hist.values():
        if len(hist.values()) == 3:
            ret = 3
        else:
            ret = 2
    else:
        ret = 1

    ret = [ret] + [val(c) for c in hand]
    return ret


def main():
    hands_and_bids = load()
    # pprint(hands_and_bids)

    sorted_hands_and_bids = sorted(hands_and_bids, key=score_hab)
    #pprint(sorted_hands_and_bids)

    acc = 0
    for i, hab in enumerate(sorted_hands_and_bids):
        acc += ((i + 1) * hab[1])

    print(acc)

if __name__ == "__main__":
    main()

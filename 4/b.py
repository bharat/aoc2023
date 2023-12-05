#!/usr/bin/env python3

import sys
import re
from pprint import pprint

def load():
    cards = []
    for line in [x.strip() for x in sys.stdin]:
        m = [re.findall('(\d+)', l) for l in line.split('|')]
        id = int(m[0][0])
        winning = set([int(i) for i in m[0][1:]])
        have = set([int(i) for i in m[1]])
        cards.append((id, winning, have))
    return cards


def process(cards, active):
    #print("proc")
    acc = []
    for card in active:
        intersect = card[1] & card[2]
        cnt = len(intersect)
        for i in range(0, len(intersect)):
            acc.append(cards[card[0] + i])

    #pprint(('acc is ', acc))
    return acc


def main():
    cards = load()

    active = cards
    count = 0
    while len(active) > 0:
        #pprint(active)
        count += len(active)
        active = process(cards, active)

    print(count)

if __name__ == "__main__":
    main()

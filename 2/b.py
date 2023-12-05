#!/usr/bin/env python3

import sys
import re
from pprint import pprint

def load_games():
    game = {}
    for line in [x.strip() for x in sys.stdin]:
        #print(line)
        id = int(re.match('Game (\d+)', line)[1])
        game[id] = []
        for draw in line.split(';'):
            acc = {'red': 0, 'blue': 0, 'green': 0}
            for m in re.findall('(\d+) (blue|red|green)', draw):
                acc[m[1]] += int(m[0])
            game[id].append(acc)
    return game


def find_mins(games):
    mins = []
    for id, game in games.items():
        acc = game[0]
        for draw in game:
            for x in ['green', 'red', 'blue']:
                acc[x] = max(acc[x], draw[x])
        mins.append(acc)
    return mins


def calc_pows(mins):
    return [x['green'] * x['red'] * x['blue'] for x in mins]


def main():
    games = load_games()
    mins = find_mins(games)
    #pprint(mins)
    pows = calc_pows(mins)
    #pprint(pows)
    print(sum(pows))

if __name__ == "__main__":
    main()

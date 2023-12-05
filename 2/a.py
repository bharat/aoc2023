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


def sub_game(a, b):
    return {'red': a['red'] - b['red'], 'green': a['green'] - b['green'], 'blue': a['blue'] - b['blue']}


def find_matches(games, pattern):
    matches = []
    for id, game in games.items():
        deltas = [sub_game(pattern, draw) for draw in game]
        #pprint(deltas)
        bad = [any([v < 0 for v in delta.values()]) for delta in deltas]
        #pprint(bad)
        if not any([value is True for value in bad]):
            matches.append(id)
    return matches

def main():
    games = load_games()

    matches = find_matches(games, {'red': 12, 'green': 13, 'blue': 14})
    pprint(sum(matches))

if __name__ == "__main__":
    main()

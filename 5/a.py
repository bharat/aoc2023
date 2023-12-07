#!/usr/bin/env python3

import sys
import re
from pprint import pprint

def load():
    map = {}
    lines = [x.strip() for x in sys.stdin]

    seeds = [int(x) for x in re.findall('(\d+)', lines[0])]
    lines = lines[2:]

    for line in lines:
        if 'map' in line:
            a_to_b = re.findall('(\w+)-to-(\w+) ', line)[0]
            a = a_to_b[0]
            b = a_to_b[1]
            if a not in map:
                map[a] = {}
            if b not in map[a]:
                map[a][b] = []
        elif len(line):
            s = line.split(' ')
            (d_start, s_start, cnt) = (int(s[0]), int(s[1]), int(s[2]))
            map[a][b].append((range(s_start, s_start+cnt-1), range(d_start, d_start+cnt-1)))
    return (seeds, map)


def get(map, seed, keys):
    while len(keys) > 1:
        a = keys.pop(0)
        b = keys[0]
        for (s, d) in map[a][b]:
            if s.start <= seed <= s.stop:
                #pprint((seed, s, d, seed - s.start))
                seed = d.start + seed - s.start
                break
        #pprint((seed, a, b))
    return seed

def main():
    (seeds, map) = load()
    #pprint((seeds, map))

    best = 1E15
    for seed in seeds:
        loc = get(map, seed, ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location'])
        #print(loc)
        best = min(best, loc)

    print(best)

if __name__ == "__main__":
    main()

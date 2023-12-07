#!/usr/bin/env python3

import sys
import re
from pprint import pprint

def load():
    map = {}
    lines = [x.strip() for x in sys.stdin]

    seeds = []
    raw = [int(x) for x in re.findall('(\d+)', lines[0])]
    for i in range(0, len(raw), 2):
        seeds.append(range(raw[i], raw[i] + raw[i+1]))

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
            map[a][b].append((range(s_start, s_start+cnt), range(d_start, d_start+cnt)))
    return (seeds, map)


def get_intersect(seed, transform):
    src = transform[0]
    dst = transform[1]
    offset = dst.start - src.start

    start_intersect = max(seed.start, src.start)
    stop_intersect = min(seed.stop, src.stop)

    if start_intersect < stop_intersect:
        src_intersection = range(start_intersect, stop_intersect)
        intersection = range(start_intersect + offset, stop_intersect + offset)

        nir_1 = nir_2 = None
        if seed.start < start_intersect:
            nir_1 = range(seed.start, start_intersect)
        if seed.stop > stop_intersect:
            nir_2 = range(stop_intersect, seed.stop)
        return intersection, nir_1, nir_2
    else:
        return None, None, None


def transform_seeds(seeds, map, a_to_b):
    acc = []
    while len(seeds) > 0:
        s = seeds.pop(0)
        for txform in map[a_to_b[0]][a_to_b[1]]:
            inside, r1, r2 = get_intersect(s, txform)
            if inside != None:
                acc.append(inside)
                seeds = [x for x in [r1, r2] + seeds if x is not None]
                s = False
                break
        if s:
            acc.append(s)
    return acc


def main():
    (seeds, map) = load()

    best = 1E15
    for a_to_b in [('seed', 'soil'), ('soil', 'fertilizer'), ('fertilizer', 'water'),
              ('water', 'light'), ('light', 'temperature'),
              ('temperature', 'humidity'), ('humidity', 'location')]:
        seeds = transform_seeds(seeds, map, a_to_b)

    print(min([x.start for x in seeds]))

if __name__ == "__main__":
    main()

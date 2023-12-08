#!/usr/bin/env python3

import sys
import re
import math
from pprint import pprint
from functools import cmp_to_key, reduce

def load():
    lines = [x.strip() for x in sys.stdin]
    cmds = list(lines.pop(0))
    lines.pop(0)

    nodes = {}
    for l in lines:
        m = re.findall('([A-Z0-9]{3})', l)
        nodes[m[0]] = (m[1], m[2])

    return cmds, nodes


def main():
    cmds, nodes = load()

    cnt = 0
    cur = [x for x in nodes.keys() if x[-1] == 'A']
    periods = [None for x in cur]
    while True:
        for c in cmds:
            if c == 'L':
                cur = [nodes[c][0] for c in cur]
            else:
                cur = [nodes[c][1] for c in cur]
            cnt += 1

            for i, c in enumerate(cur):
                if c[-1] == 'Z' and periods[i] == None:
                    periods[i] = cnt

        if not None in periods:
            break

    print(math.lcm(*periods))


if __name__ == "__main__":
    main()

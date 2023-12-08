#!/usr/bin/env python3

import sys
import re
from pprint import pprint
from functools import cmp_to_key

def load():
    lines = [x.strip() for x in sys.stdin]
    cmds = list(lines.pop(0))
    lines.pop(0)

    nodes = {}
    for l in lines:
        m = re.findall('([A-Z]{3})', l)
        nodes[m[0]] = (m[1], m[2])

    return cmds, nodes


def main():
    cmds, nodes = load()

    cnt = 0
    cur = 'AAA'
    while True:
        for c in cmds:
            if c == 'L':
                cur = nodes[cur][0]
            else:
                cur = nodes[cur][1]
            cnt += 1
            if cur == 'ZZZ':
                print(cnt)
                sys.exit(0)



if __name__ == "__main__":
    main()

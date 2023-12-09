#!/usr/bin/env python3

import sys
import re
import numpy as np
from pprint import pprint
from functools import cmp_to_key

def load():
    lines = [x.strip() for x in sys.stdin]
    return [[int(x) for x in l.split(' ')] for l in lines]


def main():
    seqs = load()
    # pprint(seqs)

    ans = 0
    for seq in seqs:
        ans += sum([np.diff(seq, i)[-1] for i in range(len(seq))])

    print(ans)


if __name__ == "__main__":
    main()

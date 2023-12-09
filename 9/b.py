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
        firsts = [np.diff(seq, i)[0] for i in range(len(seq))]
        #pprint(firsts)

        acc = 0
        for f in reversed(firsts):
            #pprint((f, '-', acc))
            acc = f - acc
            #pprint(acc)
        ans += acc

    print(ans)


if __name__ == "__main__":
    main()

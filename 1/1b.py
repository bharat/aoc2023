#!/usr/bin/env python3

import sys
import re
from pprint import pprint

subs = {
    'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
    'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
}

def sub_callback(match):
    return subs[match.group()]

def sub_callback_rev(match):
    return subs[match.group()[::-1]]

def main():
    pattern = '|'.join(subs.keys())
    acc = 0

    lines = [x.strip() for x in sys.stdin]

    for line in lines:
        fwd_line = re.sub(pattern, sub_callback, line, count=0)
        first = re.findall(r'\d', fwd_line)[0]

        rev_line = re.sub(pattern[::-1], sub_callback_rev, line[::-1], count=0)
        last = re.findall(r'\d', rev_line)[0]

        val = int("%s%s" % (first, last))
        # print(line, fwd_line, rev_line, first, last, val)
        acc += val

    print(acc)

if __name__ == "__main__":
    main()

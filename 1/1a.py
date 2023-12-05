#!/usr/bin/env python3

import sys
import re

def main():
    acc = 0
    for line in sys.stdin:
        digits = re.findall(r'\d', line)
        acc += int("%s%s" % (digits[0], digits[-1]))
    print(acc)

if __name__ == "__main__":
    main()

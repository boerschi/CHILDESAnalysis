#!/usr/bin/python

# to sort dictionaries, as gnu sort doesn't seem to match but python does

import sys

if __name__=="__main__":
    res = []
    for l in sys.stdin:
        res.append(l)
    res.sort()
    for l in res:
        print l.strip()

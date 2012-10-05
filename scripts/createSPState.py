#!/usr/bin/python
# 05/10/12
# author: boerschi@cl.uni-heidelberg.de
#
# creates a silence model, see HTK Tutorial p. 33

import sys

if __name__=="__main__":
    inF = sys.stdin
    isInSil = False
    isInState3 = False
    for l in inF:
        l = l.strip()
        if l.startswith("~h \"sil\""):
            isInSil = True
            print "~h \"sp\""
            print "<BEGINHMM>"
            print "<NUMSTATES> 3"
            continue
        if isInSil and not isInState3:
            if l == "<STATE> 3":
                print "<STATE> 2"
                isInState3 = True
                continue
        if isInSil and isInState3 and l.startswith("<STATE>"): #quit
            print "<TRANSP> 3"
            print "0 0.6 0.4"
            print "0 0.6 0.4"
            print "0 0 0"
            print "<ENDHMM>"
            break
        elif isInSil and isInState3:
            print l
        else:
            continue

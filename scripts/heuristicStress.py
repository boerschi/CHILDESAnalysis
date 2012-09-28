#!/usr/bin/python
#
# date: 28/09/12
# author: boerschi@cl.uni-heidelberg.de

# this just adds stress on the penultimate vowel in a word

import sys

vowels = "AA AE AH AO AW AY EH ER EY IH IY OW OY UH UW".split()

def nVowels(word):
    res = 0
    for w in word.split():
        if w in vowels:
            res += 1
    return res

def addStress(word):
    res = []
    nV = nVowels(word)
    if nV == 0:
        return word
    elif nV == 1:
        res = []
        for w in word.split():
            if w in vowels:
                res.append("%s1"%w)
            else:
                res.append(w)
        return " ".join(res)
    else:
        curV = 1
        tarV = nV-1 #penultimate vowel
        for w in word.split():
            if w in vowels:
                if curV == tarV:
                    res.append("%s1"%w)
                else:
                    res.append("%s0"%w)
                curV += 1
            else:
                res.append(w)
        return " ".join(res)

if __name__=="__main__":
    for l in sys.stdin:
        w,p = l.strip().split("\t")
        print("%s\t%s"%(w,addStress(p)))

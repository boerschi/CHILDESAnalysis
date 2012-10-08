#!/usr/bin/python
# -*- coding: utf-8 -*-
# this is a rather ugly script to get Miranda's hand-annotations into a consistent format

import xmlchat, codecs


def hasTime(x):
    return x.count(u"\x15")>0

def hasFinalT(x):
    for w in x.split():
        if w.endswith("t"):
            return True
    return False

def cleanedUp(x):
    return x.count("[")==0

def getRelevantMotherUtterances(f):
    #indexed from zero
    results = []
    takePhon=False
    plain=None
    for l in codecs.open(f,encoding="utf-8"):
        if l.startswith("@"):
            continue
        elif l.startswith("*MOT") and hasFinalT(l) and hasTime(l):
            plain=l.strip()
            takePhon=True
        elif l.startswith("%pho") and takePhon:
            if cleanedUp(l):
                results.append((plain,l.strip()))
            takePhon=False
            plain=None
        else:
            takePhon=False
    return results
            

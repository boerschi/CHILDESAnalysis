#!/usr/bin/python
#
# date: 28/09/12
# author: boerschi@cl.uni-heidelberg.de

# this script generates a full HMM from the proto-hmm generated by HTK
# (refer to the HTK tutorial for background, p. 30f)
# just pass the list of phones as first and the proto-hmm as second
# argument

import sys

#assume that protohmm begins with
#3 additional lines (~o, <STREAM..., <VECSIZE...), then ~h "proto"

if __name__=="__main__":
    phones = [x.strip() for x in open(sys.argv[1],"r")]
    header = [x.strip() for x in open(sys.argv[2],"r").readlines()[:3]]
    hmm = [x.strip() for x in open(sys.argv[2],"r").readlines()[4:]]
    for h in header:
        print h
    for phone in phones:
        print "~h \"%s\""%phone
        for l in hmm:
            print l

    

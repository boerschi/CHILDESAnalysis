#!/usr/bin/python
#
# date: 28/09/12
# author: boerschi@cl.uni-heidelberg.de

VECSIZE=39
CODING="PLP_D_A_Z_0"
STATES = [2,3,4] #start=1, end=5, can be ignored

protoHMMHeader = """~o <VecSize> %s <%s>
~h "proto"
"""%(VECSIZE,CODING)

#not sure, taken over from HTKBook, p.31
TRANSP = """    0.0 1.0 0.0 0.0 0.0
    0.0 0.6 0.4 0.0 0.0
    0.0 0.0 0.6 0.4 0.0
    0.0 0.0 0.0 0.7 0.3
    0.0 0.0 0.0 0.0 0.0"""

def protoHMMBody():
    print("<BeginHMM>")
    print("  <NumStates> 5")
    for s in STATES:
        print("  <State> %s"%s)
        print("    <Mean> 39")
        print("      %s"%" ".join([str(0.0) for x in xrange(VECSIZE)]))
        print("    <Variance> 39")
        print("      %s"%" ".join([str(1.0) for x in xrange(VECSIZE)]))
    print("  <TransP> 5")
    print(TRANSP)
    print("<EndHMM>")
    
if __name__=="__main__":
    print(protoHMMHeader)
    protoHMMBody()

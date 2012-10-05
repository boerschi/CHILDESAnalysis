#!/bin/bash
#
# usage: transcribeNoSP <label-file> <dict-file>

HTKCONF="/home/bborschi/research/CHILDESAnalysis/htkfiles"

HLEd -l '*' -d $2 -i phones0.mlf ${HTKCONF}/mkphones0.led $1
#!/bin/bash
#
# usage: transcribeNoSP <label-file> <dict-file>

HTKCONF="/home/bborschi/research/CHILDESAnalysis/htkfiles"

HLEd -l '*' -d $2 -i phones1.mlf ${HTKCONF}/mkphones1.led $1
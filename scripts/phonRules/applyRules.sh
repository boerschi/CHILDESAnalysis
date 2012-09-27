#!/bin/bash
#
# this generates a dictionary for a wordlist and applies phonological
# variation rules

WORDS=$1
DICT=$2
RULES=$3
OUT=$4
OUTTMP=${OUT}"_tmp"

# first pass, gets rid of original pronunciations
HDMan -w ${WORDS} -g ${RULES} -m ${OUTTMP} ${DICT}
# second pass, to add the original pronunciations
HDMan -w ${WORDS} -m ${OUT} ${OUTTMP} ${DICT}
#clean up
rm ${OUTTMP}

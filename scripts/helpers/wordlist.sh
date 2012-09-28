#!/bin/bash
#creates a wordlist from a master-label file
grep -v "^[.\"#]" $1 | less | sort | uniq

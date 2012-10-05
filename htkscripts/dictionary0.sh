#!/bin/bash
# 
# produces the first dictionary without "silence"
#
FOLDER=/home/bborschi/research/CHILDESAnalysis

CMU_MUL=${FOLDER}/dictionary/cmudict.0.7a_multiple
CMU_MAIN=${FOLDER}/dictionary/cmudict.0.7a_noComments
PROV=${FOLDER}/dictionary/providenceWords_heuristicStress
SCRIPT=${FOLDER}/htkfiles/global.ded


HDMan -w $1 -n monophones1 -g ${SCRIPT} -l dlog monophones0_single.dict ${CMU_MAIN} ${PROV}
HDMan -m -w $1 -n monophones1 -g ${SCRIPT} -l dlog monophones0_multiple.dict ${CMU_MUL} ${PROV}
echo "sil" >> monophones1
grep -v "^sp" monophones1 > monophones0
echo -e "silence\tsil" >> monophones0_single.dict
${FOLDER}/scripts/helpers/sort.py < monophones0_single.dict > monophones0.dict_sorted
mv monophones0.dict_sorted monophones0_single.dict
echo -e "silence\tsil" >> monophones0_multiple.dict
${FOLDER}/scripts/helpers/sort.py < monophones0_multiple.dict > monophones0.dict_sorted
mv monophones0.dict_sorted monophones0_multiple.dict
#!/bin/bash
#
# 04/10/12

SOUNDFILES=/media/8C56F47F56F46B7A/Users/bborschi/linuxdata/ProvidenceMedia/media/Eng-USA/Providence
XMLFILES=/home/bborschi/data/Providence
CHILD=Naima

HTKCONF=/home/bborschi/research/CHILDESAnalysis/htkfiles
HTKSCRIPTS=/home/bborschi/research/CHILDESAnalysis/htkscripts
SCRIPTS=/home/bborschi/research/CHILDESAnalysis/scripts

#echo "extracting wav-files and preparing transcripts"
#${SCRIPTS}/prepareFolder.py ${XMLFILES}/${CHILD} ${SOUNDFILES}/${CHILD}

##echo "converting wav-files to plp"
##mkdir -p plp
##for f in wav/*.wav
##do
##  filename=`basename ${f}`
##  echo "${f} plp/${filename%.wav}.plp" >> codetr.scp
##done
##HCopy -T 00001 -C ${HTKCONF}/config -S codetr.scp
echo "building lexicon"
grep -vP "^(#|\"|\.)" words.mlf | sort | uniq > wordlist
${HTKSCRIPTS}/dictionary0.sh wordlist
echo "transcribing label file"
${HTKSCRIPTS}/transcribeNoSP.sh words.mlf monophones0_single.dict
##ls plp/*.plp > train.scp
ls wav/*.wav > train.scp
echo "initializing monophone hmm"
${SCRIPTS}/buildProtoHMM.py > proto.hmm
mkdir -p hmm0
echo "estimating flat-parameters"
HCompV -C ${HTKCONF}/config -f 0.01 -m -S train.scp -M hmm0 proto.hmm
${SCRIPTS}/buildFullHMM.py monophones0 hmm0/proto > hmm0/hmmdefs
head -n3 hmm0/proto > hmm0/macros
cat hmm0/vFloors >> hmm0/macros
for i in 1 2 3
do
  echo "training hmm${i}"
  mkdir -p hmm${i}
  HERest -C ${HTKCONF}/config -I phones0.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm$[i-1]/hmmdefs -T 00001 -M hmm${i} monophones0 > tLog
done

echo "build silence model"
mkdir -p hmm4
cp hmm3/hmmdefs hmm4
${SCRIPTS}/createSPState.py < hmm3/hmmdefs >> hmm4/hmmdefs
mkdir -p hmm5
cp hmm0/macros hmm4/ #this seems redundant?!
HHEd -H hmm4/macros -H hmm4/hmmdefs -M hmm5 ${HTKSCRIPTS}/sil.hed monophones1

echo "prepare data with short-pauses" # --- don't get confused, monophones0_single.dict includes "sp"
${HTKSCRIPTS}/transcribeWithSP.sh words.mlf monophones0_single.dict
for i in 6 7
do
  echo "training hmm${i}"
  mkdir -p hmm${i}
  HERest -C ${HTKCONF}/config -I phones1.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm$[i-1]/hmmdefs -T 0001 -M hmm${i} monophones1 > tLog
done
cp hmm0/macros hmm7
echo "realign training data with multiple pronunciations"
#no pruning
HVite -l '*' -T 00001 -o SWT -b silence -C ${HTKCONF}/config -a -H hmm7/macros -H hmm7/hmmdefs -i aligned.mlf -m -y lab -I words.mlf -S train.scp monophones0_multiple.dict monophones1 > alignLog

echo "train on realigned data"
for i in 8 9
do
  echo "training hmm${i}"
  mkdir -p hmm${i}
  HERest -C ${HTKCONF}/config -I aligned.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm$[i-1]/hmmdefs -T 0001 -M hmm${i} monophones1 > tLog
done
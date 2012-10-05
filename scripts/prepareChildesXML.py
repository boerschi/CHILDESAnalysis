#!/usr/bin/python
#
# date: 28/09/12
# author: boerschi@cl.uni-heidelberg.de

"""prepareChildesXML.py is a module that prepares CHILDES xml-files for forced alignment"""

import xmlchat, sys, codecs, os, optparse

#minimum length in seconds
MINLENGTH=1.5
MAXLENGTH=30
ignoredLength=0

def writeUtterance(utterance,outF):
    outF.write("\"*/%s.lab\"\n"%(os.path.basename(utterance[1]).split(".")[0]))
    for w in utterance[0]:
        outF.write("%s\n"%(w.upper()))
    outF.write(".\n")


def generateLabelFile(transcripts,fileName="words.mlf"):
    """
    this generates an HTK master-label file, refer to HTK Book p.28 for more details
    """
    outF = codecs.open(fileName,"w",encoding="utf-8")
    outF.write("#!MLF!#\n")
    for transcript in transcripts:
        for utterance in transcript.transcriptions:
            writeUtterance(utterance,outF)
    outF.close()

def generateHCopyInput(transcripts,fileName="codetr.scp",outfolder="./"):
    """
    this generates an input-script for HCopy
    """
    outF = codecs.open(fileName,"w",encoding="utf-8")
    for transcript in transcripts:
        for utterance in transcript.transcriptions:
            fOut = os.path.join(outfolder,os.path.basename(utterance[1]).split(".")[0]+".plp")
            outF.write("%s.wav %s\n"%(utterance[1],fOut))
    outF.close()

class Transcript:
    def __init__(self,xmlFile,outFolder,soundFolder,speakers="MOT".split()):
        self.transcriptions = []
        self.outFolder = outFolder
        self.fName = os.path.basename(xmlFile).split(".")[0]
        self.xmlFile = xmlFile
        self.utterances = xmlchat.readfile(xmlFile)[1]
        self.speakers = speakers
        self.soundFile = os.path.join(soundFolder,self.fName)+".wav"

    def createAlignmentFiles(self):
        global ignoredLength
        os.system("mkdir -p %s"%os.path.join(self.outFolder,"wav"))
        for ut in self.utterances:
            if ut['who'] in self.speakers:
                if ut.has_key("start"):
                    utterance = Utterance(ut["start"],ut["end"]-ut["start"],ut["words"],ut["uID"])
                    if utterance.length < MINLENGTH or utterance.length > MAXLENGTH:
#                        sys.stderr.write("Ignored %s, length=%f\n"%(ut["uID"],utterance.length))
                        ignoredLength += utterance.length
                        continue
#                    sys.stderr.write("processing %s (length %fs)\n"%(self.xmlFile,utterance.length))
                    fName = os.path.join(self.outFolder,"%s_%s"%(self.fName,utterance.uID))
                    #get the wave-slice
                    os.system("sox %s -b 16 %s.wav trim %f %f channels 1 rate 16k"%(self.soundFile,os.path.join(self.outFolder,"wav",fName),utterance.start,utterance.length))
                    #get the transcript
                    self.transcriptions.append((utterance.words,os.path.join(self.outFolder,"wav","%s_%s.wav"%(self.fName,utterance.uID))))

class Utterance:
    def __init__(self, start, length, words,uID):
        self.start = float(start)
        self.length = float(length)
        self.words = [x.upper() for x in words if x is not None]
        self.uID = uID

    



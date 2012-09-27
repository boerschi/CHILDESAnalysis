#!/usr/bin/python
#
# date: 26/09/12


usage="""prepareChildesXML.py is a script that prepares a single CHILDES xml-file by generating
individual audio-files for every (time-aligned) utterance in the transcript, as well as
generating a list of transcriptions and files that are required for HTK processing

prepareChildesXML.py <xml-file> <audio-file> <dictionary>    
"""

import xmlchat, sys, codecs, os, optparse

class Transcript:
    def __init__(self,xmlFile,outFolder,soundFile,speakers="MOT FAT".split()):
        self.filelist = []
        self.transcriptions = []
        self.outFolder = outFolder
        self.xmlFile = xmlFile
        self.utterances = xmlchat.readfile(xmlFile)[1]
        self.speakers = speakers

    def createAlignmentFiles(self):
        for ut in self.utterances:
            if ut['who'] in speakers:
                if ut.has_key("start"):
                    utterance = Utterance(ut["start"],ut["end"]-ut["start"],ut["words"],ut["uID"])
                    fName = "%s_%s"%(utterance.corpus,utterance.uID)
                    print "processing %s (length %fs)"%(fName,utterance.length)
                    #get the wave-slice
                    os.system("sox %s -b 16 %s.wav trim %f %f channels 1 rate 16k"%(fullFile,fName,utterance.start,utterance.length))
                    #get the transcript
                    if not hasTranscription(utterance,dictionary):
                        writeTranscriptFile(utterance.words,"%s.unk"%fName,dictionary)
                    else:
                        filelist.append(fName)
                        transcriptions.append(getTranscription(utterance.words,fName,dictionary))


class Utterance:
    def __init__(self, start, length, words,,uID):
        self.start = float(start)
        self.length = float(length)
        self.words = [x.upper() for x in words if x is not None]
        self.uID = uID


def hasTranscription(utterance,dictionary):
    for w in utterance.words:
        if not dictionary.has_key(w.upper()):
            return False
    return True

def createAlignmentFiles(utterance, dictionary,fullFile):
    """
        creates a small wave-file for each utterance and produce both the file-list and the transcription-file needed for
        SPHINX adaptation
    """
    global filelist
    global transcriptions
    fName = "%s_%s"%(utterance.corpus,utterance.uID)
    print "processing %s (length %fs)"%(fName,utterance.length)
    #get the wave-slice
    os.system("sox %s -b 16 %s.wav trim %f %f channels 1 rate 16k"%(fullFile,fName,utterance.start,utterance.length))
    #get the transcript
    if not hasTranscription(utterance,dictionary):
        writeTranscriptFile(utterance.words,"%s.unk"%fName,dictionary)
    else:
        filelist.append(fName)
        transcriptions.append(getTranscription(utterance.words,fName,dictionary))
#        writeTranscriptFile(utterance.words,"%s.mlf"%fName,dictionary)
        #align the slice
#        os.system("python %s/align.py %s_%s.wav %s_%s.mlf %s_%s.align"%(p2fa,utterance.corpus,utterance.uID,utterance.corpus,utterance.uID,utterance.corpus,utterance.uID))
        #save the raw output of f2pa
#        os.system("mv ./tmp/aligned.mlf ./%s_%s.raw"%(utterance.corpus,utterance.uID))

def writeTranscriptFile(words,fileName,dictionary):
    output = codecs.open(fileName,'w',encoding="UTF-8")
    for w in words:
        if dictionary.has_key(w.upper()):
            output.write("%s\n"%w)
        else:
            output.write("%s_UNK\n"%w)
    output.close()

def getTranscription(words,fName,dictionary):
    res = []
    res.append("<s>")
    for w in words:
        res.append(w.upper())
    res.append("</s>")
    res.append("(%s)"%fName)
    return " ".join(res)

def readDict(dictFile):
    """
        only returns an indicator whether or not a word has a transcription
    """
    result = {}
    d = codecs.open(dictFile,"r",encoding="UTF-8")
    for line in d:
        result[line.strip().split("\t")[0]] = 1
    d.close()
    return result

    

if __name__=="__main__":
    try:
        inFile = sys.argv[1]
        soundFile = sys.argv[2]
        dictFile = sys.argv[3]
    except IndexError:
        print usage
        sys.exit(-1)
    transcript = xmlchat.readfile(inFile)
    print transcript
    pronDict = readDict(dictFile)
    childId = inFile.split("/")[-1].split(".")[0]
    for ut in transcript[1]:
        if ut['who']!="CHI":
            if ut.has_key("start"):
                tmpUt = Utterance(ut["start"],ut["end"]-ut["start"],ut["words"],childId,ut["uID"])
                createAlignmentFiles(tmpUt,pronDict,soundFile)
    #now generate the file-list and transcription file
    fList = open("tmp.listoffiles","w")
    tList = open("tmp.transcriptions","w")
    for (f,t) in zip(filelist,transcriptions):
        fList.write("%s\n"%f)
        tList.write("%s\n"%t)
    fList.close()
    tList.close()



#!/usr/bin/python
#
# date: 03/10/12
# author: boerschi@cl.uni-heidelberg.de
#
# this script prepares an entire xml-folder (or a sequence of folders)
# for forced alignment, taking the current working directory as its output
# folder

import sys, prepareChildesXML, os

if __name__=="__main__":
    N = len(sys.argv[1:])
    pairs = zip([sys.argv[1:][i] for i in range(N) if i%2==0],[sys.argv[1:][i] for i in range(N) if i%2==1])
    transcripts = []
    for (xFolder,sFolder) in pairs:
        print("Processing %s"%xFolder)
        N = len(os.listdir(xFolder))
        i = 0
        for f in os.listdir(xFolder):
            sys.stdout.write("\r%f (%d/%d)"%(i/float(N),i,N))
            sys.stdout.flush()
            if not f.endswith(".xml"): continue
            transcript = prepareChildesXML.Transcript(os.path.join(xFolder,f),"./",sFolder)
            transcript.createAlignmentFiles()
            transcripts.append(transcript)
            i += 1
        print
    for t in transcripts:
        prepareChildesXML.generateLabelFile(transcripts)
    print("Ignored a total of %f min"%prepareChildesXML.ignoredLength/60.)

            

import sys
import nltk
import json
import codecs
from practnlptools.tools import Annotator
import gensim
import glob
import subprocess

class tcw2v0010:

    def __init__(self):
        # stores all the files as json objects with data from TIPSem and word2vec for each document
        self.documents = []
        self.inputDir = '/home/osboxes/ML/semeval-2015-task-4-master/output'

        # using  Stanford Glove instead of Word2Vec because the  the word2vec for wikipedia was too big  (over 8 GB)
        # we first convert the glove output to word2vec format so that gensim can  use it
        # read data from TipSem output files. Assumption is the files have TIPSem data and raw text & each line a  JSON object
        self.model= gensim.models.KeyedVectors.load_word2vec_format('/home/osboxes/glove2word2vecout.txt', binary=False)
    def loadData(self):

        try:
            # load the lines of the input file into a list. Each line is a json object.
            # we expect three files; one for each corpus
            for filename in glob.glob(self.inputDir + '/*_output.txt'):
                print 'Processing ' + filename + '...'
                f = codecs.open(filename, encoding='utf-8')
                # read each line as a json object and load the data1 list.
                for line in f:
                    self.getword2vec(json.loads(line)['RAW TEXT'], self)
                    # print json.loads(line)['RAW TEXT']
                    self.documents.append(json.loads(line))
        except:
            e = sys.exc_info()
            print e
        return

    def addVectors (vector1, vector2):
        result = []
        if vector1.__len__()!= vector2.__len__():
            print 'Two vectors added should have same length' + str(vector1.__len__()) + ' ' + str(vector2.__len__())
            return []
        else:
            for i in range(0, vector1.__len__()):
                result.append(vector1[i]+vector2[i])
        return result

    def getvector(strPhrase, self):
        tokentxt = nltk.word_tokenize(strPhrase)
        vectorVal = []
        ctr = 0
        for tkn in tokentxt:
            #print tkn

            try:
                tknVector = self.model[tkn.lower()]
            except:
                ctr = ctr + 1
                continue
            if ctr==0:
                vectorVal = tknVector
            else:
                vectorVal = self.addVectors(vectorVal, tknVector)
            ctr = ctr + 1
        return vectorVal

    def getword2vec(rawtext, self):
        sentences = nltk.sent_tokenize(rawtext)
        annotator = Annotator()
        counter = 0
        docVec = []
        for sentence in sentences:
            #get semantic role labelling data for each sentence
            srl = list(annotator.getAnnotations(sentence)['srl'])
            word2vec =[]
            #get the event structure for each sentence
            for s in srl:
                if 'V' in s:
                    #print s['V']
                    word2vec = self.getvector(s['V'])
                    #print word2vec
                else:
                    print 'No verb found in sentence'
                    return
                if 'A0' in s:
                    #print s['A0']
                    word2vec = self.addVectors(word2vec, self.getvector(s['A0']))

                if 'A1' in s:
                    #print s['A1']
                    word2vec = self.addVectors(word2vec, self.getvector(s['A1']))
            if counter ==0:
                docVec = word2vec
            else:
                docVec = self.addVectors(docVec, word2vec)
            counter = counter + 1
    def createJSONfromFiles(self):
        p= subprocess.Popen(java -jar /home/osboxes/ML/)




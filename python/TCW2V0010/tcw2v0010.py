import sys
import nltk
import json
import codecs
from practnlptools.tools import Annotator
import gensim
import glob
import subprocess
import os
import scipy.spatial.distance as sci
from operator import itemgetter


# import requests

class TcW2v0010:
    def __init__(self):

        # stores all the files as json objects with data from TIPSem and word2vec for each document
        self.documents = []
        self.file_data = []
        self.inputDir = '/home/osboxes/ML/semeval-2015-task-4-master/output'

        # using  Stanford Glove instead of Word2Vec because the  the word2vec for wikipedia was too big  (over 8 GB)
        # we first convert the glove output to word2vec format so that gensim can  use it
        # read data from TipSem output files.
        # Assumption is the files have TIPSem data and raw text & each line a  JSON object
        self.model = gensim.models.KeyedVectors.load_word2vec_format('/home/osboxes/glove2word2vecout.txt',
                                                                    binary=False)

    def loadData(self, corpus_name):

        try:
            print "Loading " + corpus_name + " data for processing..."
            # load the lines of the input file into a list. Each line is a json object.
            # we expect three files; one for each corpus
            for filename in glob.glob(self.inputDir + '/' + corpus_name + '_output.txt'):
                #print 'Processing ' + filename + '...'
                f = codecs.open(filename, encoding='utf-8')
                # read each line as a json object and load the data1 list.
                for line in f:
                    # txt = str(json.loads(line)['RAW TEXT'])
                    # self.getword2vec(txt)
                    # print json.loads(line)['RAW TEXT']
                    self.documents.append(json.loads(line))
                f.close()
        except:
            e = sys.exc_info()
            print e
        return

    @staticmethod
    def addVectors(vector1, vector2):
        result = []
        if vector1.__len__() != vector2.__len__():
            if vector1.__len__() == 0:
                return vector1
            elif vector2.__len__() == 0:
                return vector2
            else:
                print 'Two vectors added should have same length' + str(vector1.__len__()) + ' ' + str(
                    vector2.__len__())
                return []
        else:
            for i in range(0, vector1.__len__()):
                result.append(vector1[i] + vector2[i])
        return result

    def getvector(self, str_phrase):
        token_txt = nltk.word_tokenize(str_phrase)
        vector_val = []
        ctr = 0
        for tkn in token_txt:
            # print tkn

            try:
                tkn_vector = self.model[tkn.lower()]
            except:
                ctr = ctr + 1
                continue
            if ctr == 0:
                vector_val = tkn_vector
            else:
                vector_val = self.addVectors(vector_val, tkn_vector)
            ctr = ctr + 1
        return vector_val

    def getword2vec(self, raw_text):
        sentences = nltk.sent_tokenize(raw_text)
        annotator = Annotator()
        counter = 0
        doc_vec = []
        for sentence in sentences:
            # get semantic role labelling data for each sentence
            srl = list(annotator.getAnnotations(sentence)['srl'])
            word2vec = []
            # get the event structure for each sentence
            for s in srl:
                if 'V' in s:
                    # print s['V']
                    word2vec = self.getvector(s['V'])
                    # print word2vec
                else:
                    print 'No verb found in sentence'
                    return
                if 'A0' in s:
                    # print s['A0']
                    word2vec = self.addVectors(word2vec, self.getvector(s['A0']))

                if 'A1' in s:
                    # print s['A1']
                    word2vec = self.addVectors(word2vec, self.getvector(s['A1']))
            if counter == 0:
                doc_vec = word2vec
            else:
                doc_vec = self.addVectors(doc_vec, word2vec)
            counter = counter + 1

    @staticmethod
    def createJSONfromFiles():
        p = subprocess.Popen('java -jar /home/osboxes/ML/TCW2V0010/createCorpusJson.jar' +
                             ' /home/osboxes/ML/semeval-2015-task-4-master', shell=True)
        st = os.waitpid(p.pid, 0)

    def getNERdata(self, txt):
        try:
            p = subprocess.Popen('/home/osboxes/ML/TCW2V0010/getOpeNEROutput.sh ' +
                                 "'" + str(txt) + "&language=en'", shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            strs = p.stdout.read()
            # print str(strer)
            # print json.loads(strs)

            # print str(kaf_str)

        except:
            e = sys.exc_info()
            print e
        return json.loads(strs)

        # st = os.waitpid(p.pid, 0)

    def get_filtered_verbs_with_vecs(self, doc_id, srl, entity):
        # get the verbs that only relate to the entity and the associated word2vec for
        # that event structure. Event structure is the set {A0, A1, V}
        filtered_event_list = []
        try:
            # print json.dumps(srl)
            # get NER info for sentence
            # opener_output = self.getNERdata(str(sentence))
            # print 'afer opener....'
            for s in srl:
                # print json.dumps(s)
                # stores the word2vec for an event if it matches the entity
                word2vec = []
                tmp_struc = {}
                # if we find a verb in the object


                if 'V' in s:

                    # to indicate if A1 or A0 match was found for entity
                    match_found = 0
                    a0_txt = ''
                    a1_txt = ''

                    word2vec = self.getvector(str(s['V']))
                    # print word2vec
                    if 'A0' in s:
                        a0_txt = s['A0']
                        # print a0_txt
                        if str.lower(a0_txt).__contains__(str.lower(entity)):
                            match_found = 1
                            tmp_vec = self.getvector(s['A0'])
                            # add the vector to the verb only if found in Glove
                            if tmp_vec.__len__() > 0:
                                word2vec = self.addVectors(word2vec, self.getvector(s['A0']))
                    if 'A1' in s:
                        a1_txt = s['A1']
                        # print a1_txt
                        if str.lower(a1_txt).__contains__(str.lower(entity)):
                            match_found = 1
                            tmp_vec = self.getvector(s['A1'])
                            # add the vector to the verb only if found in Glove
                            if tmp_vec.__len__() > 0:
                                word2vec = self.addVectors(word2vec, self.getvector(s['A1']))

                                # print 'preparing object...'
                    if match_found == 1:
                        # print 'match found' + '--->' +  s['V']
                        tmp_struc['doc_id'] = str(doc_id)
                        tmp_struc['event'] = s['V']
                        tmp_struc['w2v'] = word2vec
                        # add json to list
                        filtered_event_list.append(tmp_struc)

        except:
            e = sys.exc_info()
            print 'inside word vector proc...'
            print e
        return list(filtered_event_list)

    def get_filtered_events(self, doc_id, raw_text, entity):

        filtered_events = []
        sentences = nltk.sent_tokenize(raw_text)
        annotator = Annotator()

        # for each sentence determine if it pertains to the entity
        for sentence in sentences:
            # get semantic role labelling data for each sentence
            events = self.get_filtered_verbs_with_vecs(doc_id, list(annotator.getAnnotations(sentence)['srl']), entity)
            # print events.__len__()
            if events.__len__() > 0:
                filtered_events.extend(events)

        # return list of events
        return filtered_events

    def get_tipsem_events(self, doc_id, event_txt, time_ml_object):
        # print event_txt
        # list of events from tipsem
        tlink_key = 'TLINK'.encode(encoding='utf-8')
        event_key = 'EVENT'.encode(encoding='utf-8')
        timex3_key = 'TIMEX3'.encode(encoding='utf-8')
        text_key = 'TEXT'.encode(encoding='utf-8')
        instance_key = 'MAKEINSTANCE'.encode(encoding='utf-8')

        tipsem_event_list = list(time_ml_object[text_key][event_key])
        tlink_list = list(time_ml_object[tlink_key])

        # event and time link
        tlink_list = list(time_ml_object[tlink_key])
        dct = time_ml_object['DCT'.encode(encoding='utf-8')]
        doc_date = dct[timex3_key]['value']

        event_struct = {}
        list_of_events = []
        event_date = ''

        # if not time info is found just assign doc date and move on
        if timex3_key in time_ml_object[text_key]:
            time_list = []
            time_list.extend(list(time_ml_object[text_key][timex3_key]))


            # look for event_Txt in event list and find corresponding date
            for te in tipsem_event_list:
                # print 'te--->'+str.lower(json.dumps(te['content']))
                if str.lower(json.dumps(te['content'])).__contains__(str.lower(event_txt).encode(encoding='utf-8')):
                    # get its timeid from tlink
                    # get the event instance id
                    for mi in time_ml_object[instance_key]:
                        if mi['eventID'] == te['eid']:
                            eiid = mi['eiid']
                            # print '\t\t\t\t\t\t\t\t\t'+str(eiid)

                    # find the time
                    for tl in tlink_list:

                        if tl['eventInstanceID'] == eiid:

                            # print '\t\t\t\ttipsem---->' + json.dumps(tl)
                            if tl['relType'] == 'IS_INCLUDED' and 'relatedToTime' in tl:
                                # print "\t\t\t\t\t\t\t\t\tlink id " + tl['eventInstanceID'] + ' ' + tl['relType'] \
                                #     + ' ' + tl['relatedToTime']
                                tid = tl['relatedToTime']
                                if tid == 't0':
                                    event_date = doc_date
                                else:
                                    for t in time_list:
                                        #need to have this check as one of the docs does not have
                                        #a valid time structure. without the check the subsequent if check
                                        # errors out.
                                        if type(t) is 'dict':
                                            if t['tid'] == tid:
                                                event_date = t['value']

                                # form the event struct to send back
                                event_struct['event_date'] = event_date
                                event_struct['event_text'] = event_txt
                                event_struct['doc_id'] = doc_id
                                event_struct['dct'] = doc_date
                                # print json.dumps(event_struct)
                                list_of_events.append(event_struct)




        return list_of_events

    def sort_event_list(self, pre_sort_list):
        #event struc = {"w2v": [], "doc_id": "tmp2017.08.19-20.09.46.043", "event_text": "delayed", "event_date": "2017-08-19",
        # "dct": "2017-08-19", "doc_counter": 4}
        sorted_list = []

        # first get cosine distance of words and add to event. All with respect to first event
        copy_of_list = list(pre_sort_list)
        for pe in pre_sort_list:
            for pj in copy_of_list:
                pj['cosine'] = sci.cosine(pe['w2v'], pj['w2v'])
                #print str(pj['cosine'])
        sorted_list = sorted(copy_of_list, key=itemgetter('cosine', 'event_date'))
        return sorted_list

    def retrieveEvents(self, entity):
        doc_counter = 0
        tipsem_key = 'TIPSEM'.encode(encoding='utf-8')
        time_ml_key = 'TimeML'.encode(encoding='utf-8')
        doc_id_key = 'DOCID'.encode(encoding='utf-8')

        timex3_key = 'TIMEX3'.encode(encoding='utf-8')
        text_key = 'TEXT'.encode(encoding='utf-8')
        raw_txt_key = 'RAW TEXT'.encode(encoding='utf-8')
        final_event_list = []
        pre_sorted_final_list = []
        ner_filtered_events = []

        for doc in self.documents:
            # doc_id
            doc_id = doc[tipsem_key][time_ml_key][doc_id_key]
            time_ml_object = doc[tipsem_key][time_ml_key]  # [text_key]

            # all events identified by TipSem
            events = time_ml_object['TLINK'.encode(encoding='utf-8')]
            tmp_list = self.get_filtered_events(doc_id, json.dumps(doc[raw_txt_key]), entity)

            # if there are no events for the entity from ner move on to next doc
            if tmp_list.__len__() > 0:
                ner_filtered_events.extend(tmp_list)
                # if there are matching events
                # look up event time
                for ne in ner_filtered_events:
                    event_txt = ne['event']
                    # should ideally return one record. Just in case...

                    elist = self.get_tipsem_events(doc_id, event_txt, time_ml_object)
                    # append the word2vec vector to the event
                    for e in elist:
                        e['doc_counter'] = doc_counter
                        e['w2v'] = ne['w2v']
                    # NEED TO DEAL WITH SIMULTANEOUS EVENTS
                    pre_sorted_final_list.extend(elist)

            doc_counter = doc_counter + 1
            final_event_list=self.sort_event_list(pre_sorted_final_list)

        # if final_event_list.__len__() ==0:
        #    print "No events found"
        #    return
        # print entity + '....'
        # for fe in final_event_list:
        #    print str(fe['doc_counter']) + '\t' + str(fe['event_date']) + '\t' + fe['doc_id'] + '-' + fe['event_text']
        return final_event_list

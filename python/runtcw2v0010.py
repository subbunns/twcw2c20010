import sys
import os
from TCW2V0010 import TcW2v0010

input_dir = '/home/osboxes/ML/semeval-2015-task-4-master'
output_path = '/home/osboxes/ML/semeval-2015-task-4-master/output'
try:
    m = TcW2v0010()
    #uncomment to process documents and output tipsem data
    #m.createJSONfromFiles()

    # m.retrieveEvents('Airbus')
    #exit()

    #CORPUS 1
    m.loadData('corpus_1')
    entity_file = open(input_dir + '/corpus_1/list_target_entities_corpus_1.txt')

    if not os.path.exists(output_path + '/corpus_1'):
        os.makedirs(output_path + '/corpus_1')
    lines = entity_file.readlines()
    for l in lines:
        output_file = output_path + '/corpus_1/' + str.replace(str.strip(l), " ", "_") + '.txt'
        print 'Procsssing entity ' + str.strip(l) + ' to ' + output_file
        event_list = m.retrieveEvents(str.strip(l))
        if event_list.__len__() > 0:
            print str(event_list.__len__())
            of = open(output_file, 'w')
            for e in event_list:
                out_line = str(e['doc_counter']) + '\t' + str(e['event_date']) + '\t' + e['doc_id'] + '-' + e[
                    'event_text']
                of.write(out_line.encode(encoding='utf-8')+'\n')
            of.close()
        else:
            print 'No events found in corpus'
    entity_file.close()

    exit()

    # CORPUS 2
    m.loadData('corpus_2')
    entity_file = open(input_dir + '/corpus_2/list_target_entities_corpus_2.txt')

    if not os.path.exists(output_path + '/corpus_2'):
        os.makedirs(output_path + '/corpus_2')
    lines = entity_file.readlines()
    for l in lines:
        output_file = output_path + '/corpus_2/' + str.replace(str.strip(l), " ", "_") + '.txt'
        print 'Procsssing entity ' + str.strip(l) + ' to ' + output_file
        event_list = m.retrieveEvents(str.strip(l))
        if event_list.__len__() > 0:
            print str(event_list.__len__())
            of = open(output_file, 'w')
            for e in event_list:
                out_line = str(e['doc_counter']) + '\t' + str(e['event_date']) + '\t' + e['doc_id'] + '-' + e[
                    'event_text']
                of.write(out_line.encode(encoding='utf-8') + '\n')
            of.close()
        else:
            print 'No events found in corpus'
    entity_file.close()

    # CORPUS 3
    m.loadData('corpus_3')
    entity_file = open(input_dir + '/corpus_3/list_target_entities_corpus_3.txt')

    if not os.path.exists(output_path + '/corpus_3'):
        os.makedirs(output_path + '/corpus_3')
    lines = entity_file.readlines()
    for l in lines:
        output_file = output_path + '/corpus_3/' + str.replace(str.strip(l), " ", "_") + '.txt'
        print 'Procsssing entity ' + str.strip(l) + ' to ' + output_file
        event_list = m.retrieveEvents(str.strip(l))
        if event_list.__len__() > 0:
            print str(event_list.__len__())
            of = open(output_file, 'w')
            for e in event_list:
                out_line = str(e['doc_counter']) + '\t' + str(e['event_date']) + '\t' + e['doc_id'] + '-' + e[
                    'event_text']
                of.write(out_line.encode(encoding='utf-8') + '\n')
            of.close()
        else:
            print 'No events found in corpus'
    entity_file.close()

except:
    e = sys.exc_info()
    print e

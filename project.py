
###########################
#NLP Project 2017 main code
###########################

#Autors: Hong Xu and Jie Zhang
#Repository: https://github.com/HeavenlyBerserker/NLP_Project_2017.git
#Sources for nltk: http://www.nltk.org/book_1ed/
#Credit to : Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. OReilly Media Inc.

#Possibly useful imports
import argparse
import sys
import getopt
import math
import re
import random
import os
#NLP tools
import nltk
import spacy
from spacy.lang.en import English
from nltk import Tree
import en_core_web_sm
import unicodedata
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords


import random
from spacy.gold import GoldParse
from spacy.language import EntityRecognizer




def main(argv):
	#print(wn.synsets("jump")[0].pos() == "v")
	#print(nltk.pos_tag(["kill"]))

	#[print(sent.root) for sent in en_doc.sents]
	#print(WordNetLemmatizer().lemmatize('being','v'))

	#Reads the files in directory that begin with DEV and parses them into
	#project friendly format
	#files = [file_index 0-i] 
	#		 [0 = filename, 1 = text_file_related, 2 = answers_file_related] 
	#[i][0] = filename
	#[i][1][0] = raw text
	#[i][1][1] = parsed sentences
	#[i][1][2] = important words meaning words that were extracted as parsed answers 
	#	plus the index in which they were found in that sentence
	#[i][1][3] = Tagged noun phrases in sentences
	#[i][1][4] = POSs in sentences
	#[i][1][5] = veps in sentences
	#[i][2][0] = raw answers
	#[i][2][1] = parsed answers
	#See printed output for more details
	files = processFiles('developset/texts', 'developset/answers', "DEV")
	t1Files = processFiles('developset/texts', 'developset/answers', "TST1")

	#uncomment the following line to see how "files" works
	#printFiles(files)
	print("Loading 20%")

	patterns, trigs, words = paternize(files)
	subjpatternlist, csubjpatternlist, nsubjpasspatternlist, csubjpasspatternlist, dobjpatternlist, pobjpatternlist = auto_slog(files)
               
	print("Loading 80%")

	writePats(patterns, "output/patterns.txt")
	writeTrigs(trigs, "output/triggers.txt")
	writeWords(words, "output/words.txt")

        writePats_autoslog(subjpatternlist, "output/subjpatterns.txt")
        writePats_autoslog(csubjpatternlist, "output/csubjpatterns.txt")
        writePats_autoslog(nsubjpasspatternlist, "output/nsubjpasspatterns.txt")
        writePats_autoslog(csubjpasspatternlist, "output/csubjpasspatterns.txt")
        writePats_autoslog(dobjpatternlist, "output/dobjpatterns.txt")
        writePats_autoslog(pobjpatternlist, "output/pobjpatterns.txt")
        
	#printFiles(t1Files)

	print("Loading 100%")

	print(argv)

#Writes words in
def writeWords(trigs, name):
	file = open(name, 'w')
	for line in trigs:
		file.write(line[0] +"/" + line [1] +"/" + str(line [2]) + "\n")

#Writes triggers to a file
def writeTrigs(trigs, name):
	file = open(name, 'w')
	for line in trigs:
		file.write(line[0] +"/" + line [1] + "\n")

#Writes patterns to a file
def writePats(pats, name):
	file = open(name, 'w')
	for line in pats:
		file.write(line[0] + "/" +  line[1] + "/" + line[2] + "/" + str(line[3]) + "\n")

#Writes patterns to a file
def writePats_autoslog(pats, name):
	file = open(name, 'w')
	for line in pats:
                length=len(line)
                for i in range(0, length):
                        file.write(str(line[i]) + "/")
                file.write("\n")



def auto_slog(files):
        nlp=spacy.load('en')
        sentences = []
        imp = []

        subjpatternlist=[]
        csubjpatternlist=[]
        nsubjpasspatternlist=[]
        csubjpasspatternlist=[]
        dobjpatternlist=[]
        pobjpatternlist=[]

	for i in range(len(files)):
		sentences=files[i][1][1]
		imp=files[i][1][2]

                
                for index in range(len(imp)):
                        if len(imp[index])!=0:
                                imp_in_one_sent=imp[index]
                                #print imp_in_one_sent
                                sent=sentences[index]
                                #print sent
                                doc=nlp(unicode(sent))
                                #print "len(doc)"
                                #print len(doc)
                                
                                imp_entry_len=len(imp_in_one_sent)
                                for j in range(0, imp_entry_len):
                                        one_key=imp_in_one_sent[j]
                                        if one_key[2]=='VICTIM' or one_key[2]=='TARGET' or one_key[2]=='PERP INDIV':
                                        #print one_key
                                        #print "one_key[0].lower"
                                        #print one_key[0].lower()
                                                for word in doc:
                                                        if word.text.encode('utf-8').lower()==one_key[0].lower() or word.text.encode('utf-8').lower() in one_key[0].lower() or one_key[0].lower() in word.text.encode('utf-8').lower():
                                                                
                                                                if word.dep_.encode('utf-8')=='nsubj':
                                                                        one_pattern_entry=[]
                                                                        #one_pattern_entry.append('subj')
                                                                        #one_pattern_entry.append(one_key[0])

                                                                        not_exit=True
                                                                        current=word.i+1
                                                                        ########SHOULD WE JUST EXTRACT ROOT HERE???????????????########################
                                                                        while not_exit and current<len(doc):
                                                                                                                                               
                                                                                if doc[current].pos_.encode('utf-8')=="VERB":
                                                                                        if doc[current].tag_.encode('utf-8')=="VBP" or doc[current].tag_.encode('utf-8')=="HVS":
                                                                                                one_pattern_entry.append(doc[current].lemma_.encode('utf-8'))
                                                                                                if doc[current+1].pos_.encode('utf-8')=="VERB":
                                                                                                        one_pattern_entry.append(doc[current+1].text.encode('utf-8'))
                                                                                        else:
                                                                                                one_pattern_entry.append(doc[current].text.encode('utf-8'))
                                                                                                if doc[current+1].pos_.encode('utf-8')=="VERB":
                                                                                                        one_pattern_entry.append(doc[current+1].text.encode('utf-8'))
                                                                                        not_exit=False
                                                                                current=current+1
                                                                                        
                                                                        one_pattern_entry.append(one_key[2])
                                                                        subjpatternlist.append(one_pattern_entry)
                                                                        
                                                                        
 
                                                                        '''
                                                                        for current in doc:
                                                                                if current.dep_.encode('utf-8')=="ROOT":
                                                                                        if doc[current.i-1].dep_.encode('utf-8')=='aux':
                                                                                                one_pattern_entry.append(doc[current.i-1].text.encode('utf-8'))
                                                                                        one_pattern_entry.append(current.text.encode('utf-8'))
                                                                        one_pattern_entry.append(one_key[2])
                                                                        subjpatternlist.append(one_pattern_entry)
                                                                        '''
                                                                if word.dep_.encode('utf-8')=='csubj':
                                                                        one_pattern_entry=[]
                                                                        #one_pattern_entry.append('csubj')
                                                                        #one_pattern_entry.append(one_key[0])

                                                                        not_exit=True
                                                                        current=word.i+1
                                                                        ########SHOULD WE JUST EXTRACT ROOT HERE???????????????########################
                                                                        while not_exit and current<len(doc):                                                                                                                                            
                                                                                if doc[current].pos_.encode('utf-8')=="VERB":
                                                                                        if doc[current].tag_.encode('utf-8')=="VBP" or doc[current].tag_.encode('utf-8')=="HVS":
                                                                                                one_pattern_entry.append(doc[current].lemma_.encode('utf-8'))
                                                                                                if doc[current+1].pos_.encode('utf-8')=="VERB":
                                                                                                        one_pattern_entry.append(doc[current+1].text.encode('utf-8'))
                                                                                        else:
                                                                                                one_pattern_entry.append(doc[current].text.encode('utf-8'))
                                                                                                if doc[current+1].pos_.encode('utf-8')=="VERB":
                                                                                                        one_pattern_entry.append(doc[current+1].text.encode('utf-8'))
                                                                                        not_exit=False
                                                                                current=current+1
                                                                                        
                                                                        one_pattern_entry.append(one_key[2])
                                                                        subjpatternlist.append(one_pattern_entry)
                                                                        
                                                                        
                                                                        '''
                                                                        for current in range(word.i, len(doc)):
                                                                                if doc[current].dep_.encode('utf-8')=="ccomp" or doc[current].pos_.encode('utf-8')=='VERB':
                                                                                        one_pattern_entry.append(doc[current].text.encode('utf-8'))
                                                                                        
                                                                        one_pattern_entry.append(one_key[2])
                                                                        csubjpatternlist.append(one_pattern_entry)
                                                                        '''
                                                                
                                                                if word.dep_.encode('utf-8')=='nsubjpass':
                                                                        one_pattern_entry=[]
                                                                        #one_pattern_entry.append('nsubjpass')
                                                                        #one_pattern_entry.append(one_key[0])
 

                                                                
                                                                        for current in range(word.i, len(doc)):
                                                                                if doc[current].pos_.encode('utf-8')=='VERB' and doc[current].dep_.encode('utf-8')=="auxpass":                                                                                       
                                                                                        if doc[current+1].pos_.encode('utf-8')=='VERB':
                                                                                                one_pattern_entry.append(doc[current].lemma_.encode('utf-8'))
                                                                                                one_pattern_entry.append(doc[current+1].text.encode('utf-8'))
                                                                                                break
                                                                        one_pattern_entry.append(one_key[2])
                                                                        nsubjpasspatternlist.append(one_pattern_entry)
                                                                
                                                                
                                                                if word.dep_.encode('utf-8')=='csubjpass':
                                                                        one_pattern_entry=[]
                                                                        #one_pattern_entry.append('csubjpass')
                                                                        #one_pattern_entry.append(one_key[0])
                                                                         
                                                                        
                                                                        for current in range(word.i, len(doc)):
                                                                                if doc[current].dep_.encode('utf-8')=="ccomp" or doc[current].pos_.encode('utf-8')=='VERB':
                                                                                        one_pattern_entry.append(doc[current].text.encode('utf-8'))
                                                                        one_pattern_entry.append(one_key[2])
                                                                        csubjpasspatternlist.append(one_pattern_entry)

                                                        

  
                                                                if word.dep_.encode('utf-8')=='pobj':
                                                                        one_pattern_entry=[]
                                                                        #one_pattern_entry.append('pobj')
                                                                        #one_pattern_entry.append(one_key[0])

                                                                        if (doc[word.i-1].dep_.encode('utf-8')=="prep" or doc[word.i-1].pos_.encode('utf-8')=="ADP") and (doc[word.i-1-1].pos_.encode('utf-8')=="VERB" or doc[word.i-1-1].pos_.encode('utf-8')=="NOUN"):
                                                                                if doc[word.i-1-1].pos_.encode('utf-8')=="VERB" and doc[word.i-1-1-1].pos_.encode('utf-8')=="VERB":
                                                                                        one_pattern_entry.append(doc[word.i-1-1-1].text.encode('utf-8'))
                                                                                        one_pattern_entry.append(doc[word.i-1-1].text.encode('utf-8'))
                                                                                        one_pattern_entry.append(doc[word.i-1].text.encode('utf-8'))
                                                                                                
                                                                                else:
                                                                                        one_pattern_entry.append(doc[word.i-1-1].text.encode('utf-8'))
                                                                                        one_pattern_entry.append(doc[word.i-1].text.encode('utf-8'))
                                                                                                
                                                                               
                                                                        '''
                                                                        for current in range(0, word.i):
                                                                                if doc[current].dep_.encode('utf-8')=="prep" and (doc[current-1].pos_.encode('utf-8')=="VERB" or doc[current-1].pos_.encode('utf-8')=="NOUN"):
                                                                                #if (doc[current].pos_.encode('utf-8')=="ADP" or doc[current].dep_.encode('utf-8')=="prep" ) and (doc[current-1].pos_.encode('utf-8')=="VERB" or doc[current-1].pos_.encode('utf-8')=="NOUN"):
                                                                                #if (doc[current].pos_.encode('utf-8')=="ADP" or doc[current].dep_.encode('utf-8')=="prep" or doc[current].dep_.encode('utf-8')=="agent" ) and (doc[current-1].pos_.encode('utf-8')=="VERB" or doc[current-1].pos_.encode('utf-8')=="NOUN"):
                                                                                        
                                                                                        if doc[current-1].pos_.encode('utf-8')=="VERB" and doc[current-1-1].pos_.encode('utf-8')=="VERB":
                                                                                                one_pattern_entry.append(doc[current-1-1].text.encode('utf-8'))
                                                                                                one_pattern_entry.append(doc[current-1].text.encode('utf-8'))
                                                                                                one_pattern_entry.append(doc[current].text.encode('utf-8'))
                                                                                                break
                                                                                        else:
                                                                                                one_pattern_entry.append(doc[current-1].text.encode('utf-8'))
                                                                                                one_pattern_entry.append(doc[current].text.encode('utf-8'))
                                                                                                break
                                                                        '''

                                                                        one_pattern_entry.append(one_key[2])
                                                                        pobjpatternlist.append(one_pattern_entry)
                                                        
                ####clean subj here!!!!!!
        subjpatternlist = clean_subj(subjpatternlist)
        subjpatternlist = subj_list_lemma(subjpatternlist)
        for entry in nsubjpasspatternlist:
                subjpatternlist.append(entry)

        subjpatternlist=clean_pattern(subjpatternlist)
        csubjpatternlist=clean_pattern(csubjpatternlist)
        nsubjpasspatternlist=clean_pattern(nsubjpasspatternlist)
        csubjpasspatternlist=clean_pattern(csubjpasspatternlist)       
        dobjpatternlist=clean_pattern(dobjpatternlist)
        pobjpatternlist=clean_pattern(pobjpatternlist)

        subjpatternlist=clear_pattern_again(subjpatternlist)
        csubjpatternlist=clear_pattern_again(csubjpatternlist)
        nsubjpasspatternlist=clear_pattern_again(nsubjpasspatternlist)
        csubjpasspatternlist=clear_pattern_again(csubjpasspatternlist)       
        dobjpatternlist=clear_pattern_again(dobjpatternlist)
        pobjpatternlist=clear_pattern_again(pobjpatternlist)

        subjpatternlist=trim_one(subjpatternlist)
        csubjpatternlist=trim_one(csubjpatternlist)
        nsubjpasspatternlist=trim_one(nsubjpasspatternlist)
        csubjpasspatternlist=trim_one(csubjpasspatternlist)       
        dobjpatternlist=trim_one(dobjpatternlist)
        pobjpatternlist=trim_one(pobjpatternlist)


        pobjpatternlist=clean_pobj(pobjpatternlist)


        print "print subj list #####################################################################"
        printList(subjpatternlist, 0)
        print "print csubj list ####################################################################"
        printList(csubjpatternlist, 0)
        print "print nsubjpass list ################################################################"
        printList(nsubjpasspatternlist, 0)
        print "print csubpass list #################################################################"
        printList(csubjpasspatternlist, 0)
        print "print dobj list #####################################################################"
        printList(dobjpatternlist, 0)
        print "print pobj list #####################################################################cl"
        printList(pobjpatternlist, 0)
        return subjpatternlist, csubjpatternlist, nsubjpasspatternlist, csubjpasspatternlist, dobjpatternlist, pobjpatternlist


def clean_pattern(patternlist):
        for pattern_entry in patternlist:
                if len(pattern_entry)==1:
                        patternlist.remove(pattern_entry)
        return patternlist
                
                        
                        
def clear_pattern_again(patternlist):
        pats = []
	for pat in patternlist:
		inPats = -1
		for i in range(len(pats)):
                        length=len(pats[i])
			if pat == pats[i][0:length]:
				inPats = i
		if inPats >= 0:
                        length=len(pats[i])
			pats[inPats][length-1] += 1
		else:
			p = list(pat)
			p.append(1)
			pats.append(p)

	pats = sorted(pats, key=lambda x: x[len(x)-1], reverse=True)
	uniquePats = []
	for pat in pats:
		repeated = False
		for i in range(len(uniquePats)):
                        uniquelength=len(uniquePats[i])
                        patlength=len(pat)
			if pat[0:patlength] == uniquePats[i][0:uniquelength]:
				repeated = True
		if not repeated:
			uniquePats.append(pat)			
	return uniquePats


def trim_one(patternlist):
        newpatternlist=[]
        for entry in patternlist:
                length=len(entry)
                entry=entry[0:length-1]
                newpatternlist.append(entry)
        return newpatternlist

def subj_list_lemma(subjpatternlist):
        belist=['AM', 'am', 'IS', 'is', 'WAS', 'was', 'ARE', 'are', 'WERE', 'were']
        havelist=['HAVE', 'HAS', 'HAD']
        for entry in subjpatternlist:
                if entry[0] in belist:
                        entry[0]='be'
                if entry[0] in havelist:
                        entry[0]='have'
        return subjpatternlist


                
def clean_subj(subjpatternlist):
        goodwordlist=['WEARING', 'DIED', 'KILLED', 'INJURED', 'RESPONSIBLE', 'HIT', 'OBLIGED', 'INTERCEPTED', 'OPERATING', 'CARRYING', 'IMPLICATED', 'ABONDONED', 'FAILED', 'ATTEMPTED', 'MAINTAIN', 'BOMBING', 'MISSING', 'ATTACKED', 'WARNED', 'MURDERED', 'LINKED', 'INVOLVED', 'SUFFERING', 'ATTACKED', 'RECALLED', 'COULD', 'ATTEMPTING', 'BOMBED', 'HURTING', 'GUARDING', 'SABOTAGED', 'PARTICIPATED', 'STAGED', 'CARRIED', 'ASSASSINATED','DAMAGED', 'FIRED', 'DENIED', 'SEEKING', 'FLEES']
        newsubjpatternlist=[]
        for entry in subjpatternlist:
                if entry[0] in goodwordlist:
                        newsubjpatternlist.append(entry)
        for entry in subjpatternlist:               
                if len(entry)>=2:
                        if entry[1] in goodwordlist:
                                newsubjpatternlist.append(entry)
        return newsubjpatternlist
        
def clean_dobj(dobjpatternlist):
        badwordlist=['wear', 'call','approve', 'need', 'issue', 'ask', 'do', 'deliver', 'see', 'say', 'request', 'indicate', 'admit','begin', 'remain','erupt', 'report', 'responsible', 'cross', 'heavy', 'say', 'propose', 'follow', 'have', 'will', 'include', 'receive', 'describe', 'make', 'do', 'find', 'request', 'reiterate', 'surround', 'leave', 'use', 'will','train', 'stop', 'hector', 'receive', 'have', 'point', 'continue', 'replace', 'name', 'participate','rank', 'be']
        newdobjpatternlist=[]
        for entry in dobjpatternlist:
                if len(entry)>=2:
                        if entry[0] in badwordlist:
                                continue
                        else:
                                newdobjpatternlist.append(entry)
                        
        return newdobjpatternlist

def clean_pobj(pobjpatternlist):
        badwordlist=['FASHION', 'MISSIONARIES', 'MORNING', 'ACCORDING', 'BEING', 'PRIESTS', 'BEEN', 'POWER', 'HEADQUARTERS']
        newpobjpatternlist=[]
        for entry in pobjpatternlist:
                if len(entry)>=2:
                        if entry[0] in badwordlist:
                                continue
                        else:
                                newpobjpatternlist.append(entry)                       
        return newpobjpatternlist


def create_NER_training_data(files):
        train_data=[]
        for i in range(len(files)):
            for j in range(len(files[i][1][2])):
                if len(files[i][1][2][j])!=0:
                        important_sentence=unicode(files[i][1][1][j])
                        tuple_info=[]
                        for k in range(len(files[i][1][2][j])):
                                important_entry=files[i][1][2][j][k]
                                start_index=important_entry[1][0]
                                end_index=start_index+len(important_entry[0])+1
                                important_word=important_entry[0]
                                #print "important entry"
                                #print important_entry
                                #print "importaant_index"
                                #print start_index, end_index
                                #print "important word"
                                #print important_word


                                answer_array=files[i][2][1]
                                for p in range(len(answer_array)):
                                        answer_line=answer_array[p]
                                        for q in range(1, len(answer_line)):
                                                if important_word in answer_line[q]:
                                                        label=answer_line[0]
                                                        #print "label"
                                                        #print label
                                                        one_tuple=(start_index, end_index, label)
                                                        tuple_info.append(one_tuple)
                        one_train_data_entry=(important_sentence, tuple_info)
                        train_data.append(one_train_data_entry)

        
        return train_data

def train_NER(train_data, t1Files):
        nlp=spacy.load('en', entity=False, parser=False)
        ner=EntityRecognizer(nlp.vocab, entity_types=['ID', 'INCIDENT', 'WEAPON', 'PERP INDIV', 'PERP ORG', 'TARGET', 'VICTIM'])

        for itn in range(5):
                random.shuffle(train_data)
                for raw_text, entity_offset in train_data:
                        doc = nlp.make_doc(raw_text)
                        gold = GoldParse(doc,entities=entity_offset)

                        nlp.tagger(doc)
                        ner.update(doc, gold)
                        
        ner.model.end_training()

        for i in range(len(t1Files)):
                test_file_sentences=t1Files[i][1][1]
                for j in range(len(test_file_sentences)):
                        s=unicode(test_file_sentences[j])
                        doc=nlp(s, entity=False)
                        ner(doc)
                        print("Entites on fine tuned NER:")
                        for word in doc:
                              print(word.text, word.orth, word.lower, word.tag_, word.ent_type_, word.ent_iob)
                       

#Prints files content
def printFiles(files):
	for i in range(len(files)):
		print("\n\n\n")
		print("#################Filename####################")
		print(files[i][0]) #prints name of file i
		print("#################Raw_Text####################")
		print(files[i][1][0]) #prints text for file i
		print("Parsed sentences-----------------------------")
		printList(files[i][1][1],2)
		print("Important words------------------------------")
		printList(files[i][1][2],2)
		print("Tagger output------------------------------")
		printList(files[i][1][3],2)
		print("Answers--------------------------------------")
		print(files[i][2][0]) #prints answer for the file i
		print("Answers_in_array_form------------------------")
		printList(files[i][2][1],0) #prints answer array for the file i

#Function#########################################################
#Creates patterns of form: [verb, POS, type_of_attribute, frequency]
#Work in progress
def paternize(files):
	tags = []
	ans = []
	sentences = []
	imp = []
	raw = []
	pos = []
	vps = []

	#Pattern format: [verb, POS, type_of_attribute]
	patterns = []

	'''
	long_patterns=[]
        nlp = spacy.load('en')
	for i in range(len(files)):
            for j in range(len(files[i][1][2])):
                if len(files[i][1][2][j])!=0:
                    doc=nlp(unicode(files[i][1][1][j]))
                    for np in doc.noun_chunks:
                        for k in range(len(files[i][1][2][j])):
                                if files[i][1][2][j][k][0]==np.text or files[i][1][2][j][k][0] in np.text or np.text in files[i][1][2][j][k][0] :
                                    for answer_entry in files[i][2][1]:
                                        if files[i][1][2][j][k][0]==answer_entry[1][0]:
                                            verb=np.root.head.text
                                            
                                            wordindex=word_index(verb, files[i][1][1][j])
                                            if wordindex!=None:
                                                verb=doc[wordindex]
                                                span=doc[verb.left_edge.i:verb.right_edge.i+1]
                                                long_patterns.append([span.text, np.root.dep_, answer_entry[0]])
                

        print "now print long_patterns. ########################################################"                                                                                				
	printList(long_patterns,0)

        long_patterns_verb=[]
        
        for i in range(len(files)):
            for j in range(len(files[i][1][2])):
                if len(files[i][1][2][j])!=0:
                    verbphrase=[]
                    doc=nlp(unicode(files[i][1][1][j]))
                    for word in doc:
                            if word.pos_.encode('utf-8')=='VERB':
                                    verbphrase.append(word)
                    long_patterns_verb.append(verbphrase)
                
        printList(long_patterns_verb,0)
	'''


 
	for i in range(len(files)):
		tags.append(files[i][1][3])
		pos.append(files[i][1][4])
		vps += files[i][1][5]
		#print(tags)
		ans.append(files[i][2][1])
		sentences.append(files[i][1][1])
		imp.append(files[i][1][2])
		raw.append(files[i][1][0])
		#print(tags[i])
		#print(ans[i])
	#print(vps)
	vps = list(set(vps))
	#print(vps)

	triggers, words = findTriggers(sentences, imp, ans, raw, vps)

	'''
	for i in range(len(tags)):
		answs = ans[i]
		for sent in tags[i]:
			verbs = []
			for np in sent:
				if np[2] == 'nsubj' or np[2] == 'dobj':
					
					if np[2] not in verbs:
						verbs.append(np[2])

			for np in sent:
				noun = np[0]
				for answer in answs:
					#print(answer)
					for j in range(1,len(answer)):
						for entry in answer[j]:
							#print(entry)
							if entry in noun:
								
								if np[2] == 'nsubj' or np[2] == 'dobj':
									patterns.append([np[3], np[2], answer[0]])
								else:
									for v in verbs:
										patterns.append([v, np[2], answer[0]])
	'''
	for i in range(len(tags)):
		answs = ans[i]
		for j in range(len(tags[i])):
			sent = tags[i][j]
			senti = sentences[i][j]
			verbs = []
			trigs = {}
			for np in sent:
				if np[2] == 'nsubj' or np[2] == 'dobj':
					if np[2] not in verbs:
						verbs.append(np[2])
			for trig in triggers:
				#print(trig + "####" + senti)
				if trig[0] in senti and trig[0] not in trigs:
					trigs[trig[0]] = 1
			
			for np in sent:
				noun = np[0]
				for answer in answs:
					#print(answer)
					for j in range(1,len(answer)):
						for entry in answer[j]:
							#print(entry)
							if entry in noun:
								for trig in trigs:
									patterns.append([trig, np[2], answer[0]])

	pats = []

	for pat in patterns:
		inPats = -1
		for i in range(len(pats)):
			if pat == pats[i][0:3]:
				inPats = i
		if inPats >= 0:
			pats[i][3] += 1
		else:
			p = list(pat)
			p.append(1)
			pats.append(p)

	pats = sorted(pats, key=lambda x: x[3], reverse=True)

	uniquePats = []

	for pat in pats:
		repeated = False
		for i in range(len(uniquePats)):
			if pat[0:2] == uniquePats[i][0:2]:
				repeated = True
		if not repeated:
			uniquePats.append(pat)
	
	#printList(uniquePats, 0)
	#print(len(pats))
	#print(len(uniquePats))
	return uniquePats, triggers, words

def findTriggers(sents, ans, ans2, raw, vps):
	sinc = []
	swe = []
	sind = []
	sorg = []
	star = []
	svic = []

	allWeaponsDic = {}
	allORGDic={}

	for i in range(len(sents)):
		if ans2[i][1][0] == "INCIDENT":
			sinc.append([raw[i], ans2[i][1][1][0]])
		for j in range(len(sents[i])):
			sent = sents[i][j]
			an = ans[i][j]
			if len(an) > 0:
				#print(an[0])
				for answer in an:
					if answer[2] == "WEAPON":
						swe.append(sent)
						#print(answer)
						if answer[0] not in allWeaponsDic:
							allWeaponsDic[answer[0]] = 1
						else:
							allWeaponsDic[answer[0]] += 1
					elif answer[2] == "PERP INDIV":
						sind.append(sent)
					elif answer[2] == "PERP ORG":
						sorg.append(sent)
						#print(answer)
						if answer[0] not in allORGDic:
							allORGDic[answer[0]] = 1
						else:
							allORGDic[answer[0]] += 1
							
					elif answer[2] == "TARGET":
						star.append(sent)
					elif answer[2] == "VICTIM":
						svic.append(sent)

	allWeapons = []
	for key in allWeaponsDic:
		allWeapons.append([key, allWeaponsDic[key]])

	allWeapons = sorted(allWeapons, key=lambda x: x[1], reverse=True)	

	saveWeaps(allWeapons)

        allORGs = []
	for key in allORGDic:
		allORGs.append([key, allORGDic[key]])

	allORGs = sorted(allORGs, key=lambda x: x[1], reverse=True)	

	saveORGs(allORGs)


	#printList(allWeapons,0)

	stops = ["ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE","TEN", "TEXT"]
	file = open("developset/stopwords.txt", 'r')
	for line in file:
		stops.append(line.rstrip('\n').upper())

	for el in list(set(stopwords.words('english'))):
		stops.append(el.upper())

	#printList(sinc, 2)
	incident = incidentDet(sinc, stops, sents,"INCIDENT", vps)
	#print(swe)
	weapon = trigsCat(swe, stops, sents,"WEAPON", vps)
	indiv= trigsCat(sind, stops, sents,"PERP INDIV", vps)
	org = trigsCat(sorg,stops, sents,"PERP ORG", vps)
	target =  trigsCat(star,stops, sents, "TARGET", vps)
	victim = trigsCat(svic,stops, sents,"VICTIM", vps)
	
	printList(incident,0)
	print("###################################")
	allTrigs = weapon + indiv + org + target + victim
	#print(allTrigs)

	return allTrigs, incident

def saveWeaps(weapons):
	file = open("output/weapons.txt", "w")
	for w in weapons:
		file.write(w[0] + "/" + str(w[1]) + "\n")
def saveORGs(ORGs):
	file = open("output/ORGs.txt", "w")
	for w in ORGs:
		file.write(w[0] + "/" + str(w[1]) + "\n")


def tokNtag(pos, ind):
	token=[]
	tagged=[]
	for p in pos[ind]:
		token.append(p[0])
		tagged.append(p[1])
	return token,
	
def incidentDet(relSents, stops, sents,typ, vps):
	relWords = {}
	for i in range (len(relSents)):
		relSents[i][0] = re.sub('\n', ' ', relSents[i][0])
		relSents[i][0] = nltk.sent_tokenize(relSents[i][0])

	types = []
	for i in range (len(relSents)):
		sentes = relSents[i][0]
		ty = relSents[i][1]
		if ty not in types:
			types.append(ty)
		for sentence in sentes:
			tokens = nltk.word_tokenize(sentence)
			'''
			tagged = nltk.pos_tag(tokens)
			for i in range(len(tokens)):
				token = tokens[i]
				tag = tagged[i]
				if tag[1].startswith("VB"):
			'''
			for token in tokens:
				if token.isalpha() and token not in stops and token not in relWords:
					relWords[token] = [1, ty]
				elif token.isalpha() and token not in stops:
					relWords[token][0] += 1
					#print(token + " " + ty)

	allWords = {}

	for i in range (len(relSents)):
		sentes = relSents[i][0]
		ty = relSents[i][1]
		
		for sentence in sentes:
			tokens = nltk.word_tokenize(sentence)
			for token in tokens:
				for incs in types:
					if incs != ty and token.isalpha() and token not in stops and token+ty not in allWords:
						allWords[token+ty] = 1
					elif incs != ty and token.isalpha() and token not in stops:
						allWords[token+ty] += 1
						#print(token + " " + ty)


	#printDic(allWords)
	trigs = []

	for key in relWords:
		denom = 0
		for t in types:
			if t is not relWords[key][1] and key+t in allWords:
				denom += float(allWords[key+t])
		if denom is not 0:
			trigs.append([key,round(float(relWords[key][0])/denom * math.log(allWords[key+relWords[key][1]]),4),relWords[key][1]])

	#printList(trigs, 0)

	trigs = sorted(trigs, key=lambda x: x[1], reverse=True)

	ctrigs = []
	count = {}
	c = {}
	for t in types:
		count[t] = 0
		c[t] = 0
	for t in trigs:
		#if (len(ctrigs) < 11 or t[1] > 1.0) and count[t[2]] < 40:
		if t[1] > 1.0:
			ctrigs.append([t[0], t[2],t[1]])
			count[t[2]]+=1
			c[t[2]] += t[1]
	#printList(ctrigs, 0)
	for i in range (len(ctrigs)):
		ctrigs[i][2] = ctrigs[i][2]/float(c[ctrigs[i][1]])
	printList(types,0)
	#print(ctrigs)
	return ctrigs

def printDic(dic):
	for key in dic:
		print(key + " = " + str(dic[key]))

def trigsCat(relSents, stops, sents,typ, pos):
	relWords = {}

	for i in range(len(relSents)):
		sentence = relSents[i]
		tokens = nltk.word_tokenize(sentence)
		for i in range(len(tokens)):
			token = tokens[i]
			if token.isalpha() and token not in stops and token not in relWords:
				relWords[token] = 1
			elif token.isalpha() and token not in stops:
				relWords[token] += 1

	allWords = {}

	for senta in sents:
		for sentence in senta:
			tokens = nltk.word_tokenize(sentence)
			for i in range(len(tokens)):
				token = tokens[i]
				if token.isalpha() and token not in stops and token not in allWords:
					allWords[token] = 1
				elif token.isalpha() and token not in stops:
					allWords[token] += 1

	trigs = []

	for key in relWords:
		trigs.append([key,round(float(relWords[key])/float(allWords[key]) * math.log(allWords[key]),4)])

	trigs = sorted(trigs, key=lambda x: x[1], reverse=True)

	ctrigs = []
	for t in trigs:
		if len(ctrigs) < 11 or t[1] > 1.5:
			ctrigs.append([t[0], typ])

	#print(ctrigs)
	return ctrigs
	
#Function#########################################################
#Prints items in array
def printList(sentences,skip):
	for i in range(len(sentences)):
		sentence = sentences[i]
		if skip == 2:
			print(str(i) + " " + str(sentence))
		else:
			print(sentence)
		if skip:
			print("")

#Function#########################################################
#Processes the test in various ways to then store them back into the array
#It does it without losing anything
def processFiles(dirtxt, dirans, startswith):
	#Reads and parses the files into the following format
	#files = [file_index 0-i] 
	#		 [0 = filename, 1 = text_file, 2 = answers_file] 
	#		 [0 = plain_text]
	files = readAndParseFile(dirtxt, dirans, startswith)

	#Parses the answers so they fit in array in files[i][2][1]
	files = parseAnswers(files)

	#Extracts sentences in files[i][1][1]
	files = extractSentences(files)

	return files

#Function#########################################################
#Function breaks down files into an array of sentences contained in files[i][1][1]
#Also includes entities in files[i][1][2]
def extractSentences(files):
	#nlp = spacy.load('en')
	for i in range(len(files)):
		#print("Processing " + str(i) +"/" + str(len(files)) + " files")
		file = files[i][1][0]
		sentences = nltk.sent_tokenize(file)[0:]
		sentenceEntities = []
		sentenceImp = []
		sentenceTagged = []
		veps = []
		for j in range(len(sentences)):
			sentences[j] = re.sub('\n', ' ', sentences[j])
			#tokens = nltk.word_tokenize(sentences[j])
			#tagged = nltk.pos_tag(tokens)
			'''
			doc=nlp(unicode(sentences[j].lower()))
			
			chunks = []
			for np in doc.noun_chunks:
				chunk = []
				chunk.append(unicodedata.normalize('NFKD', np.text.upper()).encode('ascii','ignore'))
				chunk.append(unicodedata.normalize('NFKD', np.root.text.upper()).encode('ascii','ignore'))
				chunk.append(unicodedata.normalize('NFKD', np.root.dep_).encode('ascii','ignore'))
				chunk.append(unicodedata.normalize('NFKD', np.root.head.text.upper()).encode('ascii','ignore'))
				chunks.append(chunk)
			'''


			##################Test lab##########################
			#print('\n' + sentences[j])
			tokens = nltk.word_tokenize(sentences[j].lower())
			tagged = nltk.pos_tag(tokens)
			sentenceTagged.append(tagged)
			#print(tagged)
			tags = []
			for k in range(len(tagged)):
				tags.append([tagged[k][0].upper(),tagged[k][1]])
			#print(tags)
			verbsAndPos = []
			k=0
			while k < len(tags):
				t = tags[k]
				s = k
				vs = []
				if t[1][0:2] == 'VB' and t[0].isalpha() and not t[0].endswith("ING"):
					which = False
					if k-1 >= 0 and tags[k-1][0] == "WHICH":
						which = True
					vs.append(t[0])
					k+=1
					while k < len(tags) and tags[k][1][0:2] == 'VB' and tags[k][0].isalpha():
						vs[0] = vs[0] + " " + tags[k][0]
						k+=1
					while k < len(tags) and tags[k][0] != ',' and tags[k][0] != ':' and tags[k][0] != ';':
						k+=1
					vs.append(k)
					vs.append(s)
					vs.append(not which)
				if len(vs) > 0 and len(vs[0]) > 0:
					verbsAndPos.append(vs)
				k+=1
			if len(verbsAndPos) > 0:
				verbsAndPos[len(verbsAndPos)-1][1] = len(tags)-1

			chunks2 = []
			k=0
			vps = []
			
			while k < len(tags):
				t = tags[k]
				s = k
				vs = []
				vp = ''
				if (t[1][0:2] == 'VB') and t[0].isalpha() and not t[0].endswith("ING"):
					prep = t[0]
					vp = t[0]
					k+=1
					while k < len(tags) and (tags[k][1][0:2] == 'VB')and tags[k][0].isalpha():
						vp = vp + " " + tags[k][0]
						k+=1
					#print(vp)
					vps.append(vp)
				elif (t[1][0:2] == 'IN') and t[0].isalpha():
					prep = t[0]
					vs.append("")
					vs.append("")
					k+=1
					while k < len(tags) and (tags[k][1][0:2] == 'NN' or tags[k][1][0:2] == 'JJ'  or tags[k][1][0:2] == 'JJ')and tags[k][0].isalpha():
						vs[0] = vs[0] + " " + tags[k][0]
						k+=1
					vs.append(prep.lower())
					vs.append(retVerb(k, verbsAndPos))
				elif (t[1][0:2] == 'NN' or t[1][0:2] == 'DT') and t[0].isalpha():
					vs.append(t[0])
					vs.append(t[0])
					k+=1
					while k < len(tags) and (tags[k][1][0:2] == 'NN' or tags[k][1][0:2] == 'JJ'  or tags[k][1][0:2] == 'JJ')and tags[k][0].isalpha():
						vs[0] = vs[0] + " " + tags[k][0]
						k+=1
					vs.append(subobj(k, verbsAndPos))
					vs.append(retVerb(k, verbsAndPos))
					'''
					if (so(k, verbsAndPos)):
						print(verbsAndPos)
						print(sentences[j])
						print(vs)
						print('\n')
					'''
				if len(vs) > 0:
					chunks2.append(vs)
				if k == s:
					k+=1
			veps = veps + vps
			#print(verbsAndPos)
			#printList(chunks,0)
			#print("Chunks2")
			#printList(chunks2,0)

			#[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
			#####################################################
			#sentenceEntities.append(sub_toks)
			'''
			entities = nltk.chunk.ne_chunk(tagged)
			sentenceEntities.append(entities)'''
			sentenceEntities.append(chunks2)
			
			impWords = []
			for important in files[i][2][1]:
				for k in range(1, len(important)):
					for l in range(len(important[k])):
						if not important[k][l].startswith("DEV") and important[k][l] != '-' and important[k][l] in sentences[j]:
							impWords.append([important[k][l], find_indexes(important[k][l], sentences[j]), important[0]])
			sentenceImp.append(impWords)
			

		files[i][1].append(sentences)
		#files[i][1].append(sentenceEntities)
		files[i][1].append(sentenceImp)
		files[i][1].append(sentenceEntities)
		files[i][1].append(sentenceTagged)
		files[i][1].append(veps)
	return files

def retVerb(index, verbpos):
	if len(verbpos) == 0:
		return ""
	verb = verbpos[len(verbpos) - 1][0]
	for i in range(len(verbpos)-1, -1, -1):
		el = verbpos[i]
		#print(el)
		#print(index)
		if index <= el[1]:
			verb = el[0]
			#print(verb)
	#print(index)
	#print(verb)
	return verb

def passive(verb):
	v = verb.split(" ")
	#print(v)
	if len(v) > 1 and ((v[0] == "WAS" or v[0] == "IS") and not v[1].endswith("ING")):
		return True
	return False

def subobj(index, verbpos):
	if len(verbpos) == 0:
		return "nsubj"
	verb = True
	v = False
	for el in verbpos:
		if index <= el[1] and index > el[2]:
			verb = False
			v = passive(el[0]) and el[3]
	if v and verb:
		return "dobj"
	elif not v and verb:
		return "nsubj"
	elif v and not verb:
		return "nsubj"
	elif not v and not verb:
		return "dobj"

def so(index, verbpos):
	if len(verbpos) == 0:
		return "nsubj"
	verb = True
	v = False
	for el in verbpos:
		if index <= el[1] and index > el[2]:
			verb = False
			v = passive(el[0]) and el[3]
	#return str(verb) + " " + str(v)
	return v

#Function#########################################################
#Given wor1 and wor2, returns the index where any instance of wor1 was found in wor2
def find_indexes(wor1, wor2):
	ind = []
	for i in range(len(wor2) - len(wor1)+1):
		if wor1 == wor2[i:(i+len(wor1))]:
			ind.append(i)
	return ind


#Function#########################################################
#Function parses the answers into an array of the following format contained in files[i][2][1]
#array = list of answers of the following format 
#['type of id', ['answer_1', 'alternate_answer_1'], ['answer_2', 'alternative_answer_2'], ...]
def parseAnswers(files):
	for i in range(len(files)):
		file = files[i][2][0]
		#print(file)
		templates =[]
		template = []
		file = file.splitlines()
		for line in file:
			#print(line)
			if ':' in line:
				if len(template) != 0 :
					templates.append(template)
			#print(template)
				template = []
				template.append(line.split(':')[0])
				template.append(list(filter(None,line.split(':')[1].lstrip(' ').rstrip(' ').split('/'))))
			elif line.split('/')[0] != '':
				template.append(line.lstrip(' ').rstrip(' ').split('/'))
			
			for j in range(1, len(template)):
				for k in range(len(template[j])):
					template[j][k] = template[j][k].lstrip(' ').rstrip(' ')

		templates.append(template)
		#print(template)
		files[i][2].append(templates)
	return files


#Function#########################################################
#Function reads files and returns an array of the following format
#
#files = [file_index 0-i] 
#		 [0 = filename, 1 = text_file, 2 = answers_file] 
#		 [0 = plain_text]
#
#inputs:
#Directory with texts
#Directory with answers
#What should files start with
##################################################################
def readAndParseFile(dirnametxt, dirnameans, startsw):
	txtFiles = []
	ansFiles = []
	files = []
	filedir = dirnametxt
	for filename in os.listdir(filedir):
		if filename.startswith(startsw):
			#print ("###############################################################")
			#print (filename)

			answer=find(filename, dirnameans)+".anskey"
			#print(answer)

			tfile = open(dirnametxt +"/" + filename,"r")
			afile = open(answer,"r")

			rawText = tfile.read()

			rawText = rawText[rawText.index("--"):]
			#print(rawText)

			text = [ filename ,[rawText], [afile.read()]]

			files.append(text)

	return files
	'''
	with open(answer, 'r') as input_file:
		prevrole=""
		for line in input_file:
			if ":" in line:
				linecontent=line.split(":")
				if linecontent[1].lstrip()!="-":
					role=linecontent[0]
					if "/" in linecontent[0]:
						filler_elements=linecontent[0].split("/")
						for i in range(0,len(filler_elements)):
							each_entry=filler_elements[i].lstrip().rstrip()
							create_pattern(each_entry, filedir, filename)
					else:
						each_entry=linecontent[1].lstrip().rstrip()
						create_pattern(each_entry, filedir, filename)
					prevrole=role
			else:
				content=line.lstrip().rstrip()
				if "/" in content:
					filler_elements=content.split("/")
					for i in range(0,len(filler_elements)):
						each_entry=filler_elements[i].lstrip().rstrip()
						create_pattern(each_entry, filedir, filename)
				else:
					each_entry=content.lstrip().rstrip()
					create_pattern(each_entry, filedir, filename)
				role=prevrole
	'''

def create_pattern(each_entry, filedir, txt_file_name):
	with open(filedir+"/"+txt_file_name, 'r') as textfile:
		text=textfile.read()
		sents=nltk.sent_tokenize(text)
		for i in range(0, len(sents)):
			if each_entry in sents[i]:
				#print("Hello")
				a=1
				#print (sents[i])
                #todo

def find(name, path):
	for root, dirs, files in os.walk(path):
		if name+".anskey" in files:
			return os.path.join(root, name)

def tok_format(tok):
    return "_".join([tok.orth_, tok.tag_, tok.dep_])

def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)
    
def word_index(word, sentence):
    sents=word_tokenize(sentence)
    for i in range(len(sents)):
        if sents[i]==word:
            return i
    return None


if __name__ == "__main__":
	main(sys.argv[1:])

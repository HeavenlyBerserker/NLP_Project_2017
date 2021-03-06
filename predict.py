###########################
#NLP Project 2017 predict file
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
from project import *



def main(argv):
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
	#[i][2][0] = raw answers
	#[i][2][1] = parsed answers
	#See printed output for more details

	final = 1

	devtest = 0

	t1Files = []
	
	if final == 0:
		if devtest:
			t1Files = processFiles('developset/texts', 'developset/answers', "DEV")
			processAns('developset/answers', "DEV")
		else:
			t1Files = processFiles('testset1/texts', 'testset1/answerkeys', "")
			processAns('testset1/answerkeys', "")
	
	
	#t1Files = processFiles('developset/texts', 'developset/answers', "DEV")

	patterns = readPats("output/patterns.txt")
	triggers = readTrigs("output/triggers.txt")
	words = readWords("output/words.txt")

	subjpatternlist = readPats_autoslog("output/subjpatterns.txt")
        csubjpatternlist = readPats_autoslog("output/csubjpatterns.txt")
        nsubjpasspatternlist = readPats_autoslog("output/nsubjpasspatterns.txt")
        csubjpasspatternlist = readPats_autoslog("output/csubjpasspatterns.txt")
        dobjpatternlist = readPats_autoslog("output/dobjpatterns.txt")
        pobjpatternlist = readPats_autoslog("output/pobjpatterns.txt")
        attrpatternlist = readPats_autoslog("output/attrpatterns.txt")

	#printFiles(t1Files)
	#printList(patterns, 0)
	#printList(words,0)
	#print(triggers)
	
	print(argv[0])
	files = processFilesFinal(argv[0],'')
	#printFiles2(files)

	predictions = []

	if final == 0:
		predictions = predict(t1Files, patterns, triggers, words,1, subjpatternlist, csubjpatternlist, nsubjpasspatternlist, csubjpasspatternlist, dobjpatternlist, pobjpatternlist, attrpatternlist)
	else:
		predictions = predict(files, patterns, triggers, words,0, subjpatternlist, csubjpatternlist, nsubjpasspatternlist, csubjpasspatternlist, dobjpatternlist, pobjpatternlist, attrpatternlist)

	#predictions=predict_auto_slog(t1Files, subjpatternlist, csubjpatternlist, nsubjpasspatternlist, csubjpasspatternlist, dobjpatternlist, pobjpatternlist)
	#predictions = predict(t1Files, patterns, triggers, words,0)

	writePred(predictions)

	print(argv[0])
	print("The final predictions have been written to final-predictions.txt in the NLP_Project_2017  directory.")

	


def predict(files, patterns, triggers, words, test, subjpatternlist, csubjpatternlist, nsubjpasspatternlist, csubjpasspatternlist, dobjpatternlist, pobjpatternlist, attrpatternlist):
	tags = []
	ans = []
	sentences = []
	raw = []


	for i in range(len(files)):
		tags.append(files[i][1][3])
		if test:
			ans.append(files[i][2][1])
		sentences.append(files[i][1][1])
		raw.append(files[i][1][0])

	predicts = []

        
	'''
	for i in range(len(tags)):
		predict = []
		for sentence in tags[i]:
			for entry in sentence:
				#print(entry)
				for p in patterns:
					if p[1] == entry[2] and p[0] == entry[3]:
						#predict.append([sentences[i][tags[i].index(sentence)],p[2], entry[0], entry, p])
						predict.append([p[2], entry[0]])
		predicts.append(predict)
		print("############################\nPredictions:")
		printList(predict, 0)
		print("----------------------------\nActual Answers:")
		printList(ans[i], 0)
		print("############################\n\n\n")
	'''
 
	count = 0
	right = 0
	problems = {}
	weapons = getWeaps()
	ORGs=getORGs()
	print "print weapon list"
	printList(weapons, 0)
	print "print org list"
	printList(ORGs, 0)
	for i in range(len(tags)):
		print("Working... " + str(float(i)/float(len(tags))) + "%")
		count += 1
		predict = []
		inc = predInc(raw[i], words)
		
		#if "BOMB" in raw[i] or "BOMBING" in raw[i] or "EXPLOSIVE" in raw[i] or "EXPLOSION" in raw[i]:
		#	inc = "BOMBING"
		#if "KIDNAP" in raw[i]:
		#	inc = "KIDNAPPING"
		inc, proWord = dumbGuess(raw[i])
		
		predict.append(['INCIDENT', inc])
		if test:
			if inc == ans[i][1][1][0]:
				right += 1
			else:
				if inc + " != " + ans[i][1][1][0] not in problems:
					problems[inc + " != " + ans[i][1][1][0]] = 1
				else:
					problems[inc + " != " + ans[i][1][1][0]] += 1
				#print("Wrong: " + proWord + "--"+ str(i) +"-- "+ inc + " != " + ans[i][1][1][0])
				#if inc + " != " + ans[i][1][1][0] == "ATTACK != KIDNAPPING":
				#	print(raw[i])
                weapon_count=0
		for weapon in weapons:
			if weapon[0] in raw[i] and weapon[1] > 0 and weapon_count<2:

				predict.append(['WEAPON', weapon[0]])
				weapon_count=weapon_count+1

		org_count=0
		for org in ORGs:
			if org[0] in raw[i] and org[1] > 0 and org_count<1:
				predict.append(['PERP ORG', org[0]])
				org_count=org_count+1
				

		for j in range(len(tags[i])):
			sentence = tags[i][j]
			sent = sentences[i][j]
			trigs = {}
			for trig in triggers:
				#print(trig + "####" + senti)
				if trig[0] in sent and trig[0] not in trigs:
					trigs[trig[0]] = trig[1]
			for entry in sentence:
				#print(entry)
				for p in patterns:
					for trig in trigs:
						if p[2] != "WEAPON" and p[1] == entry[2] and p[0] == trig and p[2] == trigs[trig]:
							#predict.append([sentences[i][tags[i].index(sentence)],p[2], entry[0], entry, p])
							if [p[2], entry[0]] not in predict and len(entry[0]) > 0:
								#predict.append([p[2], entry[0]])
								losAn = 0
		
		predict = clean(predict)

		predicts.append(predict)

	
        #autoslog predict
        nlp=spacy.load('en')
	sentences = []

	for i in range(len(files)):
		sentences=(files[i][1][1])
                one_doc_predict=predicts[i]
                print "one_doc_predict"
                printList(one_doc_predict, 0)
		for j in range(len(sentences)):
                        one_sent=sentences[j]
                        doc=nlp(unicode(one_sent))
                        for nc in doc.noun_chunks:
                                #print nc.text
                                #print nc.root
                                #print nc.root.dep_
                                if nc.root.dep_.encode('utf-8')=='nsubj':
                                        #print i
                                        #print 'in subj predict'
                                        #print nc.root.text.encode('utf-8')
                                        #print nc.root.head.text.encode('utf-8')
                                        #print nc.root.head.lemma_.encode('utf-8')
                                        #print nc.root.head.dep_.encode('utf-8')
                                        for each_pattern in subjpatternlist:
                                                if nc.root.head.lemma_.encode('utf-8') == 'be':
                                                        #print "nc.root.head.lemma_.encode('utf-8')"
                                                        #print each_pattern
                                                        #print nc.root.head.dep_.encode('utf-8')
                                                        
                                                        if doc[nc.root.head.i+1].text.encode('utf-8') in each_pattern:
                                                                #print "doc[nc.root.head.i+1].text.encode('utf-8')"
                                                                #print doc[nc.root.head.i+1].text.encode('utf-8')
                                                                one_predict=[each_pattern[len(each_pattern)-2], nc.text.encode('utf-8')]
                                                                one_predict=clean_one_predict(one_predict)
                                                                one_predict=clean_out_number(one_predict)
                                                                one_doc_predict.append(one_predict)
                                                
                                                else:
                                                        if nc.root.head.text.encode('utf-8') in each_pattern:
                                                                one_predict=[each_pattern[len(each_pattern)-2], nc.text.encode('utf-8')]
                                                                one_predict=clean_one_predict(one_predict)
                                                                one_predict=clean_out_number(one_predict)
                                                                one_doc_predict.append(one_predict)
                                                
                                if nc.root.dep_.encode('utf-8')=='csubj':
                                        for each_pattern in csubjpatternlist:
                                                if nc.root.head.text.encode('utf-8') in each_pattern:
                                                        one_predict=[each_pattern[len(each_pattern)-2], nc.text.encode('utf-8')]
                                                        one_predict=clean_one_predict(one_predict)
                                                        one_predict=clean_out_number(one_predict)
                                                        one_doc_predict.append(one_predict)
 
								####TO IMPROVE##############
                                if nc.root.dep_.encode('utf-8')=='nsubjpass':
                                        for each_pattern in nsubjpasspatternlist:
                                                not_exit=True
                                                current=nc.root.i+1
                                                while not_exit and current<len(doc):
                                                        if doc[current].lemma_.encode('utf-8')=="be":
                                                                if doc[current +1 ].pos_.encode('utf-8')=='VERB' and doc[current +1 ].text.encode('utf-8') in each_pattern: 
                                                                        one_predict=[each_pattern[len(each_pattern)-2], nc.text.encode('utf-8')]
                                                                        one_predict=clean_one_predict(one_predict)
                                                                        one_predict=clean_out_number(one_predict)
                                                                        one_doc_predict.append(one_predict)                                                                  
                                                                        not_exit=False
                                                        current=current+1  


                                if nc.root.dep_.encode('utf-8')=='csubjpass':
                                        for each_pattern in csubjpasspatternlist:
                                                for current in range(nc.root.i, len(doc)):
                                                        if doc[current].pos_.encode('utf-8')=='VERB' and doc[current].dep_.encode('utf-8')!='auxpass' and doc[current].text.encode('utf-8') in each_pattern:                                        
                                                                one_predict=[each_pattern[len(each_pattern)-2], nc.text.encode('utf-8')]
                                                                one_predict=clean_one_predict(one_predict)
                                                                one_predict=clean_out_number(one_predict)
                                                                one_doc_predict.append(one_predict)
                        
                                if nc.root.dep_.encode('utf-8')=='dobj':
                                        for each_pattern in dobjpatternlist:
                                                not_exit=True
                                                current=nc.root.i-1
                                                while not_exit and current>=0:
                                                        if doc[current].pos_.encode('utf-8')=="VERB":
                                                                if doc[current].lemma_.encode('utf-8') in each_pattern:
                                                                        one_predict=[each_pattern[len(each_pattern)-2], nc.text.encode('utf-8')]
                                                                        one_predict=clean_one_predict(one_predict)
                                                                        one_predict=clean_out_number(one_predict) 
                                                                        one_doc_predict.append(one_predict)                                                                       
                                                                not_exit=False
                                                        current=current-1
                                                        

                                if nc.root.dep_.encode('utf-8')=='pobj' and nc.root.ent_type_.encode('utf-8')!='DATE':
                                        for each_pattern in pobjpatternlist:
                                                current=nc.root.left_edge.i-1

                                                if (doc[current].dep_.encode('utf-8')=="prep" or doc[current].pos_.encode('utf-8')=="ADP") and doc[current].text.encode('utf-8') in each_pattern and doc[current-1].text.encode('utf-8') in each_pattern:
                                                        one_predict=[each_pattern[len(each_pattern)-2], nc.text.encode('utf-8')]
                                                        one_predict=clean_one_predict(one_predict)
                                                        one_predict=clean_out_number(one_predict)
                                                        one_doc_predict.append(one_predict)

                                                
                                                '''
                                                not_exit=True
                                                current=nc.root.i-1
                                                while not_exit and current>=0:
                                                        if (doc[current].dep_.encode('utf-8')=="prep" or doc[current].pos_.encode('utf-8')=="ADP") and doc[current].text.encode('utf-8') in each_pattern and doc[current-1].text.encode('utf-8') in each_pattern:
                                                                one_predict=[each_pattern[len(each_pattern)-2], nc.text.encode('utf-8')]
                                                                one_predict=clean_one_predict(one_predict)
                                                                one_predict=clean_out_number(one_predict)
                                                                one_doc_predict.append(one_predict)
                                                                not_exit=False
                                                        current=current-1
                                                '''

                                if nc.root.dep_.encode('utf-8')=='attr':
                                        for each_pattern in attrpatternlist:
                                                if nc.root.head.lemma_.encode('utf-8') == 'be':
                                                        if doc[nc.root.head.i-1].text.encode('utf-8')=='TARGET':
                                                                one_predict=['TARGET', nc.text.encode('utf-8')]
                                                                one_predict=clean_one_predict(one_predict)
                                                                one_predict=clean_out_number(one_predict)
                                                                one_doc_predict.append(one_predict)

                                                        if doc[nc.root.head.i-1].text.encode('utf-8')=='VICTIM':
                                                                one_predict=['VICTIM', nc.text.encode('utf-8')]
                                                                one_predict=clean_one_predict(one_predict)
                                                                one_predict=clean_out_number(one_predict)
                                                                one_doc_predict.append(one_predict)

                                                        if doc[nc.root.head.i-1].text.encode('utf-8')=='PERPETRATOR':
                                                                one_predict=['PERP INDIV', nc.text.encode('utf-8')]
                                                                one_predict=clean_one_predict(one_predict)
                                                                one_predict=clean_out_number(one_predict)
                                                                one_doc_predict.append(one_predict)
                                                                
                                                

                                                     
                '''
		if test:
			print("############################\nPredictions:")
			printList(predict, 0)
			if not test:
				print("----------------------------\nActual Answers:")
				printList(ans[i], 0)
			if not test:
				print("---------------------\nAnswers included in predictors")
				prediRightPred(predict, ans[i])
				print("---------------------\nAnswers predictor got right")
				prediRight(predict, ans[i])
				print("---------------------")
			print("############################\n\n\n")
		'''
			
        predicts=clean_duplicate_in_predicts(predicts)



	keeplose = "111111"
	predicts = purgePredicts(predicts, keeplose)

	print "print predicts #####################################################"

        printList(predicts,0)

        
	problematic = []
	for key in problems:
		problematic.append([key, problems[key]])

	problematic = sorted(problematic, key=lambda x: x[1], reverse=True)
	if test:
		print("Right = " + str(right) + "/" + str(count))
		printList(problematic, 0)

	predictions = textifyPreds(predicts, files)
	
		#print(out)

	return predictions


def purgePredicts(predicts, ar):
	cats = {"INCIDENT": 0, "WEAPON":1, "PERP INDIV":2,"PERP ORG":3, "TARGET":4, "VICTIM":5}

	newpred = []

	for file in predicts:
		pred = []
		for predic in file:
			if ar[cats[predic[0]]] == '1':
				pred.append(predic)
		newpred.append(pred)

	return newpred

def getWeaps():
	file = open("output/weapons.txt", "r")
	weaps = []
	for line in file:
		if len(line) > 0:
			sp = line.rstrip("\n").split("/")
			weaps.append([sp[0], int(sp[1])])
	return weaps

def getORGs():
	file = open("output/ORGs.txt", "r")
	ORGs = []
	for line in file:
		if len(line) > 0:
			sp = line.rstrip("\n").split("/")
			ORGs.append([sp[0], int(sp[1])])
	return ORGs


#Write predict file
def writePred(predictions):
	predictions = sorted(predictions)
	file = open("final-predictions.txt", 'w')
	for line in predictions:
		file.write(line + "\n")

#Reads triggers from a file
def readTrigs(name):
	trigs = []
	file = open(name, 'r')
	for line in file:
		trigs.append(line.rstrip('\n').upper().split('/'))
	return trigs

#Reads words from a file
def readWords(name):
	trigs = []
	file = open(name, 'r')
	for line in file:
		temp = line.rstrip('\n').upper().split('/')
		#print(temp)
		temp[2] = float(temp[2])
		trigs.append(temp)
	return trigs


def dumbGuess(text):
	inc = "ATTACK"
	word = "        "
	b = ["EXPLODED", "EXPLOSION", "CAR BOMB", "DYNAMITE", "BY A BOMB", "PLACED A BOMB", "DETONATED", "TNT"]
	k = ["KIDNAPPED", "KIDNAPPING OF","TOOK HOSTAGE", "HOSTAGE"]
	a = ["SET FIRE", "BURNING"]
	atta = ["MACHINEGUN"]


	for w in a:
		if w in text:
			inc = "ARSON"
			word = w

	for w in b:
		if w in text:
			inc = "BOMBING"
			word = w

	for w in k:
		if w in text:
			inc = "KIDNAPPING"
			word = w

	for w in atta:
		if w in text:
			inc = "ATTACK"
			word = w

	for w in a:
		if w in text:
			inc = "ARSON"
			word = w

	return inc, word

def clean_duplicate_in_predicts(predicts):
        newcleanpredicts=[]
        for each_doc in predicts:
                each_doc=clean_one_doc_predict(each_doc)
                newcleanpredicts.append(each_doc)               
        return newcleanpredicts


def clean_one_doc_predict(each_doc_predict):
        cleanpredict=[]
        for p in each_doc_predict:
                inCP=-1
                for i in range(len(cleanpredict)):
                        if p == cleanpredict[i]:
                                inCP=i
                if inCP == -1:
                         cleanpredict.append(p)
        return cleanpredict
                                



                
def clean_one_predict(one_predict):

        strip_count=0
                
        while strip_count<3:
                if one_predict[1][0:2]=="A ":
                        one_predict[1]=one_predict[1].lstrip("A ")
                if one_predict[1][0:3]=="AN ":
                        one_predict[1]=one_predict[1].lstrip("AN ")
                if one_predict[1][0:3] == "THE":
                        one_predict[1] = one_predict[1].lstrip("THE")
        	if one_predict[1][0:4] == "ONE ":
                        one_predict[1] = one_predict[1].lstrip("ONE ")       
                if one_predict[1][0:4] == "TWO ":
                        one_predict[1] = one_predict[1].lstrip("TWO ")
                if one_predict[1][0:6] == "THREE ":
                        one_predict[1] = one_predict[1].lstrip("THREE ")
                if one_predict[1][0:5] == "FOUR ":
                        one_predict[1] = one_predict[1].lstrip("FOUR ")
                if one_predict[1][0:5] == "FIVE ":
                        one_predict[1] = one_predict[1].lstrip("FIVE ")
                if one_predict[1][0:4] == "SIX ":
                        one_predict[1] = one_predict[1].lstrip("SIX ")
                if one_predict[1][0:6] == "SEVEN ":
                        one_predict[1] = one_predict[1].lstrip("SEVEN ")
                if one_predict[1][0:6] == "EIGHT ":
                        one_predict[1] = one_predict[1].lstrip("EIGHT ")
                if one_predict[1][0:5] == "NINE ":
                        one_predict[1] = one_predict[1].lstrip("NINE ")
                if one_predict[1][0:4] == "TEN ":
                        one_predict[1] = one_predict[1].lstrip("TEN ")
                if one_predict[1][0:1] == " ":
                        one_predict[1] = one_predict[1].lstrip(" ")
                        
                strip_count=strip_count+1
                        
	return one_predict

def clean_out_number(one_predict):
        nlp=spacy.load('en')
        predicted_words=one_predict[1].split(" ")
        string_length=len(predicted_words[0])
        word=nlp(unicode(predicted_words[0]))
        if word[0].pos_.encode('utf-8')=='NUM':
                one_predict[1]=one_predict[1][string_length+1:]
        return one_predict
        


def clean(predict):
	npredict = []

	for i in range(len(predict)):
		right = True
		if predict[i][1][0:1] == " ":
			predict[i][1] = predict[i][1].lstrip(" ")
		if predict[i][1][0:2] == "A ":
			predict[i][1] = predict[i][1].lstrip("A ")
		if predict[i][1][0:4] == "THE ":
			predict[i][1] = predict[i][1].lstrip("THE ")
		if predict[i][1] == "THE" or predict[i][1] == "A":
			right = False
		if predict[i][0] == "VICTIM":
			if predict[i][1] == 'ATTACK':
				right = False
		if right and predict[i] not in npredict:
			npredict.append(predict[i])

	npredict = sorted(npredict, key=lambda x: x[0], reverse=True)
	#print(npredict)

	return npredict

def textifyPreds(predicts, files):
	predictions = []
	for i in range(len(predicts)):
		ent = predicts[i]
		Id = files[i][0]
		incident = []
		weapon = []
		indiv = []
		org = []
		target = []
		victim = []
		out = ''
		for entry in ent:
			if entry[0] == "INCIDENT":
				incident.append(entry[1])
			if entry[0] == "WEAPON":
				weapon.append(entry[1])
			if entry[0] == "PERP INDIV":
				indiv.append(entry[1])
			if entry[0] == "PERP ORG":
				org.append(entry[1])
			if entry[0] == "TARGET":
				target.append(entry[1])
			if entry[0] == "VICTIM":
				victim.append(entry[1])
		out += '\nID:             ' + Id + '\nINCIDENT:       '
		if len(incident) > 0:
			out += incident[0]
		else:
			out += '-'
		for j in range(1,len(incident)):
			out += "\n                " + indicent[j]
		out += '\nWEAPON:         '
		if len(weapon) > 0:
			out += weapon[0]
		else:
			out += '-'
		for j in range(1,len(weapon)):
			out += "\n                " + weapon[j]
		out += '\nPERP INDIV:     '
		if len(indiv) > 0:
			out += indiv[0]
		else:
			out += '-'
		for j in range(1,len(indiv)):
			out += "\n                " + indiv[j]
		out += '\nPERP ORG:       '
		if len(org) > 0:
			out += org[0]
		else:
			out += '-'
		for j in range(1,len(org)):
			out += "\n                " + org[j]
		out += '\nTARGET:         '
		if len(target) > 0:
			out += target[0]
		else:
			out += '-'
		for j in range(1,len(target)):
			out += "\n                " + target[j]
		out += '\nVICTIM:         '
		if len(victim) > 0:
			out += victim[0]
		else:
			out += '-'
		for j in range(1,len(victim)):
			out += "\n                " + victim[j]

		predictions.append(out)
		#print(out)
	return predictions

def prediRight(predict, answer):
	for item in answer:
		typ = item[0]
		for i in range(2, len(item)):
			ansor = item[i]
			for ans in ansor:
				for pred in predict:
					if ans == pred[1] and typ == pred[0]:
						print(pred)

def prediRightPred(predict, answer):
	for item in answer:
		typ = item[0]
		for i in range(1, len(item)):
			ansor = item[i]
			for ans in ansor:
				for pred in predict:
					if ans == pred[1] or ans in pred[1] or pred[1] in ans:
						print(pred)

def readPats_autoslog(filename):
	file = open(filename, 'r')

	pat = []

	for line in file:
		temp = line.split('/')
		length=len(temp)
		#temp[3] = int(temp[length-1].rstrip('\n'))
		#print(temp)
		pat.append(temp)

	return pat

def readPats(filename):
	file = open(filename, 'r')

	pat = []

	for line in file:
		temp = line.split('/')
		temp[3] = int(temp[3].rstrip('\n'))
		#print(temp)
		pat.append(temp)

	return pat

def predInc(text, words):
	#print(text)
	tokens = nltk.word_tokenize(text)
	#print(tokens)
	incs = {}
	for word in words:
		if word[1] not in incs:
			incs[word[1]] = 0
	for token in tokens:
		for word in words:
			if token == word[0]:
				incs[word[1]]+=word[2]

	#print(incs)
	maxval = 0
	maxlab = 0
	for key in incs:
		if incs[key] > maxval:
			maxval = incs[key]
			maxlab = key
	#print(maxlab)
	return maxlab

#Function#########################################################
#Processes the test in various ways to then store them back into the array
#It does it without losing anything
def processFilesFinal(filein, filean):
	#Reads and parses the files into the following format
	#files = [file_index 0-i] 
	#		 [0 = filename, 1 = text_file, 2 = answers_file] 
	#		 [0 = plain_text]
	files = readAndParseFileFinal(filein, filean)

	#Extracts sentences in files[i][1][1]
	files = extractSentences2(files)

	return files

def readAndParseFileFinal(filein, filean):
	txtFiles = []
	ansFiles = []
	files = []
	
	
			#print ("###############################################################")
			#print (filename)

	#print(answer)

	tfile = open(filein,"r")

	rawText = tfile.read()

	words = nltk.word_tokenize(rawText)

	rawText = []
	good = ''
	for word in words:
		if (word.startswith("DEV-MUC") or word.startswith("TST1-MUC") or word.startswith("TST2-MUC")) and len(good) > 1:
			rawText.append([good[good.index("--"):],filter(None,good.split(" "))[0]])
			#print(word)

			good = ''
		good += ' ' + word
	#print(filter(None,good.split(" "))[0])
	rawText.append([good[good.index("--"):],filter(None,good.split(" "))[0]])
	#print(rawText)

	for f in rawText:
		text = [ f[1] ,[f[0]]]

		files.append(text)

	#print(files)
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

def extractSentences2(files):
	nlp = spacy.load('en')
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
			doc=nlp(unicode(sentences[j].lower()))
			
			chunks = []
			for np in doc.noun_chunks:
				chunk = []
				chunk.append(unicodedata.normalize('NFKD', np.text.upper()).encode('ascii','ignore'))
				chunk.append(unicodedata.normalize('NFKD', np.root.text.upper()).encode('ascii','ignore'))
				chunk.append(unicodedata.normalize('NFKD', np.root.dep_).encode('ascii','ignore'))
				chunk.append(unicodedata.normalize('NFKD', np.root.head.text.upper()).encode('ascii','ignore'))
				chunks.append(chunk)


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
			'''
			impWords = []
			for important in files[i][2][1]:
				for k in range(1, len(important)):
					for l in range(len(important[k])):
						if not important[k][l].startswith("DEV") and important[k][l] != '-' and important[k][l] in sentences[j]:
							impWords.append([important[k][l], find_indexes(important[k][l], sentences[j]), important[0]])
			sentenceImp.append(impWords)
			'''
			

		files[i][1].append(sentences)
		#files[i][1].append(sentenceEntities)
		files[i][1].append(sentenceImp)
		files[i][1].append(sentenceEntities)
		files[i][1].append(sentenceTagged)
		files[i][1].append(veps)
	return files

#Prints files content
def printFiles2(files):
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

def processAns(dirnameans, startsw):
	txtFiles = []
	ansFiles = []
	files = []
	filedir = dirnameans
	for filename in os.listdir(filedir):
		if filename.startswith(startsw):
			#print ("###############################################################")
			#print (filename)

			answer = dirnameans +"/"+ filename
			#print(answer)

			afile = open(answer,"r")

			rawText = afile.read()

			files.append(rawText)
	files = sorted(files)
	f = open("scoring program/" + startsw+ ".txt", 'w')
	f.write('\n')
	for text in files:
		f.write(text)

	return files

if __name__ == "__main__":
	main(sys.argv[1:])

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
from spacy.en import English
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

	t1Files = processFiles('developset/texts', 'developset/answers', argv[0])
	processAns('developset/answers', argv[0])
	#t1Files = processFiles('developset/texts', 'developset/answers', "DEV")

	patterns = readPats("output/patterns.txt")
	triggers = readTrigs("output/triggers.txt")
	words = readWords("output/words.txt")

	#printFiles(t1Files)
	#printList(patterns, 0)
	#printList(words,0)
	#print(triggers)

	
	
	files = processFilesFinal("sample-textfile.txt",'')
	#printFiles2(files)

	predictions = predict(t1Files, patterns, triggers, words,0)
	#predictions = predict(t1Files, patterns, triggers, words,0)

	writePred(predictions)

	print(argv)

#Write predict file
def writePred(predictions):
	predictions = sorted(predictions)
	file = open("scoring program/predictions.txt", 'w')
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

def predict(files, patterns, triggers, words, test):
	tags = []
	ans = []
	sentences = []
	raw = []

	for i in range(len(files)):
		tags.append(files[i][1][3])
		if not test:
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
	for i in range(len(tags)):
		count += 1
		predict = []
		inc = predInc(raw[i], words)
		'''if "BOMB" in raw[i] or "BOMBING" in raw[i] or "EXPLOSIVE" in raw[i] or "EXPLOSION" in raw[i]:
			inc = "BOMBING"
		if "KIDNAP" in raw[i]:
			inc = "KIDNAPPING"'''
		inc, proWord = dumbGuess(raw[i])
		
		predict.append(['INCIDENT', inc])
		if not test:
			if inc == ans[i][1][1][0]:
				right += 1
			else:
				if inc + " != " + ans[i][1][1][0] not in problems:
					problems[inc + " != " + ans[i][1][1][0]] = 1
				else:
					problems[inc + " != " + ans[i][1][1][0]] += 1
				print("Wrong: " + proWord + "--"+ str(i) +"-- "+ inc + " != " + ans[i][1][1][0])
				if inc + " != " + ans[i][1][1][0] == "ATTACK != KIDNAPPING":
					print(raw[i])

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
						if p[1] == entry[2] and p[0] == trig and p[2] == trigs[trig]:
							#predict.append([sentences[i][tags[i].index(sentence)],p[2], entry[0], entry, p])
							if [p[2], entry[0]] not in predict and len(entry[0]) > 0:
								predict.append([p[2], entry[0]])
		
		predict = clean(predict)

		predicts.append(predict)
		if test == 3:
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
	problematic = []
	for key in problems:
		problematic.append([key, problems[key]])

	problematic = sorted(problematic, key=lambda x: x[1], reverse=True)
	if not test:
		print("Right = " + str(right) + "/" + str(count))
		printList(problematic, 0)

	predictions = textifyPreds(predicts, files)
	
		#print(out)

	return predictions

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

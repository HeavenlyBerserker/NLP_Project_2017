
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
from spacy.en import English
from nltk import Tree
import en_core_web_sm
import unicodedata
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import random
from spacy.gold import GoldParse
from spacy.language import EntityRecognizer


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
	files = processFiles('developset/texts', 'developset/answers', "DEV")
	t1Files = processFiles('developset/texts', 'developset/answers', "TST1")

	#uncomment the following line to see how "files" works
	#printFiles(files)
        train_data=create_NER_training_data(files)
        train_NER(train_data, t1Files)
        
	patterns = paternize(files)

	writePats(patterns, "output/patterns.txt")
	#printFiles(t1Files)

	print(argv)
	
#Writes patterns to a file
def writePats(pats, name):
	file = open(name, 'w')
	for line in pats:
		file.write(line[0] + "/" +  line[1] + "/" + line[2] + "/" + str(line[3]) + "\n")

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
		printList(files[i][1][1],1)
		print("Important words------------------------------")
		printList(files[i][1][2],1)
		print("Tagger output------------------------------")
		printList(files[i][1][3],1)
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

	#Pattern format: [verb, POS, type_of_attribute]
	patterns = []
	                   
	for i in range(len(files)):
		tags.append(files[i][1][3])
		ans.append(files[i][2][1])
		sentences.append(files[i][1][1])
		#print(tags[i])
		#print(ans[i])

	for i in range(len(tags)):
		answs = ans[i]
		for sent in tags[i]:
			verbs = []
			for np in sent:
				if np[2] == 'nsubj' or np[2] == 'dobj':
					'''
					tempv = WordNetLemmatizer().lemmatize(np[3].lower(),'v').upper()
					if isinstance(tempv, str) and tempv not in verbs:
						verbs.append(WordNetLemmatizer().lemmatize(np[3].lower(),'v').upper())
					elif isinstance(tempv, unicode) and unicodedata.normalize('NFKD', tempv).encode('ascii','ignore') not in verbs:
						verbs.append(unicodedata.normalize('NFKD', tempv).encode('ascii','ignore'))
					'''
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
								'''
								if np[2] == 'nsubj' or np[2] == 'dobj':
									tempv = WordNetLemmatizer().lemmatize(np[3].lower(),'v').upper()
									if isinstance(tempv, str):
										patterns.append([WordNetLemmatizer().lemmatize(np[3].lower(),'v').upper(), np[2], answer[0]])
									else:
										patterns.append([unicodedata.normalize('NFKD', tempv).encode('ascii','ignore'), np[2], answer[0]])
								else:
									for v in verbs:
										patterns.append([v, np[2], answer[0]])
								'''
								if np[2] == 'nsubj' or np[2] == 'dobj':
									patterns.append([np[3], np[2], answer[0]])
								else:
									for v in verbs:
										patterns.append([v, np[2], answer[0]])

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
	return uniquePats

#Function#########################################################
#Prints items in array
def printList(sentences,skip):
	for sentence in sentences:
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
	nlp = spacy.load('en')
	for i in range(len(files)):
		#print("Processing " + str(i) +"/" + str(len(files)) + " files")
		file = files[i][1][0]
		sentences = nltk.sent_tokenize(file)[0:]
		sentenceEntities = []
		sentenceImp = []
		for j in range(len(sentences)):
			sentences[j] = re.sub('\n', ' ', sentences[j])
			#tokens = nltk.word_tokenize(sentences[j])
			#tagged = nltk.pos_tag(tokens)
			doc=nlp(unicode(sentences[j]))
			
			chunks = []
			for np in doc.noun_chunks:
				chunk = []
				chunk.append(unicodedata.normalize('NFKD', np.text).encode('ascii','ignore'))
				chunk.append(unicodedata.normalize('NFKD', np.root.text).encode('ascii','ignore'))
				chunk.append(unicodedata.normalize('NFKD', np.root.dep_).encode('ascii','ignore'))
				chunk.append(unicodedata.normalize('NFKD', np.root.head.text).encode('ascii','ignore'))
				chunks.append(chunk)
			#[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
			#sentenceEntities.append(sub_toks)
			'''
			entities = nltk.chunk.ne_chunk(tagged)
			sentenceEntities.append(entities)'''
			sentenceEntities.append(chunks)
			
			impWords = []
			for important in files[i][2][1]:
				for k in range(1, len(important)):
					for l in range(len(important[k])):
						if not important[k][l].startswith("DEV") and important[k][l] != '-' and important[k][l] in sentences[j]:
							impWords.append([important[k][l], find_indexes(important[k][l], sentences[j])])
			sentenceImp.append(impWords)
			

		files[i][1].append(sentences)
		#files[i][1].append(sentenceEntities)
		files[i][1].append(sentenceImp)
		files[i][1].append(sentenceEntities)
	return files

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

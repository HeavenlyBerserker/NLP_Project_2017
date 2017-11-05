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
	t1Files = processFiles('developset/texts', 'developset/answers', "TST1")

	patterns = readPats("output/patterns.txt")

	#printFiles(t1Files)
	#printList(patterns, 0)

	predictions = predict(t1Files, patterns)

	print(argv)

def predict(files, patterns):
	tags = []
	ans = []
	sentences = []

	for i in range(len(files)):
		tags.append(files[i][1][3])
		ans.append(files[i][2][1])
		sentences.append(files[i][1][1])

	predicts = []

	for i in range(len(tags)):
		predict = []
		for sentence in tags[i]:
			for entry in sentence:
				#print(entry)
				for p in patterns:
					if p[1] == entry[2] and p[0] == entry[3]:
						predict.append([p[2], entry[0]])
		predicts.append(predict)
		print("############################\nPredictions:")
		printList(predict, 0)
		print("----------------------------\nActual Answers:")
		printList(ans[i], 0)
		print("############################\n\n\n")
	return predicts



def readPats(filename):
	file = open(filename, 'r')

	pat = []

	for line in file:
		temp = line.split('/')
		temp[3] = int(temp[3].rstrip('\n'))
		#print(temp)
		pat.append(temp)

	return pat

if __name__ == "__main__":
	main(sys.argv[1:])
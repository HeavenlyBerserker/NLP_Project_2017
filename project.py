###########################
#NLP Project 2017 main code
###########################

#Autors: Hong Xu and Jie Zhang
#Repository: https://github.com/HeavenlyBerserker/NLP_Project_2017.git

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

def main(argv):
	#Reads the files in directory that begin with DEV and parses them into
	#project friendly format
	#files = [file_index 0-i] 
	#		 [0 = filename, 1 = text_file_related, 2 = answers_file_related] 
	#[i][0] = filename
	#[i][1][0] = raw text
	#[i][1][1] = parsed sentences
	#[i][2][0] = raw answers
	#[i][2][1] = parsed answers
	#See printed output for more details
	files = processFiles('developset/texts', 'developset/answers', "DEV")

	#uncomment the following to see how "files" works

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
		print("Answers--------------------------------------")
		print(files[i][2][0]) #prints answer for the file i
		print("Answers_in_array_form------------------------")
		printList(files[i][2][1],0) #prints answer array for the file i

	print(argv)

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
	for i in range(len(files)):
		#print("Processing " + str(i) +"/" + str(len(files)) + " files")
		file = files[i][1][0]
		sentences = nltk.sent_tokenize(file)[0:]
		sentenceEntities = []
		sentenceImp = []
		for j in range(len(sentences)):
			sentences[j] = re.sub('\n', ' ', sentences[j])
			'''tokens = nltk.word_tokenize(sentences[j])
			tagged = nltk.pos_tag(tokens)
			entities = nltk.chunk.ne_chunk(tagged)
			sentenceEntities.append(entities)'''
			
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

			text = [ filename ,[tfile.read()], [afile.read()]]

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

if __name__ == "__main__":
	main(sys.argv[1:])

#!/usr/bin/python3

import timeit
import math
from nltk import word_tokenize

f = open("data.txt","r")

word_d = {}
sent_list = []
def process_new_sentence(s):
	sent_list.append(s)
	tokenized = word_tokenize(s)
	for word in tokenized:
		if word not in word_d.keys():
			word_d[word]=0
		word_d[word] += 1

def compute_tf(s):
	bow = set()
	# dictionary for words in the given sentence (document)
	wordcount_d = {}

	tokenized = word_tokenize(s)
	for tok in tokenized:
		if tok not in wordcount_d.keys():
			wordcount_d[tok]=0
		wordcount_d[tok] += 1
		bow.add(tok)
	tf_d = {}
	for k,v in wordcount_d.items():
		tf[k] = v/(float(len(bow)))
	return tf_d


def compute_idf():
	Dval = len(sent_list)
	bow = set()
	for i in range(0,len(sent_list)):
		tokenized = word_tokenize(sent_list[i])
		for tok in tokenized:
			bow.add(tok)
	idf_d = {}
	for t in bow:
		cnt = 0
		for s in sent_list:
			if t in word_tokenize(s):
				cnt += 1
			idf_d[t]=log((float(len(bow)))/cnt)
	return idf_d


if __name__ == '__main__':

	start = timeit.default_timer()
	docs = []
	
	f = open("data.txt","r")

	while True:
		line = f.readline()
		docs.append(line)
		if not line: break
	
	f.close()
	v = []
	for line in docs:
		process_new_sentence(line)
		
	idf_d = compute_idf()
	for i in range(0,len(sent_list)):
		tf_d = compute_tf(sent_list[i])

	for word,tfval in tf_d.items():
		print(word, tfval*idf_d[word])
	print(" ")

	end = timeit.default_timer()
	end-=start
	
	print("time =",end)

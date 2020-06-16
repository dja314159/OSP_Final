#!/usr/bin/python3

import re
import timeit
import math
import nltk
from nltk import word_tokenize

f = open("data.txt","r")

word_d = {}
sent_list = []
def clean_str(text):
    pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '<[^>]*>'         # HTML 태그 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '[^\w\s]'         # 특수기호제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '[0-9]'
    text = re.sub(pattern=pattern, repl='', string=text)
    return text   

def process_new_sentence(s):
	sent_list.append(s)
	tokenized = word_tokenize(s)
	for word in tokenized:
		word = word.lower()	
		if word not in word_d.keys():
			word_d[word]=0
		word_d[word] += 1

def compute_tf(s):
	bow = set()
	# dictionary for words in the given sentence (document)
	wordcount_d = {}

	tokenized = word_tokenize(s)
	for tok in tokenized:
		tok = tok.lower()	
		if tok not in wordcount_d.keys():
			wordcount_d[tok]=0
		wordcount_d[tok] += 1
		bow.add(tok)
	tf_d = {}
	for k,v in wordcount_d.items():
		tf_d[k] = v/(float(len(bow)))
	return tf_d


def compute_idf():
	Dval = len(sent_list)
	bow = set()
	for i in range(0,len(sent_list)):
		tokenized = word_tokenize(clean_str(sent_list[i].lower()))
		for tok in tokenized:
			bow.add(tok)
	idf_d = {}
	for t in bow:
		cnt = 1
		for s in sent_list:
			if t in word_tokenize(s.lower()):
				cnt += 1
			idf_d[t]=math.log((float(len(bow)))/cnt)
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
		tf_d = compute_tf(clean_str(sent_list[i]))
	
	gather = " ".join(sent_list)
	tf_d = compute_tf(clean_str(gather))
	dic_print = {}

	for word,tfval in tf_d.items():
		dic_print[word] = tfval*idf_d[word]
	arr =[]
	arr = sorted(dic_print.items(),key=lambda x: x[1], reverse=True)
	
	count = 1	
	for x,y in arr:
		if(count==10):break
		print('%-10s %.4f'%(x,y))
		count +=1	
	print("")

	end = timeit.default_timer()
	end -= start
	print("time =",end)

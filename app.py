#!/usr/bin/python3

from flask import Flask
from flask import render_template,request

import re
import requests
import urllib.request
from bs4 import BeautifulSoup

import re
import timeit
import math
import nltk
from nltk import word_tokenize

import pprint
from elasticsearch import Elasticsearch


word_d = {}
sent_list = []
arr = []
result = []
wordList =[]
TF = []
wordCount = []
processTime = []


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
	count = 0	
	Dval = len(sent_list)
	bow = set()
	for i in range(0,len(sent_list)):
		tokenized = word_tokenize(clean_str(sent_list[i].lower()))
		for tok in tokenized:
			bow.add(tok)
			count+=1
	wordCount.append(count)

	idf_d = {}
	for t in bow:
		cnt = 1
		for s in sent_list:
			if t in word_tokenize(s.lower()):
				cnt += 1
			idf_d[t]=math.log((float(len(bow)))/cnt)
	return idf_d
	
def main(url):

	req = urllib.request.Request(url)
	sourcecode = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(sourcecode, "html.parser")
	str = soup.select_one('div#bodyColumn')

		
	para = str.text.strip()
	start = timeit.default_timer()
	docs = para.split('\n')	
	v = []
	
	sent_list.clear()
	for line in docs:
		process_new_sentence(line)
	
	idf_d = compute_idf()
		
	for i in range(0,len(sent_list)):
		tf_d = compute_tf(clean_str(sent_list[i]))
		
	gather = " ".join(sent_list)
	tf_d = compute_tf(clean_str(gather))
	dic_print = {}
	dic_print.clear()
	
	for word,tfval in tf_d.items():
		dic_print[word] = tfval*idf_d[word]
		
	arr = sorted(dic_print.items(),key=lambda x: x[1], reverse=True)
		
	count = 0
	wordList.clear()
	TF.clear()
	
	for x,y in arr:
		if(count==10):break
		wordList.insert(count,x)
		TF.insert(count,y)
		count +=1		
	
	end = timeit.default_timer()
	end -= start

	"""try:
		es = Elasticsearch('127.0.0.1:9200')
		
		data = {"url" : url, "words" : wordList.copy(), "TF_IDF values" : TF.copy()}
		res = es.index(index = 'web',doc_type = "word", body = data)
		print(data)
		print("\n")
		pprint.pprint(res)
	except KeyboardInterrupt:
		pass"""
def fileAnal(URLarr):
	
	count = 0
	for url in URLarr:
		start = timeit.default_timer()	
		main(url)
		end = timeit.default_timer()
		end -= start
		processTime.append(end)
		

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/home/')
def home():
	return render_template('index.html')

@app.route("/getURL/")
def getURL():
	return render_template('getURL.html')

@app.route("/getFILE/")
def getFILE():
	return render_template('getFILE.html')

@app.route("/printFILE/",methods = ['post'])
def printFILE():	
	URLs = request.form['URLs']
	URLarr = URLs.split()
	fileAnal(URLarr)
	
	return render_template('printFILE.html',url1 = URLarr[0],count1 = wordCount[0], time1 = processTime[0],url2 = URLarr[1],count2 = wordCount[1], time2 = processTime[2],url3 = URLarr[2],count3 = wordCount[2], time3 = processTime[2],url4 = URLarr[3],count4 = wordCount[3], time4 = processTime[3],url5 = URLarr[4],count5 = wordCount[4], time5 = processTime[4],url6 = URLarr[5],count6 = wordCount[5], time6 = processTime[5],url7 = URLarr[6],count7 = wordCount[6], time7 = processTime[6],url8 = URLarr[7],count8 = wordCount[7], time8 = processTime[7],url9 = URLarr[8],count9 = wordCount[8], time9 = processTime[8],url10 = URLarr[9],count10 = wordCount[9], time10 = processTime[9])

@app.route("/printURL/", methods = ['post'])
def printURL():

	url = request.form['userURL']	
	
	start = timeit.default_timer()
	main(url)
	end = timeit.default_timer()
	end -= start
	
	return render_template('printURL.html', url = url, word1 = wordList[0], value1 = TF[0], word2 = wordList[1], value2 = TF[1],word3 = wordList[2], value3 = TF[2],word4 = wordList[3], value4 = TF[3],word5 = wordList[4], value5 = TF[4],word6 = wordList[5], value6= TF[5],word7 = wordList[6], value7 = TF[6],word8 = wordList[7], value8 = TF[7],word9 = wordList[8], value9 = TF[8],word10 = wordList[9], value10 = TF[9], time = end)

@app.route("/wordAnal/")
def wordAnal():
	return render_template('wordAnal.html')

@app.route("/pop1/",methods = ['post'])
def pop1():
	url = request.form['URL']
	main(url)
	return render_template('pop1.html' ,word1 = wordList[0], value1 = TF[0], word2 = wordList[1], value2 = TF[1],word3 = wordList[2], value3 = TF[2],word4 = wordList[3], value4 = TF[3],word5 = wordList[4], value5 = TF[4],word6 = wordList[5], value6= TF[5],word7 = wordList[6], value7 = TF[6],word8 = wordList[7], value8 = TF[7],word9 = wordList[8], value9 = TF[8],word10 = wordList[9], value10 = TF[9])

@app.route("/cosineAnal/")
def cosineAnal():
	return render_template('cosineAnal.html')





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

@app.route("/printURL/", methods = ['post'])
def printURL():

	word_d = {}
	sent_list = []
	arr = []
	result = []

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
	
	
	def main():
	
		url = request.form['userURL']
		req = urllib.request.Request(url)
		sourcecode = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(sourcecode, "html.parser")
		str = soup.select_one('div#bodyColumn')

		
		para = str.text.strip()
		start = timeit.default_timer()
		docs = para.split('\n')
		
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
		arr = sorted(dic_print.items(),key=lambda x: x[1], reverse=True)
		
		count = 0
		for x,y in arr:
			if(count==10):break
			result.append(x)
			result.append(y)
			count +=1		
	
		end = timeit.default_timer()
		end -= start
	
	start = timeit.default_timer()
	main()
	end = timeit.default_timer()
	end -= start
	
	return render_template('printURL.html', word1 = result[0], value1 = result[1], word2 = result[2], value2 = result[3],word3 = result[4], value3 = result[5],word4 = result[6], value4 = result[7],word5 = result[8], value5 = result[9],word6 = result[10], value6= result[11],word7 = result[12], value7 = result[13],word8 = result[14], value8 = result[15],word9 = result[16], value9 = result[17],word10 = result[18], value10 = result[19], time = end)

@app.route("/wordAnal/")
def wordAnal():
	return render_template('wordAnal.html')

@app.route("/pop1/")
def pop1():
	return render_template('pop1.html')

@app.route("/cosineAnal/")
def cosineAnal():
	return render_template('cosineAnal.html')





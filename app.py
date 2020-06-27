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

import numpy as np



word_d = {}
sent_list = []
arr = []
result = []
wordList =[]
TF = []
wordCount = []
processTime = []
cosSim = []
cosReturn =[]


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

	try:
		es = Elasticsearch('127.0.0.1:9200')
		
		data = {"url" : url, "words" : wordList.copy(), "TF_IDF values" : TF.copy()}
		res = es.index(index = 'web',doc_type = "word", body = data)
		pprint.pprint(data)
		print("\n")
		pprint.pprint(res)
	except KeyboardInterrupt:
		pass

def make_vector(i):
	v = []
	s = sent_list[i]
	tokenized = word_tokenize(s)
	for w in word_d.keys():
		val = 0
		for t in tokenized:
			if t==w:
				val +=1
		v.append(val)
	return v

def crawl(url):
	req = urllib.request.Request(url)
	sourcecode = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(sourcecode, "html.parser")
	str = soup.select_one('div#bodyColumn')

		
	para = str.text.strip()
	return para

def cosineAnal(URLarr):
	vector = []
	transVec = []





	for i in range(10):
		my_dic = dict()
		for j in range(10):
			#i번째 인덱스의 url과 j번째의 url을 각각 가져와서 process돌리기
			#그리고 make vector돌리고 값 리턴받아 더하고 코사인 유사도 계산
			#그리고 my_dic[URLarr[j]] = cosSim[i][j]이런 식으로 i번째 url의 코사인 유사도 순차적으로 저장
			#그리고 정렬 한 뒤
			#cosReturn 리스트에 추가
			if(i==j):
				continue		
			sent_list.clear()
			word_d.clear()
			process_new_sentence(crawl(URLarr[i]))
			process_new_sentence(crawl(URLarr[j]))
			v1 = make_vector(0)
			v2 = make_vector(1)
			#print(v1)	
			#print(v2)			
			transVec1 = np.array(v1)
			transVec2 = np.array(v2)

			#print(i)
			#print(j)
	
			dotPro = np.dot(transVec1,transVec2)
			#print(dotPro/(sum(v1)*sum(v2)))
			my_dic[URLarr[j]] = dotPro/(sum(v1)*sum(v2))
			#print(my_dic)
			my_dic_sorted = sorted(my_dic.items(),reverse=True,key=lambda item: item[1])
			my_dic_sorted.sort(key=lambda x:x[1], reverse=True)	
	
		cosReturn.append(my_dic_sorted)
			
		
	"""for url in URLarr:
		process_new_sentence(crawl(url))
		
	for i in range(0,10):
		vector.append(make_vector(i))
		transVec.append(np.array(vector[i]))
	for i in range(0,10):
		my_dic = dict()
		for j in range(0,10):
			dotPro = np.dot(transVec[i],transVec[j])
			a = np.array(vector[i])
			b = np.array(vector[j])
			value1 = np.sum(a)
			value2 = np.sum(b)
			print(dotPro/(value1*value2))		
			cosSim[i][j] = dotPro/(value1*value2)
			my_dic[URLarr[j]] = cosSim[i][j]
		my_dic_dic=dict(my_dic)
		my_dic_sorted = sorted(my_dic_dic.items(),reverse=True,key=lambda item: item[1])
		my_dic_sorted.sort(key=lambda x:x[1], reverse=True)	
		cosReturn.append(my_dic_sorted)
	print(cosReturn)"""
		



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
	cosineAnal(URLarr)
	
	return render_template('printFILE.html',url1 = URLarr[0],count1 = wordCount[0], time1 = processTime[0],num1 = 0,url2 = URLarr[1],count2 = wordCount[1], time2 = processTime[1],url3 = URLarr[2],count3 = wordCount[2], time3 = processTime[2],url4 = URLarr[3],count4 = wordCount[3], time4 = processTime[3],url5 = URLarr[4],count5 = wordCount[4], time5 = processTime[4],url6 = URLarr[5],count6 = wordCount[5], time6 = processTime[5],url7 = URLarr[6],count7 = wordCount[6], time7 = processTime[6],url8 = URLarr[7],count8 = wordCount[7], time8 = processTime[7],url9 = URLarr[8],count9 = wordCount[8], time9 = processTime[8],url10 = URLarr[9],count10 = wordCount[9], time10 = processTime[9])

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

@app.route("/pop2_0/",methods = ['post'])
def pop2_0():
	num = request.form['num']
	
	return render_template('pop2.html', cosUrl1 = cosReturn[0][0][0], similarity1 = cosReturn[0][0][1], cosUrl2 = cosReturn[0][1][0], similarity2 = cosReturn[0][1][1], cosUrl3 = cosReturn[0][2][0], similarity3 = cosReturn[0][2][1])

@app.route("/pop2_1/",methods = ['post'])
def pop2_1():
	num = request.form['num']
	
	return render_template('pop2.html', cosUrl1 = cosReturn[1][0][0], similarity1 = cosReturn[1][0][1], cosUrl2 = cosReturn[1][1][0], similarity2 = cosReturn[1][1][1], cosUrl3 = cosReturn[1][2][0], similarity3 = cosReturn[1][2][1])

@app.route("/pop2_2/",methods = ['post'])
def pop2_2():
	num = request.form['num']
	
	return render_template('pop2.html', cosUrl1 = cosReturn[2][0][0], similarity1 = cosReturn[2][0][1], cosUrl2 = cosReturn[2][1][0], similarity2 = cosReturn[2][1][1], cosUrl3 = cosReturn[2][2][0], similarity3 = cosReturn[2][2][1])

@app.route("/pop2_3/",methods = ['post'])
def pop2_3():
	num = request.form['num']
	
	return render_template('pop2.html', cosUrl1 = cosReturn[3][0][0], similarity1 = cosReturn[3][0][1], cosUrl2 = cosReturn[3][1][0], similarity2 = cosReturn[3][1][1], cosUrl3 = cosReturn[3][2][0], similarity3 = cosReturn[3][2][1])

@app.route("/pop2_4/",methods = ['post'])
def pop2_4():
	num = request.form['num']
	
	return render_template('pop2.html', cosUrl1 = cosReturn[4][0][0], similarity1 = cosReturn[4][0][1], cosUrl2 = cosReturn[4][1][0], similarity2 = cosReturn[4][1][1], cosUrl3 = cosReturn[4][2][0], similarity3 = cosReturn[4][2][1])

@app.route("/pop2_5/",methods = ['post'])
def pop2_5():
	num = request.form['num']
	
	return render_template('pop2.html', cosUrl1 = cosReturn[5][0][0], similarity1 = cosReturn[5][0][1], cosUrl2 = cosReturn[5][1][0], similarity2 = cosReturn[5][1][1], cosUrl3 = cosReturn[5][2][0], similarity3 = cosReturn[5][2][1])

@app.route("/pop2_6/",methods = ['post'])
def pop2_6():
	num = request.form['num']
	
	return render_template('pop2.html', cosUrl1 = cosReturn[6][0][0], similarity1 = cosReturn[6][0][1], cosUrl2 = cosReturn[6][1][0], similarity2 = cosReturn[6][1][1], cosUrl3 = cosReturn[6][2][0], similarity3 = cosReturn[6][2][1])

@app.route("/pop2_7/",methods = ['post'])
def pop2_7():
	num = request.form['num']
	
	return render_template('pop2.html', cosUrl1 = cosReturn[7][0][0], similarity1 = cosReturn[7][0][1], cosUrl2 = cosReturn[7][1][0], similarity2 = cosReturn[7][1][1], cosUrl3 = cosReturn[7][2][0], similarity3 = cosReturn[7][2][1])

@app.route("/pop2_8/",methods = ['post'])
def pop2_8():
	num = request.form['num']
	
	return render_template('pop2.html', cosUrl1 = cosReturn[8][0][0], similarity1 = cosReturn[8][0][1], cosUrl2 = cosReturn[8][1][0], similarity2 = cosReturn[8][1][1], cosUrl3 = cosReturn[8][2][0], similarity3 = cosReturn[8][2][1])

@app.route("/pop2_9/",methods = ['post'])
def pop2_9():
	num = request.form['num']
	
	return render_template('pop2.html', cosUrl1 = cosReturn[9][0][0], similarity1 = cosReturn[9][0][1], cosUrl2 = cosReturn[9][1][0], similarity2 = cosReturn[9][1][1], cosUrl3 = cosReturn[9][2][0], similarity3 = cosReturn[9][2][1])
	




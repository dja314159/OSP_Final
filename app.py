#!/usr/bin/python3

from flask import Flask
from flask import render_template
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

@app.route("/printURL/")
def printURL():
	return render_template('printURL.html')

@app.route("/wordAnal/")
def wordAnal():
	return render_template('wordAnal.html')

@app.route("/pop1/")
def pop1():
	return render_template('pop1.html')

@app.route("/cosineAnal/")
def cosineAnal():
	return render_template('cosineAnal.html')





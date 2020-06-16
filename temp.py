#!/usr/bin/python3

import re
import requests
import urllib.request
from bs4 import BeautifulSoup

url = "http://ambari.apache.org"
req = urllib.request.Request(url)

sourcecode = urllib.request.urlopen(url).read()
soup = BeautifulSoup(sourcecode, "html.parser")

#str = soup.select('div#bodyColumn')
str = soup.select_one('div#bodyColumn')
#str = soup.find('div',{'id':'bodyColumn'})


with open('data.txt','w+') as f:
	f.write(str.text.strip())

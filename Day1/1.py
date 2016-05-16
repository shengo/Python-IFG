#!/usr/local/lib/python2.7
#_*_coding:utf-8_*_

from __future__ import unicode_literals
import urllib2
import os
import codecs
from os import path, makedirs
import re
from bs4 import BeautifulSoup
out="./testfolder/"
counter =0
if not path.exists (out):
	makedirs(out)

listeCategory = ["politique", "economie", "sport", "culture", "sciences"]

for category in listeCategory:
	outCategory = out + "/" + category
	if not path.exists (outCategory):	
		makedirs(outCategory)

	for i in range (1,4):
		urlCategory = r'http://www.lemonde.fr/{}/{}.html'.format(category, i)
		file = urllib2.urlopen(urlCategory)
		soup = BeautifulSoup(file, "html5lib")
		blocURLS = soup.find_all(href=re.compile(r'\/\S+\/article\/\S+\.html'))
		#print urlCategory
	
		for t_url in blocURLS:
			URL = t_url["href"]
			URL = "http://lemonde.fr/" + URL
			counter = counter + 1
			print URL
			nomFichiers = "article" + category + "_" + str(counter) + ".txt"
		   
			file=urllib2.urlopen(URL)
			soup = BeautifulSoup( file , "html5lib" )
			article = soup.find( id=re.compile("articleBody") )
			article = article.get_text()
			   
			with codecs.open(os.path.join(out , nomFichiers) , "w" , encoding="utf-8") as fout:
				fout.write(article)
			fout.close()







#!/usr/local/lib/python2.7
# -*- coding: utf-8 -*-



from __future__ import unicode_literals
import urllib2
import os
import codecs
from os import path, makedirs
import re
from bs4 import BeautifulSoup
out="./testregexp/"
counter =0

def nettoyerHTML(texte):	
    
	pattern=re.compile(r'(<style.*?>([\s\S]*?)<\/style>)',re.UNICODE)
	match=re.search(pattern, texte)	
	if match:	
		texte=re.sub(pattern,'',texte)
	
	pattern=re.compile(r'<script[\s\S]+<\/script>',re.UNICODE)
	match=re.search(pattern, texte)
	if match:	
		texte=re.sub(pattern,'',texte)	
	
	return texte	
#----------------------------------------------------------------------------------


if not path.exists (out):
	makedirs(out)

listeCategory = ["politique", "economie", "sport", "culture", "sciences"]
#listeCategory = ["politique",  "sport", "culture", "sciences"]

for category in listeCategory:
	#out="./testfolder/"	
	outCategory = out + "/" + category
	if not path.exists (outCategory):	
		makedirs(outCategory)
	counter=0
	for i in range (1,3):
		urlCategory = r'http://www.lemonde.fr/{}/{}.html'.format(category, i)
		file = urllib2.urlopen(urlCategory)
		soup = BeautifulSoup(file, "html5lib")
		blocURLS = soup.find_all(href=re.compile(r'\/\S+\/article\/\S+\.html'))
		#print urlCategory
	
		for turl in blocURLS:
						
			URL = turl["href"]
			#print "---------",  URL
			URL = "http://lemonde.fr" + URL
			counter = counter + 1
			#print URL
			nomFichiers = "article" + category + "_" + str(counter) + ".txt"
		   
			file=urllib2.urlopen(URL)
			soup = BeautifulSoup( file , "html5lib" )
			

			article1 = soup.find("div", {"id" : re.compile(r'.*article.*')})
            		article2 = soup.find("div", {"class" : re.compile(r'.*article.*')})
            		container=soup.find("div", {"class" : re.compile(r'.*container.*')})
		    	print container
			
			if article1 :
				article=unicode(article1)
				article=nettoyerHTML(article)
				article=BeautifulSoup(article, "html5lib")	
				article = article.get_text()
				article=unicode(article)
			elif article2 :
				article=unicode(article2)
				article=nettoyerHTML(article)
				article=BeautifulSoup(article, "html5lib")	
				article = article.get_text()
				article=unicode(article)
			else :
				pass

			if article :
				with codecs.open(os.path.join(out , category, nomFichiers) , "w" , encoding="utf-8") as fout:
					fout.write(article)
				fout.close()







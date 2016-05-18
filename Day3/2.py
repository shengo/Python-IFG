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

	pattern=re.compile(r'<p class="lire.*">\s+Lire.*[\s\S]+<\/p>/gi',re.UNICODE) # for read more links
    	match=re.search(pattern, texte)
    	if match:
       		texte=re.sub(pattern,'',texte)
	# zeda sams /gi gasascorebelia marto pirvels poulobs ise	

	
	
	return texte	

def nettoyerEspaces(texte):		
	pattern1=re.compile(r'[ \t\n\r\f\v]+',re.UNICODE)	#all empy lines.spaces...
	match1=re.search(pattern1, texte)	
	if match1:	
		texte=re.sub(pattern1,' ',texte)	
   
	pattern2=re.compile(r'^( )+')	
	match2=re.search(pattern2, texte)	#blank spaces in the beggining of article
	if match2:	
		texte=re.sub(pattern2,' ',texte)	
	return texte
#----------------------------------------------------------------------------------


#----------------------------------------------------------------------------------


if not path.exists (out):
	makedirs(out)

#listeCategory = ["politique", "economie", "sport", "culture", "sciences"]
listeCategory = ["politique", "economie"]

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
			
			
			twitter=soup.find_all("blockquote", {"class" : re.compile(r'twitter-tweet')})
			snippet=soup.find_all("snippet", {"class" : re.compile(r'snippet')})				

			if snippet:
				for ele in snippet:				
					soup = ele.decompose()
					print "found snippet\n"
			if twitter:
				for ele in twitter:				
					soup = ele.decompose()
					print "found snippet\n"

			


			#container=soup.find("div", {"class" : re.compile(r'.*container.*')})
			#container=soup.find("img")		    	
			#print container
			
			if article1 :
				article=unicode(article1)
				article=nettoyerHTML(article)				
				article=BeautifulSoup(article, "html5lib")	
				article = article.get_text()
				article=nettoyerEspaces(article)
				#article=unicode(article)
			elif article2 :
				article=unicode(article2)
				article=nettoyerHTML(article)				
				article=BeautifulSoup(article, "html5lib")	
				article = article.get_text()
				article=nettoyerEspaces(article)
				#article=unicode(article)
			else :
				pass

			if article :
				with codecs.open(os.path.join(out , category, nomFichiers) , "w" , encoding="utf-8") as fout:
					fout.write(article)
				fout.close()







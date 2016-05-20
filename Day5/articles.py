#!/usr/local/lib/python2.7
# -*- coding: utf-8 -*-



from __future__ import unicode_literals
import urllib2
import os
import codecs
from os import path, makedirs
import re
from bs4 import BeautifulSoup
from nltk import precision,recall
out="./articles/"
outFortag="./tags/"
counter =0



def nettoyerHTML(texte):	#fonction qui supprime les  balises, <style>, <script> ...
    
	pattern=re.compile(r'(<style.*?>([\s\S]*?)<\/style>)',re.UNICODE) #regex : toutes les lignes contenant balise <style>
	match=re.search(pattern, texte)	
	if match:	#si nous avons trouve regex
		texte=re.sub(pattern,'',texte) #changer tout, qui sont trouve avec ''
	
	pattern=re.compile(r'<script[\s\S]+<\/script>',re.UNICODE) #regex : toutes les lignes contenant balise <script>
	match=re.search(pattern, texte)
	if match:	#si nous avons trouve regex
		texte=re.sub(pattern,'',texte) #changer tout, qui sont trouve avec ''

	
	return texte	#retourne le texte modifie
#----------------------------------------------------------------------------------

def nettoyeSpaces(texte):	#fonction qui supprime les espaces  et les lignes	
	
	spaces1=re.compile(r'[ \t\n\r\f\v]+',re.UNICODE)	#tous les espaces blancs
	match1=re.search(spaces1, texte)	
	if match1:	
		texte=re.sub(spaces1,' ',texte)	#changer tout, qui sont trouve avec ''
   
	spaces2=re.compile(r'^( )+')		# espaces blancs qui sont au debut d'article
	match2=re.search(spaces2, texte)	#blank spaces in the beggining of article
	if match2:	
		texte=re.sub(spaces2,' ',texte)	#changer tout, qui sont trouve avec ''
	return texte	#retourne le texte modifie
#----------------------------------------------------------------------------------

def myF(soup,tag,attr,val): #fonction pour enleve les tweets, 
    length = len(tag) 		
    resultats = [0] * length
    for i in range(0,length):
        resultats[i] = soup.find_all(tag[i], {attr[i]: re.compile(r'%s'%(val[i]))}) #pour trouver tous les tweets
	#tag- div ou blockquote, attr - class ou id, val - nom de class ou div
    for i in range(0,length):
        if resultats[i]!=0:
            for elem in resultats[i]:
                soup = elem.decompose() 
    return soup
	



#----------------------------------------------------------------------------------


if not path.exists (out): 	# si repertoire existe
	makedirs(out)		# si repertoire n'existe pas, cree

listeCategory = ["politique", "economie", "sport", "culture", "sciences"] #les categories
#listeCategory = ["politique"] #les categories

for category in listeCategory:			# repertoires pour chaqun categorie
	
	outCategory = out + "/" + category	# nom de repertoire por categories
	
	if not path.exists (outCategory):	# si repertoire n'existe pas
		makedirs(outCategory)		# creer repertoire
	
	counter=0				# variable-compteur por les noms de fichiers

	#for i in range (1,4):			#RAM overflow on function sent_features :(
	for i in range (1,2):			# pour 3 page
		urlCategory = r'http://www.lemonde.fr/{}/{}.html'.format(category, i) # url
		file = urllib2.urlopen(urlCategory)
		soup = BeautifulSoup(file, "html5lib")	#convertir la page HTML 
		blocURLS = soup.find_all(href=re.compile(r'\/\S+\/article\/\S+\.html')) #trouver URL's de tous les articles
	
		for articleurl in blocURLS: 	#pour chaqun URL d'articles
						
			URL = articleurl["href"]
			URL = "http://lemonde.fr" + URL
			counter = counter + 1	#augmenter compteur
			nomFichiers = "article" + category + "_" + str(counter) + ".txt"	#noms de fichiers
		   
			file=urllib2.urlopen(URL)			
			soup = BeautifulSoup( file , "html5lib" )	#convertir la page HTML 
	
			article1 = soup.find("div", {"id" : re.compile(r'.*article.*')})	#si nous avons div avec id
            		article2 = soup.find("div", {"class" : re.compile(r'.*article.*')})	#si nous avons div avec class
			
			
			soup = myF(soup,['div','blockquote'],['class','id'],['snippet','twitter-tweet'])
			#fonction pour enleve les tweets
			
			
			if article1 : 				#si nous avons div avec id
				article=unicode(article1)
				article=nettoyerHTML(article)	#utilise fonction nettoyerHTML			
				article=BeautifulSoup(article, "html5lib")	#convertir la page HTML 
				article = article.get_text()
				article=nettoyeSpaces(article)	#utilise fonction nettoyerSpaces
			elif article2 :				#si nous avons div avec class
				article=unicode(article2)
				article=nettoyerHTML(article)	#utilise fonction nettoyerHTML				
				article=BeautifulSoup(article, "html5lib")	#convertir la page HTML 
				article = article.get_text()
				article=nettoyeSpaces(article)	#utilise fonction nettoyerSpaces	
			else :
				pass	#faire rien

			if article :
				with codecs.open(os.path.join(out , category, nomFichiers) , "w" , encoding="utf-8") as fout: #ouvrir fichier
					fout.write(article) #ouvrir fichier
					#print fout
				fout.close() # fermer fichier
				





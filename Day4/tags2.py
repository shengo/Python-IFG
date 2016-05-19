#!/usr/local/lib/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import urllib2
import os 
import codecs
import treetaggerwrapper
from os import path,makedirs
import nltk
from nltk import precision,recall
import collections

from nltk.classify import NaiveBayesClassifier
from nltk.corpus.reader import CategorizedTaggedCorpusReader	
import random
nltk.download()


tagger=treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='../treetagger')

inputFolder ="./articles/"			#repertoire de entree
outputFolder = "./articles/_tags/"		#repertoire de sortie
listeCategory = ["politique", "economie", "sport", "culture", "sciences"]	#les categories
#listeCategory = ["politique"]	#liste de listeCategory			#les categories (pour tester)

if not path.exists (outputFolder): 	# si repertoire n'existe pas
	makedirs(outputFolder)		# creer repertoire


for category in listeCategory:		# repertoires pour chaqun categorie
	
	FilePaths = inputFolder  + category		#chemin de qu'on ouvre/lire
	with codecs.open( outputFolder + category + ".txt" , "w", encoding="utf-8" ) as output: #ouvrir fichier de sortie
		
		#print 'output: \n'	#pour tester
		#print output		#pour tester
		#print '\n'		#pour tester
			
		for filename in os.listdir( FilePaths ):				#tous fichiers dans repertoire

			file = FilePaths + "/" + filename				#fichier de sortie
			#print 'opened file: \t', filename, '\n'			#print  fichier qui nouse avons ouvrir
			with codecs.open( file , encoding="utf-8"  ) as text:		#ouvrir fichier de entree
				
				#print 'text: \n'	#pour tester
				#print text		#pour tester
				#print '\n'		#pour tester		 

				result = (text.read())		#lire
				tags = tagger.tag_text(result)	#tags
				for tag in tags:			
					
					#print '\n' 		#pour tester
					#print tag		#pour tester
					#print '\n'		#pour tester
					#print 'output: \n'	#pour tester
					#print output		#pour tester	
					#print '\n'		#pour tester
					output.write(tag+"\n")	#ecrire dans le fichier de sortie	

			text.close()	#fermer fichier de sortie
	output.close()			#fermer fichier de entree



leMonde=CategorizedTaggedCorpusReader(outputFolder, r'\w+\.txt', cat_pattern=r'\w+\.txt')
#print leMonde
total_carac=0
total_mots=0
total_phrases=0
total_vocals=0

for category in leMonde.categories():	
	print "test \n"	
	nb_carac=len(leMonde.raw(categories=category))
	nb_mots = len(leMonde.words(categories=category))
	nb_phrases=len(leMonde.sents(categories=category))
	nb_vocals=len(leMonde.words(categories=category))
	
	total_carac = total_carac +nb_carac
	total_mots = total_mots +nb_mots
	total_phrases = total_phrases +nb_phrases
	total_vocals = total_vocals +nb_vocals
	
		
	

print "\n"
print total_carac
print "\n"

print "\n"
print total_mots
print "\n"

print "\n"
print total_phrases
print "\n"

print "\n"
print total_vocals
print "\n"
	   


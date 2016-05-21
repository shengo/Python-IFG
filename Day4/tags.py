#!/usr/local/lib/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import urllib2
import os 
import codecs
import treetaggerwrapper
from os import path,makedirs

from nltk import precision,recall
#import collection

from nltk.classify import NaiveBayesClassifier
from nltk.corpus.reader import CategorizedTaggedCorpusReader	
import random



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



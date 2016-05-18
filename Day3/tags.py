#!/usr/local/lib/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import urllib2
#import urllib2.request
import os 
import re
import codecs
import treetaggerwrapper
import io

from os import path,makedirs
from bs4 import BeautifulSoup


tagger=treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='../treetagger')	#objet de treetaggerwrapper

inputFolder ="./testregexp/"			#chemin de entree
outputFolder = "./tags2/"
categories = ["politique", "economie", "sport", "culture", "sciences"]	#liste de categories
#categories = ["politique"]	#liste de categories

if not path.exists (outputFolder): 	# si repertoire existe
	makedirs(outputFolder)


for cat in categories:		#pour tous les categories dans la liste
	FilePath = inputFolder  + cat		#chemin de qu'on ouvre/lire
	#output = open(cat + ".txt" , "w")		#nom de fichier sortie est folder d'entree plus categorie
	with io.open( outputFolder + cat + ".txt" , "w" ) as output:
		print 'output: \n'
		print output
		print '\n'
		output.write( "\n\n\t\t\t\t" + cat + "\n\n" )	#juste print de categorie au debout de fichier
		for filename in os.listdir( FilePath ):			#pour tous les fichiers 
			output.write( "\n\t\t\t\t" + filename + "\n" )	#print quelle fichier on a ouvert
			file = FilePath + "/" + filename		#xyz.txt fichier
			with io.open( file , encoding="utf-8"  ) as text:		#la texte dans cette fichier
				#print 'text: \n'
				#print text
				#print '\n'			 
											#j'ai eu un probleme d'unicode donc j'utilise try/catch
				result = (text.read())			#on lise la texte
				tags = tagger.tag_text(result)		#on le tag
				for tag in tags:			#pour tous les mots dans le tag
					
					print '\n'
					print tag
					print '\n'
					print 'output: \n'
					print output
					print '\n'
					output.write(tag+"\n")		#format fichier de sortie

			text.close()
	output.close()



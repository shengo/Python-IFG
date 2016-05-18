#-*- coding : utf-8 -*-
from __future__ import unicode_literals
import urllib
import urllib.request
import os 
import re
import codecs
import treetaggerwrapper

from os import path,makedirs
from bs4 import BeautifulSoup


tagger = treetaggerwrapper.TreeTagger( TAGLANG="fr" , TAGDIR="C:\TreeTagger" )		#objet de treetaggerwrapper

inputFolder ="C:\\Users\\Amber\\Desktop\\Python\\2016.05.18\\Answer"			#chemin de entree
categories = [ "culture" , "economie" , "politique" , "sciences" , "sport" ]	#liste de categories


for cat in categories:													#pour tous les categories dans la liste
	FilePath = inputFolder + "/" + cat									#chemin de qu'on ouvre/lire
	output = open(cat + ".txt" , "w")									#nom de fichier sortie est folder d'entree plus categorie
	output.write( "\n\n\t\t\t\t" + str(cat) + "\n\n" )					#juste print de categorie au debout de fichier
	for filename in os.listdir( FilePath ):								#pour tous les fichiers 
		output.write( "\n\t\t\t\t" + filename + "\n" )					#print quelle fichier on a ouvert
		#print(filename)												
		#print( filename )
		file = FilePath + "/" + filename								#xyz.txt fichier
		text = open( file , encoding="utf-8" )							#la texte dans cette fichier
		try:															#j'ai eu un probleme d'unicode donc j'utilise try/catch
			result = (text.read())										#on lise la texte
			tags = tagger.tag_text(result)								#on le tag
			for tag in tags:											#pour tous les mots dans le tag
				output.write(str(tag)+"\n")								#format fichier de sortie
		except:
			pass

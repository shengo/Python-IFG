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
#nltk.download()

#######################################################################

def get_word_features(all_words, stop_words, n):
	word_features=[]
	for w in list(all_words.keys())[:n]:
		if(not(w in stop_words)):
			word_features.append(w)
			
	return word_features

#######################################################################

def sent_features(sent):
	sent_words=set(sent)
	features={}
	for word in word_features:
		features['contains(%s)'%word]=(word in sent_words)
	return features

#######################################################################

tagger=treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='../treetagger')

inputFolder ="./articles/"			#repertoire de entree
outputFolder = "./articles/_tags/"		#repertoire de sortie
listeCategory = ["politique", "economie", "sport", "culture", "sciences"]	#les categories
#listeCategory = ["politique"]	#liste de listeCategory			#les categories (pour tester)

if not path.exists (outputFolder): 	# si repertoire n'existe pas
	makedirs(outputFolder)		# creer repertoire

#######################################################################


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



leMonde=CategorizedTaggedCorpusReader(outputFolder, r'(\w+)\.txt', cat_pattern=r'(\w+)\.txt')
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



documents=[(sent,category) 
	for category in leMonde.categories() 
	for sent in leMonde.sents(categories=category)]


random.shuffle(documents)
all_words=nltk.FreqDist(w.lower() for w in leMonde.words())
stop_words=["!", "\"", "(", ")", ",", "-elle", "-il", ".", "/", ":", ";", "?", "a","alors", "ans", "apparemment", "assez",  "au", "aucun","aujourd'hui", "aussi", "autant", "autre", "autrement", "aux", "avait","avant", "avant hier", "avec", "avoir", "beaucoup", "bien", "bon", "car","ce", "cela", "cependant", "certainement", "certes", "ces", "cette", "ceux","chaque", "ci", "comme", "comment", "d'abord", "dans", "davantage", "de", "dedans", "dehors", "demain", "depuis", "des", "deux", "devrait", "doit", "donc", "droite", "du","elle", "elles", "en",  "encore", "enfin", "ensuite",  "environ", "est", "et", "eu", "fait", "faites", "fois", "font","force", "grandement",  "habituellement",  "hier","ici", "il", "ils", "jadis", "jamais", "je", "joliment","la", "le", "les", "leur", "leurs", "longtemps", "lors", "ma", "maintenant", "mais", "mes", "moins","mon", "mot", "ne", "ni", "nommés","non", "notre", "nous", "nouveaux", "on", "ont", "ou", "oui","par", "parce que", "parfois", "pas", "personne", "personnes", "peu","peut", "peut-être", "pièce", "plupart", "plus", "plutôt", "point", "pour","pourquoi", "premièrement", "presque", "probablement","puis", "quand", "que", "quel", "quelle", "quelles", "quelque", "quelquefois", "quels","qui",  "resume", "rien", "sa", "sans", "se", "selon", "ses", "seulement", "si",  "soit", "son","sont", "soudain", "sous", "souvent", "soyez","suffisamment", "sur", "ta", "tandis", "tant", "tard", "tellement", "tel", "tels", "tes", "ton", "toujours", "tous", "tout", "toutefois", "trop", "tu",  "un", "une", "valeur",  "voie", "voient",  "votre", "vous", "y"]

word_features=get_word_features (all_words, stop_words, 300)
#print word_features
#print "\n success \n"

featuresets=[(sent_features(d),c)for (d,c) in documents]  # RAM overflow when many pages :(

x = int((total_phrases*70)/100)
y = int((total_phrases*30)/100)

print "\n x: ", x, " y: ", y, "\n"

train_set, test_set=featuresets[x:],featuresets[:y]
#print "\n train_set: ", train_set, "\ntest_set: ", test_set, "\n"

Classifier=nltk.NaiveBayesClassifier.train(train_set)
Classifier.show_most_informative_features(10)










	   


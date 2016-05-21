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

tagger=treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='../treetagger')

inputFolder ="./articles/"			#repertoire de entree
outputFolder = "./articles/_tags/"		#repertoire de sortie
listeCategory = ["politique", "economie", "sport", "culture", "sciences"]	#les categories
#listeCategory = ["politique"]							#1 categorie (pour tester)

if not path.exists (outputFolder): 	# si repertoire n'existe pas
	makedirs(outputFolder)		# creer repertoire

###############           Les fonctions :          ####################

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

def precision_recall (classifier, test_set): #pour faire listes des precissions et rappels
	refsets=collections.defaultdict(set)
	testset=collections.defaultdict(set)
	for i, (sent, category) in enumerate(test_set):
		refsets[category].add(i)
		observed=classifier.classify(sent)
		testset[observed].add(i)
	prec={}	#list pour preccision
	rapp={}	#list pour rappel
	for category in leMonde.categories(): #pour chaque categorie
		prec[category]=nltk.precision(refsets[category], testset[category]) 	#preccision pour cet categorie
		rapp[category]=nltk.recall(refsets[category],testset[category])		#rappel pour cet categorie
	return prec,rapp #returer ces listes

#######################################################################

def fmesures(): 				#fonction pour calcule fmesures

	for category in leMonde.categories():	#pour chaque categorie
		preccision = PREC[category]	#preccision pour cet categorie
		rappel = RAPP[category]		#rappel pour cet categorie
		
		if rappel+preccision==0: # si rappel+preccision==0, 2 * preccision * rappelva etre error
			print "for category", category , " : NONE\n"	
		else:
			f_mesure=(2 * preccision * rappel)/(preccision + rappel) #calculation de fmesure
			print "for category", category, "fmesure is" , f_mesure , "\n"


#######################################################################


for category in listeCategory:		# repertoires pour chaqun categorie
	
	FilePaths = inputFolder  + category		#repertoire d'entree
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


total_carac=0 	# Les nombre des caracteres dans chaque categorie
total_mots=0	# Les nombre des mots dans chaque categorie
total_phrases=0	# Les nombre des phrasses dans chaque categorie
total_vocabs=0	# Les nombre des vocabs dans chaque categorie

for category in leMonde.categories():	#pour chaque categorie
	
	nb_carac=len(leMonde.raw(categories=category))		# Les nombre des caracteres 
	nb_mots = len(leMonde.words(categories=category))	# Les nombre des mots dans 
	nb_phrases=len(leMonde.sents(categories=category))	# Les nombre des phrasses 
	nb_vocals=len(leMonde.words(categories=category))	# Les nombre des vocabs 
	
	total_carac = total_carac + nb_carac			#ajouter au total
	total_mots = total_mots + nb_mots			#ajouter au total
	total_phrases = total_phrases + nb_phrases		#ajouter au total
	total_vocabs = total_vocabs + nb_vocals			#ajouter au total
	
		
	

print "\n"
print "total_carac: ", total_carac
print "\n"

print "total_mots: ", total_mots
print "\n"

print "total_phrases: ", total_phrases
print "\n"

print "total_vocabs: ", total_vocabs
print "\n"



documents=[(sent,category) 
	for category in leMonde.categories() 
	for sent in leMonde.sents(categories=category)]


random.shuffle(documents)
all_words=nltk.FreqDist(w.lower() for w in leMonde.words()) #tous les mots
#les mots plus frequents:
stop_words=["a","alors", "ans", "apparemment", "assez",  "au", "aucun","aujourd'hui", "aussi", "autant", "autre", "autrement", "aux", "avait","avant", "avant hier", "avec", "avoir", "beaucoup", "bien", "bon", "car","ce", "cela", "cependant", "certainement", "certes", "ces", "cette", "ceux","chaque", "ci", "comme", "comment", "d'abord", "dans", "davantage", "de", "dedans", "dehors", "demain", "depuis", "des", "deux", "devrait", "doit", "donc", "droite", "du","elle", "elles", "en",  "encore", "enfin", "ensuite",  "environ", "est", "et", "eu", "fait", "faites", "fois", "font","force", "grandement",  "habituellement",  "hier","ici", "il", "ils", "jadis", "jamais", "je", "joliment","la", "le", "les", "leur", "leurs", "longtemps", "lors", "ma", "maintenant", "mais", "mes", "moins","mon", "mot", "ne", "ni", "nommés","non", "notre", "nous", "nouveaux", "on", "ont", "ou", "oui","par", "parce que", "parfois", "pas", "personne", "personnes", "peu","peut", "peut-être", "pièce", "plupart", "plus", "plutôt", "point", "pour","pourquoi", "premièrement", "presque", "probablement","puis", "quand", "que", "quel", "quelle", "quelles", "quelque", "quelquefois", "quels","qui",  "resume", "rien", "sa", "sans", "se", "selon", "ses", "seulement", "si",  "soit", "son","sont", "soudain", "sous", "souvent", "soyez","suffisamment", "sur", "ta", "tandis", "tant", "tard", "tellement", "tel", "tels", "tes", "ton", "toujours", "tous", "tout", "toutefois", "trop", "tu",  "un", "une", "valeur",  "voie", "voient",  "votre", "vous", "y", "!", "?", "-", "(", ")", ",", ".", ":", ";"]

word_features=get_word_features (all_words, stop_words, 300)
#print word_features
#print "\n success \n"

featuresets=[(sent_features(d),c)for (d,c) in documents]  # (RAM overflow when many pages) 

x = (total_phrases*70)/100 	#70% de total
y = (total_phrases*30)/100	#30% de total

print "\n x: ", x, " y: ", y, "\n"

train_set, test_set=featuresets[x:],featuresets[:y]
#print "\n train_set: ", train_set, "\ntest_set: ", test_set, "\n"

print "\n most informative features: \n"
Classifier = nltk.NaiveBayesClassifier.train(train_set)
mif = Classifier.most_informative_features(10)
print mif, "\n"

#Vrai Positive, Vrai Negative, Faux Positive, Faux Negative
#accuracy = (VP + VN)/(VP + VN + FP + FN))
#


accuracy = nltk.classify.accuracy(Classifier,test_set )
print "accuracy is: ", accuracy, "\n"

PrecisionRappel=precision_recall(Classifier, test_set)	# listes des precissions et rappels

PREC=PrecisionRappel[0]					# listes des precissions 
RAPP=PrecisionRappel[1]					# listes des rappels
print "\npreccision: ", PREC, "\n"
print "\nrappel: ", RAPP, "\n"

print "\n"

fmesures() 						#fonction pour calcule fmesures







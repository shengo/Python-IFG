#!/usr/bin/python3 
# -*- encoding : utf-8 -*- 
from __future__ import unicode_literals
import os
import codecs
import bs4
import random
import re
import treetaggerwrapper
import collections
import nltk
from urllib.request import urlopen
from nltk.classify import NaiveBayesClassifier
from nltk.corpus.reader import CategorizedTaggedCorpusReader
from os import path, makedirs
from bs4 import BeautifulSoup
from nltk import precision
from nltk import recall
def get_word_features(all_words, stop_words, n):
	word_features=[]
	for w in list(all_words.keys())[:n]:
		if(not(w in stop_words)):
			word_features.append(w)
	return word_features
#---------------------------------------------
def sent_features(sent):
	sent_words=set(sent)
	features={}
	for word in word_features:
		features['contains(%s)'%word]=(word in sent_words)
	return features
#---------------------------------------------
def precision_recall (classifier, test_set):
	refsets=collections.defaultdict(set)
	testset=collections.defaultdict(set)
	for i, (sent, category) in enumerate(test_set):
		refsets[category].add(i)
		observed=classifier.classify(sent)
		testset[observed].add(i)
	prec={}
	rec={}
	for category in leMonde.categories():
		prec[category]=nltk.precision(refsets[category], testset[category])
		rec[category]=nltk.recall(refsets[category],testset[category])
	return prec,rec
#---------------------------------------------
def fmesure(category):
	precc=float(PREC[category])
	rapp =float(RAPP[category])
	fm=(2*precc*rapp)/(precc+rapp)
	return category, fm

#nltk.download('all')
def nettoyenHTML(texte):
#fonction supprime le texte inutile et graphiques de l'article	
	pattern=re.compile(r'<p class="lire.*">\s+Lire.*[\s\S]+<\/a>\s+<\/p>',re.UNICODE)
	#enregistre une partie du code dans lequel est écrit "Lire (lire aussi, ...)" dans pattern		
	match=re.search(pattern,texte)
	#recherches dans l'article
	if match:
		texte=re.sub(pattern,'',texte)
		#si le motif est trouvé, il change par '', qu'il est supprimé	
	pattern1=re.compile(r'.*"container_.*.>\s+.[\s\S]+</div>',re.UNICODE)
	#enregistre le code de script dans la variable pattern
	match1=re.search(pattern1,texte)
	#Recherches motif dans l'article
	if match1:
		texte=re.sub(pattern1,'',texte)
		#si le motif est trouvé, il change par '', qu'il est supprimé
	pattern2=re.compile(r'<section class=".*>\s+.[\s\S]+</section>',re.UNICODE)
	#enregistre le code de script dans la variable pattern
	match2=re.search(pattern2,texte)
	#Recherches motif dans l'article
	if match2:
		texte=re.sub(pattern2,'',texte)
		#si le motif est trouvé, il change par '', qu'il est supprimé
	pattern3=re.compile(r'<script.+[\s\S]+<\/script>',re.UNICODE)
	#trouve la  pattern dans text
	match3=re.search(pattern3,texte)
	#Recherches motif dans l'article
	if match3:
		texte=re.sub(pattern3,'',texte)
		#si le motif est trouvé, il change par '', qu'il est supprimé
#	pattern4=re.compile(r'<style.+[\s\S]+<\/style>',re.UNICODE)
	pattern4=re.compile(r'div class="contenu-portfolio-atome">\s.[\s\S]*<\/a>\s.*\s.+',re.UNICODE)
	#enregistre le code de portefeuille dans la variable pattern
	match4=re.search(pattern4,texte)
	#Recherches motif dans l'article
	if match4:
		texte=re.sub(pattern4,'',texte)
		#si le motif est trouvé, il change par '', qu'il est supprimé
	pattern5=re.compile(r'<blockquote class="twitter.*>[\s\S]+<\/blockquote>',re.UNICODE)
	#enregistre le code de bloc de twitter dans la variable pattern
	match5=re.search(pattern5,texte)
	#Recherches motif dans l'article
	if match5:
		texte=re.sub(pattern5,'',texte)
		#si le motif est trouvé, il change par '', qu'il est supprimé
	pattern6=re.compile(r'<p class=".*">\s+Analyse :\s+[\s\S]+</p>',re.UNICODE)
	#enregistre une partie du code dans lequel est écrit "Analyse :" dans pattern
	match6=re.search(pattern6,texte)
	#Recherches motif dans l'article
	if match6:
		texte=re.sub(pattern6,'',texte)
		#si le motif est trouvé, il change par '', qu'il est supprimé
	
	
	return texte
	#renvoie l'article
def nettoyerEspaces(texte):
#supprimer les espaces inutiles de l'article
	pattern7=re.compile(r'[ \t\n\r\g\v]+',re.UNICODE)
	#enregistre tous les espaces blancs dans la variable pattern7
	match7=re.search(pattern7,texte)
	#recherches motif dans l'article
	if match7:
		texte=re.sub(pattern7,' ',texte)
		#si le motif est trouvé, il change par '', ce qui signifie qu'il est supprimé
	pattern8=re.compile(r'^( )+')
	#enregistre les espaces blancs qui sont au début de l'article dans la variable pattern8
	match8=re.search(pattern8,texte)
	#recherches motif dans l'article
	if match8:
		texte=re.sub(pattern8,'',texte)
		#si le motif est trouvé, il change par '', ce qui signifie qu'il est supprimé
	return texte
	#renvoie l'article
tagger=treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR="/home/miqa/Загрузки/treetagger")
#créer l'objet TreeTagger pour la langue française
outDir= "/home/miqa/shedegebi"
#définir le répertoire de sortie pour les articles
outDirtag="/home/miqa/shedegebi/Corpus/Tagged"
#définir le répertoire de sortie pour les fichiers tags
if not path.exists(outDir):
        makedirs(outDir)
#si outDir n'existe pas, créez
if not path.exists(outDirtag):
        makedirs(outDirtag)
#si outDirtag n'existe pas, créez

compteur=0
#compteur pour numerasion de fichier
listeCat=["politique","culture","economie","sport","sciences"]
#liste des catégories
for cat in listeCat:
#passer par toutes les catégories
	nomFichierTag="article_"+cat+"_tagged"+".txt"
	sousDir=outDir+'/'+cat
	#créer un répertoire pour la catégorie
	if not path.exists(sousDir):
                makedirs(sousDir)
	#variable avec nom de fichiers pour un article
	with codecs.open(os.path.join(outDirtag, nomFichierTag),"w",encoding="utf-8") as fouttag:
 	#écrire le fichier nomFichier dans un outDirtag répertoire avec encodage UTF-8
		for i in range (1,3):
		#Url avec categorie et page nombre variables
			url="http://www.lemonde.fr/{}/{}.html".format(cat,str( i))
			#prends tous le HTML de url specifie.
			fichier=urlopen(url)
			#ouvre url
			Soup=BeautifulSoup(fichier,"html5lib")
			#convertir la page HTML valide pour HTML
			blocURL=Soup.find_all(href=re.compile(r'\/\S+\/article\/\S+\.html'))
			#trouver toutes les urls de l'article sur la page
			for e in blocURL:
			#passer  toutes les urls
				url=e["href"]
				#ca donne un complete URL pour article
				url="http://www.lemonde.fr"+url
				#nom pour chaque fichier avec variable counter
				nomFichier="article_"+cat+"_"+str(compteur)+".txt"
				#augmenter la valeur variable pour le prochain fichier article.
				compteur=compteur+1
				


#print url
				fichier=urlopen(url)
				#url ouverte
				Soup=BeautifulSoup(fichier,"html5lib")
				#convertir la page HTML valide pour HTML
				article=Soup.find(id=re.compile("articleBody"))
				#article=article.get_text()
				article=str(article)
				
				article=nettoyenHTML(article)
				article=BeautifulSoup(article,"html5lib")
				#prends soulement le texte sans HTML tags
				article=article.get_text()
				#nettoyer beucoup de whitespaces
				article=nettoyerEspaces(article)
				#fichier ouvrts avec certaine encoding avec write permission, Pour ecrire article texte dans eux
				with codecs.open(os.path.join(sousDir,nomFichier), "w" ,encoding="utf-8") as fout:
					fout.write(article)
				fout.close()
				#il cree la liste tgs avec en taggant les articles
				tags=tagger.tag_text(article)
				#boucle par tags et ecrire dans le fichier
				for tag in tags:
					fouttag.write(tag+"\n")
	compteur=0
fouttag.close()		
		#	print article
leMonde=CategorizedTaggedCorpusReader('/home/miqa/shedegebi/Corpus/Tagged',r'\S+_tagged\.txt',cat_pattern='article_(\w+)_tagged\.txt')
nb_car_all=0
nb_mot_all=0
nb_phras_all=0
nb_vocab_all=0		
for category in leMonde.categories(): 
#les variables pour Les nombre de categories,mots,phrasses et vocab par chaque categorie
	print ("ok")
	nb_caracteres=len(leMonde.raw(categories=category))
	nb_mots=len(leMonde.words(categories=category))
	nb_phrases=len(leMonde.sents(categories=category))
	#mots differants dan cattegorie
	nb_vocab=len(set([w.lower() for w in leMonde.words(categories=category)]))	
	nb_car_all=nb_car_all+nb_caracteres
	nb_mot_all=nb_mot_all+nb_mots
	nb_phras_all=nb_phras_all+nb_phrases
	nb_vocab_all=nb_vocab_all+nb_vocab
	#print info et nombres
	print ("nombre ce caracters dans" + category+ ":" +str(nb_caracteres)+"\n"
+"nombre de mots  dans" + category+ ":" +str(nb_mots)+"\n"
+"nombre de phrases dans" + category+ ":" +str(nb_phrases)+"\n"	
+"nombre de vocabulaire dans" + category+ ":" +str(nb_vocab)+"\n")
print("total caracteres" + str(nb_car_all)+"\n"+"total mots"+ str(nb_mot_all)+"\n"+"total phrases"+ str(nb_phras_all)+"\n"+"total vocab"+str(nb_vocab_all))
documents=[(sent,category) for category in leMonde.categories() for sent in leMonde.sents(categories=category)]
random.shuffle(documents)
all_words=nltk.FreqDist(w.lower() for w in leMonde.words())
stop_words=["!", "\"", "(", ")", ",", "-elle", "-il", ".", "/", ":", ";", "?", "a", "absolument", "actuellement", 
"ainsi","alors", "ans", "apparemment", "approximativement", "après", "après demain", "assez", "assurément", "au",
"aucun", "aucunement", "aucuns","aujourd'hui", "auparavant", "aussi", "aussitôt", "autant", "autre", "autrefois",
"autrement", "aux", "avait","avant", "avant hier", "avec", "avoir", "beaucoup", "bien", "bientôt", "bon", "c'", "car",
"carrément", "ce", "cela", "cependant", "certainement", "certes", "ces", "cette", "ceux","chaque", "ci", "comme", 
"comment", "complètement", "d'", "d'abord", "dans", "davantage", "de", "dedans", "dehors", "demain", "depuis",
"derechef", "des", "deux", "devrait", "diablement", "divinement", "doit", "donc",
"dorénavant", "dos", "droite", "drôlement", "du", "début","déjà", "désormais", "elle", "elles", "en", "en vérité", "encore",
"enfin", "ensuite", "entièrement", "entre temps", "environ", "essai","est", "et", "eu", "extrêmement", "fait", "faites", "fois",
"font","force", "grandement", "guère", "habituellement", "haut", "hier","hors","ici", "il", "ils", "infiniment", "insuffisamment",
"jadis", "jamais", "je", "joliment", "l'", "la", "le", "les", "leur", "leurs", "longtemps", "lors", "là", "ma", "maintenant", "mais",
 "mes", "moins","mon", "mot", "même", "n'", "naguère", "ne", "ni", "nommés","non", "notre", "nous", "nouveaux", "nullement",
  "on", "ont", "ou", "oui", "où","par", "parce que", "parfois", "pas", "pas mal", "passablement", "personne", "personnes", "peu",
"peut", "peut-être", "pièce", "plupart", "plus", "plutôt", "point", "pour","pourquoi", "premièrement", "presque", "probablement",
 "prou", "précisément", "puis","qu'", "quand", "quasi", "quasiment", "que", "quel", "quelle", "quelles", 
"quelque", "quelquefois", "quels","qui", "quotidiennement", "resume", "rien","rudement", "s'", "sa", "sans", "sans doute", "se",
"selon", "ses", "seulement", "si", "sien", "sitôt", "soit", "son","sont", "soudain", "sous", "souvent", "soyez", "subitement", "suffisamment", "sur",
 "t'", "ta", "tandis", "tant", "tantôt", "tard", "tellement", "tel", "tels","terriblement", "tes", "ton", "totalement", "toujours", "tous", "tout", 
"tout à fait", "toutefois", "trop", "très", "tu", "tôt", "un", "une", "valeur", "vers", "voie", "voient", "volontiers", 
"vont", "votre", "vous", "vraiment", "vraisemblablement", "y'", "y", "à", "à demi", "à peine", "à peu près", "ça","étaient", "état", "étions", "été", "être"]
word_features=get_word_features (all_words, stop_words,400)
featuresets=[(sent_features(d),c)for (d,c) in documents]
#d-phrase , c-categorie
train_set, test_set=featuresets[int((nb_phras_all*70)/100):],featuresets[:int((nb_phras_all*30)/100)]
Classifier=nltk.NaiveBayesClassifier.train(train_set)
PrecisionRappel=precision_recall(Classifier, test_set)
PREC=PrecisionRappel[0]
RAPP=PrecisionRappel[1]
print (PREC)
print (RAPP)
for category in leMonde.categories():
	try:
		print (fmesure(category))
	except:
		print("("+"'"+category+"'"+",pas de valeur)")

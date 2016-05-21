#!/usr/bin/python
#-*-encoding:utf-8-*-
#---------------------------------------------------------------------------------------------------------
#bloc des importations
from __future__ import unicode_literals
from os import path,makedirs
import codecs
import urllib2
import os
from bs4 import BeautifulSoup
import re
import treetaggerwrapper
import nltk
from nltk.corpus.reader import CategorizedTaggedCorpusReader	
#nltk.download('all')
#---------------------------------------------------------------------------------------------------------
def nettoyerHTML(texte):	#fonction qui supprime le texte inutile comme des balises HTML
    pattern=re.compile(r'<p class="lire.*">\s+Lire.*[\s\S]+<\/p>',re.UNICODE)	#regex qui marque les lignes qui contient 'Lire aussi:' et etc
    match=re.search(pattern, texte)		#motif de recherche dans le texte
    if match:	#si le motif a été trouvé faire à la suite
        texte=re.sub(pattern,'',texte)	#changer tout trouvé avec ''
    pattern=re.compile(r'(<blockquote class="twitter-tweet">\s.*\s+.*\s+</blockquote>)',re.UNICODE)	#marque widget tweeters
    match=re.search(pattern, texte)	#motif de recherche dans le texte
    if match:	#si le motif a été trouvé faire à la suite
        texte=re.sub(pattern,'',texte)	#changer tout trouvé avec ''
    pattern=re.compile(r'<script[\s\S]+<\/script>',re.UNICODE)	#marque toutes les lignes contenant balise <script>
    match=re.search(pattern, texte)	#motif de recherche dans le texte
    if match:	#si le motif a été trouvé faire à la suite
        texte=re.sub(pattern,'',texte)	#changer tout trouvé avec ''
    pattern=re.compile(r'<div class="contenu-portfolio-atome">\s.[\s\S]*<\/a>\s.*\s.+',re.UNICODE)	#marque portfolio
    match=re.search(pattern, texte)	#motif de recherche dans le texte
    if match:	#si le motif a été trouvé faire à la suite
        texte=re.sub(pattern,'',texte)	#changer tout trouvé avec ''
    return texte	#retourne le texte modifié
#----------------------------------------------------------------------------------------------------------
def nettoyerEspaces(texte):		#fonction qui supprime les espaces inutiles et les lignes
    pattern1=re.compile(r'[ \t\n\r\f\v]+',re.UNICODE)	#enregistre tous les espaces blancs dans la variable pattern1
    match1=re.search(pattern1, texte)	#motif de recherche dans le texte
    if match1:	#si le motif a été trouvé faire à la suite
        texte=re.sub(pattern1,' ',texte)	#changer tout trouvé avec ' '
    pattern2=re.compile(r'^( )+')	#enregistre les espaces blancs qui sont au début de l'article dans la variable pattern2
    match2=re.search(pattern2, texte)	#motif de recherche dans le texte
    if match2:	#si le motif a été trouvé faire à la suite
        texte=re.sub(pattern2,' ',texte)	#changer tout trouvé avec ' '
    return texte	#retourne le texte modifié
#-----------------------------------------------------------------------------------------------------------
tagger=treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='/home/xguest/TreeTagger')	#create a tags and save it in /home/xguest/TreeTagger et la langue est le français
outDir="/home/xguest/articles"		#répertoires où les articles sont enregistrés
outDirtag="/home/xguest/Corpus/Tagged"	#répertoires où des articles avec des étiquettes sont enregistrées
if not path.exists(outDirtag):	#si le répertoire suivant n'existe pas faire à la suite
    makedirs(outDirtag)	#créer le répertoire suivant
if not path.exists(outDir):	#	#si le répertoire suivant n'existe pas faire à la suite
    makedirs(outDir)	#créer le répertoire suivant
counter=0;	#initialiser compteur
listeCat=["politique","culture","economie","sport","sciences"]	#initialiser le conteneur avec des catégories
for i in listeCat:	#faire à la suite pour chaque catégorie
    SousDir=outDir+'/'+i;	#initialiser la variable qui sera un nom de répertoire où les articles seront sauvegardés par catégorie
    if not path.exists(SousDir):	#si le répertoire suivant n'existe pas faire à la suite
        makedirs(SousDir)	#créer le répertoire suivant
    nomFichier="articles_"+i+"_"+"tagged"+".txt"	#variable nom qui contiendra mots marqués
    with codecs.open(os.path.join(outDirtag,nomFichier),"w",encoding="utf-8") as fouttag:	#écrire une sortie pour générer le fichier dans le dossier généré avec l'encodage 'utf-8'
        for j in range (0,2):	#itérer 0-2 parce que chaque catégorie a plusieurs pages de messages
            url="http://www.lemonde.fr/{}/{}.html".format(i,j);	#url ouverte: site / catégorie / page / numéro de poste
            fichier=urllib2.urlopen(url)	#url variable est égale à l'adresse de l'article
            Soup=BeautifulSoup(fichier,"html5lib")	#convertir la page HTML valide pour HTML
            blocURLS=Soup.find_all(href=	
                                  re.compile(r'\/\S+\/article\/\S+.html'))	#trouver toutes les urls de l'article sur la page
            for e in blocURLS:	#itérer sur tous les maillons de 'blocURLS'-s
                #générer article URL
				url=e["href"]	
                url="http://www.lemonde.fr"+url	
                nomFichier="article_"+i+"_"+unicode(counter)	
                counter=counter+1	#augmenter compteur avec un
                fichier=urllib2.urlopen(url)	#url variable est égale à l'adresse de l'article
                Soup=BeautifulSoup(fichier,"html5lib")	#convertir la page HTML valide pour HTML
                #prendre le texte de l'article
				article=Soup.find(id=re.compile("articleBody"))	
                article=unicode(article)	
                article=nettoyerHTML(article)	#l'utilisation de la fonction nettoyerHTML
                article=BeautifulSoup(article,"html5lib")	##convertir la page HTML valide pour HTML
                article=article.get_text()	
                article=nettoyerEspaces(article)	##l'utilisation de la fonction nettoyerEspaces
                with codecs.open(os.path.join(SousDir,nomFichier+".txt"),"w",encoding="utf-8") as fout:	#écrire l'article du texte dans le fichier
                    fout.write(article)	
                fout.close()	
                tags=tagger.tag_text(article)      	               
                for tag in tags:	
                    fouttag.write(tag+"\n")	#écrire des balises dans le fichier
    counter=0	#réinitialiser le compteur
fouttag.close()	
leMonde=CategorizedTaggedCorpusReader('/home/xguest/Corpus/Tagged',r'\S+_tagged\.txt',cat_pattern='articles_(\w+)_tagged\.txt')	#écrire dans Lemonade conteneur entier étiqueté matériel
for category in leMonde.categories():	#itérer sur tous les maillons de 'leMonde.categories'-s
    print ("ok")	#Imprimer 'ok'
    nb_caracteres=len(leMonde.raw(categories=category))	#enregistrer nombre de caractères nb_caracteres
    nb_mots=len(leMonde.words(categories=category))	#enregistrer nombre de caractères nb_mots
    nb_phrases=len(leMonde.sents(categories=category))	#enregistrer nombre de caractères nb_phrases
    nb_vocab=len(set([w.lower() for w in leMonde.words(categories=category)]))	#enregistrer vocabulaires de caractères nb_vocab
    print ("nombre ce caracters dans" + category+ ":" +str(nb_caracteres)+"\n"	#informations d'impression
           +"nombre de mots  dans" + category+ ":" +str(nb_mots)+"\n"	
           +"nombre de phrases dans" + category+ ":" +str(nb_phrases)+"\n"	
           +"nombre de vocabulaire dans" + category+ ":" +str(nb_vocab)+"\n")	
   

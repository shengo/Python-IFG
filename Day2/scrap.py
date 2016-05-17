#!/usr/local/bin/python2
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re, os, urllib2, bs4, codecs
from os import path, makedirs
from bs4 import BeautifulSoup



outDir = "./test3"
if not path.exists(outDir):
    makedirs(outDir)

compteur =0

listeCategories = ["politique", "economie", "culture", "sport", "sciences"]
for categorie in listeCategories :

    out = outDir+"/"+categorie
    if not path.exists(out):
        makedirs(out)

    for i in range(1,3):
        urlCat = r'http://www.lemonde.fr/{}/{}.html'.format(categorie, i)
        file = urllib2.urlopen(urlCat)
        soup = BeautifulSoup(file, 'html5lib')
        blocsURLS = soup.find_all(href=re.compile(r'\/\S+\/article\/\S+\.html'))

        for e in blocsURLS :
            url = e["href"]
            url = "http://www.lemonde.fr" + url
            
            compteur = compteur+1
            nomFichier = r'article_{}_{}.txt'.format(categorie, compteur)
            file = urllib2.urlopen(url)
            soup = BeautifulSoup(file, 'html5lib')
         
         
            article1 = soup.find("div", {"id" : re.compile(r'.*article.*')})
            article2 = soup.find("div", {"class" : re.compile(r'.*article.*')})
            
            
            if article1 :
                article = article1.get_text()
            elif article2 :
                article = article2.get_text()
            else :
                pass
            if article :
                with codecs.open(os.path.join(out, nomFichier), 'w', encoding='utf-8') as fout :
                    fout.write(article)
                fout.close()
compteur = 0


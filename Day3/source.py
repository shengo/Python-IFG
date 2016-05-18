#!/usr/local/lib/python2.7
from __future__ import unicode_literals
import urllib2
import os
import re
from os import path, makedirs
from bs4 import BeautifulSoup
import codecs
import gettext


def removeExtraCode(arti):
    pattern=re.compile(r'(<style.*?>([\s\S]*?)<\/style>)',re.UNICODE)
    match=re.search(pattern, arti)
    if match:
        arti=re.sub(pattern,'',arti)

    pattern = re.compile(r'<script[\s\S]+<\/script>', re.UNICODE)
    match = re.search(pattern, arti)
    if match:
        arti = re.sub(pattern, '', arti)

    pattern = re.compile(r'<p class="lire.*">\s+Lire.*[\s\S]+<\/p>/gi', re.UNICODE)  # for read more links
    match = re.search(pattern, arti)
    if match:
        arti = re.sub(pattern, '', arti)
    return arti
def nettoyerEspaces(texte):
    pattern1 = re.compile(r'[ \t\n\r\f\v]+', re.UNICODE)  # all empy lines.spaces...
    match1 = re.search(pattern1, texte)
    if match1:
        texte = re.sub(pattern1, ' ', texte)

    pattern2 = re.compile(r'^( )+')
    match2 = re.search(pattern2, texte)  # blank spaces in the beggining of article
    if match2:
        texte = re.sub(pattern2, ' ', texte)
    return texte


def myDecompose(soup,tag,attr,val):
    n = len(tag)
    resObj = [0] * n
    for i in range(0,n):
        resObj[i] = soup.find_all(tag[i], {attr[i]: re.compile(r'%s'%(val[i]))})
    for i in range(0,n):
        if resObj[i]!=0:
            for ele in resObj[i]:
                soup = ele.decompose()
    return soup

out="/home/dachi/Documents/tmp/"
if not path.exists(out):
    makedirs(out)
listeCat = [
    'politique'
] # category-ebi
# listeCat = [
#     'politique',
#     'economie',
#     'sport',
#     'culture',
#     'sciences'
# ] # category-ebi
for cat in listeCat:
    mtvleli = 0
    outCat=out+'/'+cat
    if not path.exists(outCat):
        makedirs(outCat)
    for i in range(1,6):
        urlCat = r'http://www.lemonde.fr/{}/{}.html'.format(cat,i)
        file = urllib2.urlopen(urlCat)
        soup = BeautifulSoup(file, 'html5lib')
        blockURLS = soup.find_all(href=re.compile(r'\/\S+\/article\/\S+\.html'))
        for e in blockURLS:
            url = e['href']
            url = 'http://lemonde.fr/'+url # aq davitriet article-s url
            mtvleli+=1
            nomFichier='article_'+cat+'_'+unicode(mtvleli) + '.txt' # aq davitriet failis saxeli
            file = urllib2.urlopen(url)
            soup = BeautifulSoup(file, 'html5lib')

            article1 = soup.find('div',{'id': re.compile(r'.*article.*')})
            article2 = soup.find('div', {'class': re.compile(r'.*article.*')})

            soup = myDecompose(soup,
                               ['div',
                                'blockquote'],
                               ['class',
                                'class'],
                               ['snippet',
                                'twitter-tweet'])

            if article1:
                article = unicode(article1)
                article = removeExtraCode(article)
                article = BeautifulSoup(article, "html5lib")
                article = article.get_text()
                article = nettoyerEspaces(article)
            elif article2:
                article = unicode(article2)
                article = removeExtraCode(article)
                article = BeautifulSoup(article, "html5lib")
                article = article.get_text()
                article = nettoyerEspaces(article)


            with codecs.open(os.path.join(outCat,nomFichier),'w',encoding='UTF-8') as fout:
                fout.write(article)
                fout.close()

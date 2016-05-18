#!/usr/local/lib/python2.7
# -*- coding: utf-8 -*-



from __future__ import unicode_literals
import urllib2
import os
import codecs
from os import path, makedirs
import re
import treetaggerwrapper
from bs4 import BeautifulSoup
out="./testregexp/"
outFortag="./tags2/"
counter =0
tagger=treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='../treetagger')


if not path.exists (outFortag): 	# si repertoire existe
	makedirs(outFortag)		# si repertoire n'existe pas, cree

from __future__ import with_statement

PATH = "./testregexp/"

for path, dirs, files in os.walk(PATH):
    for filename in files:
        fullpath = os.path.join(path, filename)
        with open(fullpath, 'r') as f:
            data = re.sub(r'(\s*function\s+.*\s*{\s*)',
                r'\1echo "The function starts here."',
                f.read())
        with open(fullpath, 'w') as f:
            f.write(data)







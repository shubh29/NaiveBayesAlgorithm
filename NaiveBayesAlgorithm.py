# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:46:20 2015

@author: User
"""

import csv
import random
import math
import os
import nltk
import re

# Get stop words
stopwords = nltk.corpus.stopwords.words('english')

documentTerms = {}

def loadDocument():
    for file in os.listdir(os.getcwd()):
         if file.endswith(".txt"):
              fileOpen = open(file,'r')
              fileRead = fileOpen.read()
              documentTerms[file] = [w.lower() for w in nltk.word_tokenize(fileRead) if w.lower() not in stopwords and re.compile(r'^[a-z]+$').search(w.lower()) is not None]
              print(len(documentTerms[file]))
loadDocument()

#testing commit
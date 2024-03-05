# -*- coding: utf-8 -*-
__author__ = "S. Burleigh, Food Technology, Lund University"
__email__ = "stephen.burleigh@food.lth.se"
__status__ = "Development"
__copyright__ = "2022, Lund University"

"""
Takes website data as input and generates spreadsheet for the gap analysis. 
Uses website_data.csv, extra_stopwords.csv and keywords.csv from Zenodo Repository, 10.5281/zenodo.10782379.
"""

#imports
import sys
from sys import exit
import os
import pandas as pd
import re
from wordcloud import STOPWORDS
from collections import defaultdict

#variables
PROJ = 'Gap3'
doc = 'website_data.csv' 
kwdoc = 'keywords.csv'

#dirs
cwd = os.getcwd()
cwd = cwd.replace("\\", "/")
projdir = cwd + '/Projects/' +  PROJ + '/'
datadir = projdir + 'Files/'

#make work folders
folds = [projdir,datadir]
for fold in folds:
    if not os.path.exists(fold):
        os.makedirs(fold)
        
#load website data
fil = datadir + doc
df = pd.read_csv(fil, sep = "\t")
ID = df['ID'].tolist()
region = df['Region'].tolist()
country = df['Country'].tolist()
university = df['University'].tolist()
program = df['Program'].tolist()
texts = df['Text'].tolist()

#get extra stopwords
mystops = []
FH3 = open(datadir + 'extra_stopwords.csv')
lines = FH3.readlines()
for line in lines:
    line = line.rstrip()
    line = line.lower()
    mystops.append(line)
mystops = list(set(mystops))

#cleaning function
def cleantext(text):
    cnts = 0
    cleaned_words = []
    words = text.split()
    for word in words:    
        word = word.rstrip()
        word = re.sub(r"[^a-zA-Z]", " ", word) 
        word = word.lower()           
        if len(word) > 3:
            if len(word) < 20: 
                if word not in mystops:                    
                    if word not in STOPWORDS:
                        cleaned_words.append(word)
                        cnts += 1
    return (cleaned_words, cnts)

#load keywords
fil = datadir + kwdoc
df3 = pd.read_csv(fil, sep = "\t")

#make kw dictionary
kwdict = df3.to_dict(orient = 'list')

#clean text
wordslist = []
wrdcnts = []
for text in texts:
    (clwords,cnts) = cleantext(text)
    wordslist.append(clwords)
    wrdcnts.append(cnts)

#count kws in texts
countdict = defaultdict(list)
for words in wordslist:
    for k,v in kwdict.items():
        hits = 0        
        for kw in v:
            for word in words:
                if kw == word:
                    hits += 1
        countdict[k].append(hits)

#Make a new df
df2 = pd.DataFrame(countdict)

#make new df
df = pd.DataFrame(list(zip(ID, region, country, university, program, texts, wordslist,wrdcnts)),columns =['ID', 'Region','Country','University','Program','Text','Words','Docsize'])
df = pd.concat([df, df2], axis=1)

#save
fil = datadir + PROJ + '_' + 'add_keywords.csv'
df.to_csv(fil, index=False, sep="\t") 


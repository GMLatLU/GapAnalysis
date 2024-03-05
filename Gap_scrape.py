# -*- coding: utf-8 -*-
"""
Simple method to scrape a list of links from a website. Used to build the starting document website_data.csv.
"""

#imports
import sys
from sys import exit
import os
import pandas as pd
from bs4 import BeautifulSoup
import urllib3

#variables
PROJ = 'Gap3'
doc = 'program_websites.csv'
region = 'NEurope'
country = 'Finland'
uni = 'UEF'
dep = 'EuroForestry'
deptype = 'Forestry'
ID = country + '_' + uni + '_' + dep

#dirs
cwd = os.getcwd()
cwd = cwd.replace("\\", "/")
projdir = cwd + '/Projects/' +  PROJ + '/'
datadir = projdir + 'Files/'
resultsdir = projdir + 'Results/'

#make work folders
folds = [projdir,datadir,resultsdir]
for fold in folds:
    if not os.path.exists(fold):
        os.makedirs(fold)
        
#load website data
fil = datadir + PROJ + '_' + doc
df = pd.read_csv(fil, sep = "\t")
sites = df['sites'].tolist()

#scrape
texts = []
for site in sites:
    http = urllib3.PoolManager()
    response = http.request('GET', site)
    soup = BeautifulSoup(response.data.decode('utf-8'),features="html.parser")
    text = soup.get_text()
    text = text.replace("\n", ' ')

    #join all scrapes
    texts.append(text)
    texts.append('*******')

#collect all scrapes as string
textstr = ' '.join(texts)
textstr = textstr.replace("\n", ' ')
textstr = textstr.replace("\r", ' ')
textstr = " ".join(textstr.split())

#save
fil = datadir + region + '_' + country + '_' + uni + '_' + dep + '.csv'
FH1 = open(fil,'w',encoding='utf-8')
FH1.write('ID' + "\t" + ID + "\n")
FH1.write('Region' + "\t" + region + "\n")
FH1.write('Country' + "\t" + country + "\n")
FH1.write('University' + "\t" + uni + "\n")            
FH1.write('Department' + "\t" + dep + "\n")
FH1.write('Deptype' + "\t" + deptype + "\n")         
FH1.write('Words' + "\t" + textstr + "\n")    
FH1.close()        

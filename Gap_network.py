# -*- coding: utf-8 -*-

#imports
import os
import sys
from sys import exit
import pandas as pd
from collections import defaultdict

#variables
PROJ = 'Gap3'
doc = 'add_keywords.csv' 

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

#drop columns
droplist = ['ID','Text','Words','Forestry','Agriculture','Food','Innov','LifeLearn','Network','StratMan','Sustain','SysThink','TechKnow','Versatility']
df = df.drop(columns=droplist)
region = df['Region'].tolist()
country = df['Country'].tolist()
university = df['University'].tolist()
program = df['Program'].tolist()
docsize = df['Docsize'].tolist()

#counts
countdict = defaultdict(list)
for i in range(len(df)):
    countdict[region[i]].append(docsize[i])
    countdict[country[i]].append(docsize[i])
    countdict[university[i]].append(docsize[i])
    countdict[program[i]].append(docsize[i])

#sums
sumdict = {}
for k,v in countdict.items():
    sumdict[k] = sum(v)

#test
for k,v in sumdict.items():
    print(k,'->',v)

#make node csv
dfnodes = pd.DataFrame(sumdict.items(), columns=['Nodes', 'Docsize'])

#save
fil = fil[:-4] + '_nodes.csv'
dfnodes.to_csv(fil, sep='\t', index=False) 

#make edges csv
n1 = []
n2 = []
value = []
done = []
for i in range(len(df)):
    #region
    pair = region[i] + '_' + country[i]
    if pair not in done:
        n1.append(region[i])
        n2.append(country[i])
        value.append(sumdict[country[i]])
        done.append(pair)

    #country    
    pair = country[i] + '_' + university[i]  
    if pair not in done:    
        n1.append(country[i])
        n2.append(university[i])
        value.append(sumdict[university[i]])
        done.append(pair)

    #univeristy
    n1.append(university[i])
    n2.append(program[i])
    value.append(sumdict[program[i]])

   
#build node csv
dfedges = pd.DataFrame(list(zip(n1,n2,value)),columns=['N1','N2','Docsize'])

#save
fil = fil[:-10] + '_edges.csv'
dfedges.to_csv(fil, sep='\t', index=False) 

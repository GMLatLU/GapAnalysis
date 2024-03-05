# -*- coding: utf-8 -*-

#imports
import sys
from sys import exit
import os
import pandas as pd
import matplotlib.pyplot as plt

#variables
PROJ = 'Gap3'
doc = 'add_keywords_rel.csv'

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

#drop unwanted columns
droplist = ['ID','Region','Country','University','Program','Text','Words','Docsize','Forestry','Agriculture','Food','Innov','LifeLearn','Network','StratMan','Sustain','SysThink','TechKnow','Versatility','EEurope','NEurope','SEurope','WEurope']
df = df.drop(columns=droplist)

#sum all values
df = df.sum(axis=0)

#plot
exp = (0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,0.2)
df.plot(kind='pie',subplots=True,autopct='%1.1f%%',explode=exp,startangle=140, textprops={'fontsize': 12})

#Save the figure and show
plt.tight_layout()
plt.savefig(resultsdir + PROJ + '_piechart.png', format='png', dpi=1200)
plt.show()
plt.close() 

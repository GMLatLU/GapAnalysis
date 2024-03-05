# -*- coding: utf-8 -*-

"""
converts keyword scores to values relative to docsize (word count) for each program
"""

import os
import sys
from sys import exit
import pandas as pd

#variables
PROJ = 'Gap3'
doc = 'add_keywords.csv' 

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
fil = datadir + PROJ + '_' + doc
df = pd.read_csv(fil, sep = "\t")
#df = df.sample(100)

#rel to Docsize
colstorel = ['Forestry','Agriculture','Food','Sustain','Innov','Network','StratMan','SysThink',	'TechKnow',	'Versatility','LifeLearn']
for col in colstorel:
    df[col] = (df[col] / df["Docsize"]*100)

#region categories
df = pd.concat([df, pd.get_dummies(df['Region'])], axis=1)

#cross-sector categories
ag = []
fore = []
foo = []
agrifood = []
agriforestry = []
foodforestry = []
inter = []
other = []

#get data
agdata = df['Agriculture'].tolist()
fordata = df['Forestry'].tolist()
foodata= df['Food'].tolist()

for i in range(len(agdata)):
     if agdata[i] != 0 and fordata[i] == 0 and foodata[i] == 0:
         ag.append(1)            
         fore.append(0)      
         foo.append(0)                                
         agrifood.append(0)
         agriforestry.append(0)
         foodforestry.append(0)        
         inter.append(0)                   
         other.append(0)         
     elif agdata[i] == 0 and fordata[i] != 0 and foodata[i] == 0:
         ag.append(0)            
         fore.append(1)      
         foo.append(0)                                
         agrifood.append(0)
         agriforestry.append(0)
         foodforestry.append(0)        
         inter.append(0)                   
         other.append(0)            
     elif agdata[i] == 0 and fordata[i] == 0 and foodata[i] != 0:
         ag.append(0)            
         fore.append(0)      
         foo.append(1)                                
         agrifood.append(0)
         agriforestry.append(0)
         foodforestry.append(0)        
         inter.append(0)                   
         other.append(0)            
     elif agdata[i] != 0 and fordata[i] == 0 and foodata[i] != 0:
         ag.append(0)            
         fore.append(0)      
         foo.append(0)                                
         agrifood.append(1)
         agriforestry.append(0)
         foodforestry.append(0)        
         inter.append(0)                   
         other.append(0)            
     elif agdata[i] != 0 and fordata[i] != 0 and foodata[i] == 0:
         ag.append(0)            
         fore.append(0)      
         foo.append(0)                                
         agrifood.append(0)
         agriforestry.append(1)
         foodforestry.append(0)        
         inter.append(0)                   
         other.append(0)          
     elif agdata[i] == 0 and fordata[i] != 0 and foodata[i] != 0:
         ag.append(0)            
         fore.append(0)      
         foo.append(0)                                
         agrifood.append(0)
         agriforestry.append(0)
         foodforestry.append(1)        
         inter.append(0)                   
         other.append(0)
     elif agdata[i] != 0 and fordata[i] != 0 and foodata[i] != 0:
         ag.append(0)            
         fore.append(0)      
         foo.append(0)                                
         agrifood.append(0)
         agriforestry.append(0)
         foodforestry.append(0)        
         inter.append(1)                   
         other.append(0)            
     elif agdata[i] == 0 and fordata[i] == 0 and foodata[i] == 0:
         ag.append(0)            
         fore.append(0)      
         foo.append(0)                                
         agrifood.append(0)
         agriforestry.append(0)
         foodforestry.append(0)        
         inter.append(0)                   
         other.append(1)            
        
#add columns
df['Justag'] = ag
df['Justfor'] = fore
df['Justfood'] = foo
df['Agrifood'] = agrifood
df['Agriforestry'] = agriforestry
df['FoodForestry'] = foodforestry
df['Interdisciplinary'] = inter
df['Other'] = other

#save
fil = fil[:-4] + '_rel.csv'
df.to_csv(fil, sep='\t', index=False) 

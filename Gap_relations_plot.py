# -*- coding: utf-8 -*-

#imports
import os
import sys
from sys import exit
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

"""
create a relations plot showing the degree to which each program (colored by region) is associated with ag, food and forestry.
"""

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
print(df)

#drop rows of other category
agdata = df['Agriculture'].tolist()
fordata = df['Forestry'].tolist()
foodata= df['Food'].tolist()
tossinds = []
for i in range(len(agdata)):    
    if agdata[i] == 0 and fordata[i] == 0 and foodata[i] == 0:
        tossinds.append(i)
print('start',len(df))
df.drop(tossinds, axis=0, inplace=True)
print('remaining',len(df))

#get regions for color
region = df['Region'].tolist()

#drop unneeded cols
df = df.drop(columns=['ID','Country', 'University', 'Region', 'Text', 'Words', 'Docsize', 'Innov', 'LifeLearn', 'Network', 'StratMan', 'Sustain', 'SysThink', 'TechKnow', 'Versatility'])

#sum columns
df = df.groupby(['Program']).sum().round(2)
fil = datadir + PROJ + '_stats.csv'
df.to_csv(fil, sep='\t') 
df = pd.read_csv(fil, sep = "\t")
"""
                     Program  Forestry  Agriculture  Food
0             Aarhus_AgroBio         3           83    47
1        Aarhus_AgroEnvManag         2           37     9
2             Aarhus_BioTech         0            0     1
"""

#gather data as sums
program = df['Program'].tolist()
Ag = df['Agriculture'].tolist()
For = df['Forestry'].tolist()
Foo = df['Food'].tolist()

#get sum of col for normalization of size
catlist = ['Agriculture','Forestry','Food']
df['total']= df.loc[:,catlist].sum(axis=1)
siz = df['total'].tolist() #totals

#colors based on region, except for catlist
regioncolor = {'EEurope':'pink','NEurope':'lightblue','WEurope':'orange','SEurope':'tan'}
catcolor = {'Food':'blue','Forestry':'green','Agriculture':'red'}
for i in range(len(program)):
    catcolor[program[i]] = regioncolor[region[i]]

#start graph
G = nx.Graph()

#position of site nodes
def get_coordinates_in_circle(n):
    return_list = []
    for i in range(n):
        theta = float(i)/n*1.5*3.141592654
        x = np.cos(theta)
        y = np.sin(theta)
        x = x +1
        y = y +1   
        return_list.append((x,y))
    return return_list

#parameters
spread = 0.001 
jidder= 0.005 
textsz = 6
textalpha = 1
itt = 100 #itterations
szforsites = 800 
szforlevs = 40 
nmin = 8 #smallest node
mult = 30 #largest node

def normalizesize(dic,minn,mult):
    """
    normalized from 0 to 1
    """
    keys = list(dic.keys())
    vals = list(dic.values())        
    # Normalise to between 0 and 1 
    norm = (vals-np.nanmin(vals))/(np.nanmax(vals) - np.nanmin(vals))
    norm = [x * mult + 7 for x in norm] 
    normdic = dict(zip(keys,norm))
    return normdic

#size of each node
sizescore = {}
for i in range(len(program)):
    sizescore[program[i]] = siz[i]
sizescore = normalizesize(sizescore,nmin,mult)

#start graph
G = nx.Graph()
for i in range(len(program)): #UU_bio
    print(program[i])
    G.add_edge(program[i],'Agriculture',weight=Ag[i])
    G.add_edge(program[i],'Forestry',weight=For[i])    
    G.add_edge(program[i],'Food',weight=Foo[i])
        
#fixed nodes 
circular_positions = get_coordinates_in_circle(len(catlist))
fixed_nodes = [n for n in G.nodes() if n in catlist]
pos = {}
for i,p in enumerate(fixed_nodes):
    pos[p] = circular_positions[i]

#colors
color_map = []
for node in G:
    clr = catcolor[node]
    color_map.append(clr)      

#size
sz_map = []
for node in G:
    if node in catlist:
        sz_map.append(szforsites)
    else:
        depsize = sizescore[node]
        depsize = depsize * depsize/2 
        sz_map.append(depsize)    

#plot
pos = nx.spring_layout(G, pos=pos, iterations=itt, k=spread,threshold=jidder, fixed=fixed_nodes)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_color=color_map, node_shape='o', node_size=sz_map, alpha=0.5, edgecolors='black')

#Save the figure and show
plt.axis('off')
plt.tight_layout()
plt.savefig(resultsdir + PROJ + '_relation_plot.png', format='png', dpi=1200)
plt.show()
plt.close()    

# -*- coding: utf-8 -*-

"""
Create a PLS plot using ag, food and forestry as explanatory variables and the NextFood vocabulary as response variables. This is equivalent to the PLS Matlab code used in the actual study.
Confidence intervals for the Effects Plots can be identified using statsmodels OLS.
"""

#imports
import sys
from sys import exit
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_decomposition import PLSRegression

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
print(df)
 
#drop all rows without either an Ag food and forestry reference
agri = df['Agriculture'].tolist()
forest = df['Forestry'].tolist()
food = df['Food'].tolist()
tossinds = []
print('start',len(df))
for i in range(len(agri)):
    if agri[i] == 0 and forest[i] == 0 and food[i] == 0:
        tossinds.append(i)   
df.drop(tossinds, axis=0, inplace=True)
print('remaining',len(df))

#explanatory and response variables
colnames = ['Forestry','Agriculture','Food','Sustain','Innov','Network','StratMan','SysThink', 'TechKnow',	'Versatility','LifeLearn']
explnames = ['Forestry','Agriculture','Food']
respnames = ['Sustain','Innov','Network','StratMan','SysThink',	'TechKnow',	'Versatility','LifeLearn']
          
#all data
alldata = df[colnames]

#define predictor and response variables
X = alldata[explnames]
y = alldata[respnames]

#simple PLS
n_comp = X.shape[1]
pls = PLSRegression(n_components=n_comp, scale=True)
pls.fit(X, y)

#loadings and scores
t_pls = pls.x_scores_
w_pls = pls.x_weights_
p_pls = pls.x_loadings_
r_pls = pls.x_rotations_

u_pls = pls.y_scores_
c_pls = pls.y_weights_
q_pls = pls.y_loadings_
d_pls = pls.y_rotations_

#plot
plt.figure(figsize=(8,6))

#scaling 
wscale = 1
qscale = 4

#w, weighted P loadings (explanitory)
for i in range(len(w_pls)):
    #print(w_pls[i][0],w_pls[i][1]) #first two PCs
    plt.scatter(w_pls[i][0]*wscale,w_pls[i][1]*wscale, c='blue', s= 500, alpha = 0.8, marker='d')
    plt.text(w_pls[i][0]*wscale,w_pls[i][1]*wscale, explnames[i],fontsize=16)

#q, weighted C loadings (response)
for i in range(len(q_pls)):
    #print(q_pls[i][0],q_pls[i][1]) #first two PCs
    plt.scatter(q_pls[i][0]*qscale,q_pls[i][1]*qscale, c='yellow',s= 500, alpha = 0.8,marker='o')
    plt.text(q_pls[i][0]*qscale,q_pls[i][1]*qscale, respnames[i],fontsize=14)

#lines
plt.axhline(0, color='k', linestyle='-',linewidth=0.7)
plt.axvline(0, color='k', linestyle='-',linewidth=0.7)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PLS of GapAnalysis Data')

#save
label = resultsdir + PROJ + '_PLS_biplot.png'
plt.savefig(label, format='png', dpi=1200, bbox_inches='tight')
plt.show()
plt.close()

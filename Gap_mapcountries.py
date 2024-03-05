# -*- coding: utf-8 -*-

#imports
import os
import sys
from sys import exit
import pandas as pd
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs

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
country = df['Country'].tolist()
docsize = df['Docsize'].tolist()

#counts
countdict = defaultdict(list)
for i in range(len(df)):
    countdict[country[i]].append(docsize[i])

#sums
sumdict = {}
for k,v in countdict.items():
    sumdict[k] = sum(v)

def bettersize(cnt):
    bsize = cnt * 1.8
    #print(bsize)
    if bsize < 12:
        bsize = 12
    if bsize > 45:
        bsize = 45
    return bsize

#map region
extent = [-12, 30, 35, 69 ]

#boundries for plotting
latrng = (extent[0],extent[1])
lonrng = (extent[2],extent[3])

         
#test
for k,v in sumdict.items():
    print(k,v)

#normalize size
def normalizesize(dic,minn,mult):
    """
    normalized from 0 to 1
    """
    keys = list(dic.keys())
    vals = list(dic.values())        
    # Normalise to between 0 and 1 
    norm = (vals-np.nanmin(vals))/(np.nanmax(vals) - np.nanmin(vals))
    norm = [x * mult + 7 for x in norm]  #Edit here!
    normdic = dict(zip(keys,norm))
    return normdic

mult = 5
minn = 45
sumdict = normalizesize(sumdict,mult,minn)

#colors
colordict = {
'Austria':'olive',
'Belgium':'green',	
'Denmark':'lightblue',	
'Finland':'mediumpurple',	
'France':'red',	
'Greece':'grey',	
 'Hungary':'tan',	 
'Ireland':'yellow',	
'Italy':'blue',	
'Netherlands':'orange',	
'Poland':'cyan',	
'Portugal':'pink',
'Spain':'aquamarine',
'Sweden':'gold'
}

#symbols
symboldict = {
'Austria':'>',
'Belgium':'o',	
'Denmark':'',	
'Finland':'d',	
'France':'8',	
'Greece':'s',	
 'Hungary':'v',	 
'Ireland':'<',	
'Italy':'^',	
'Netherlands':'p',	
'Poland':'8',	
'Portugal':'o',
'Spain':'>',
'Sweden':'o'
}

#coordinates
geodict = {
'Austria':	[14.1264760996,	47.585494392],
'Belgium':	[4.6406511392,	50.6398157556],
'Denmark':	[10.0280099191,	55.9812529593],
'Finland':	[26.2746656042,	64.4988460349],
'France':	[3.1617294452,	47.1734401107],
'Greece':	[22.9555579369,	39.0746962307],
'Hungary':	[19.3955911607,	47.1627750614],
'Ireland':	[-8.1379356867,	53.175448704],
'Italy':	[12.0700133907,	42.796626414],
'Netherlands':[5.2814479301, 52.1007899002],
'Poland':	[19.3901283493,	52.1275956442],
'Portugal':	[-8.5010436127,	39.5955067145],
'Spain':	[-3.6475504732,	40.2444869811],
'Sweden':	[16.7455804869,	62.7796651931]
}

#prep data
Subjects = []
for k,v in sumdict.items():
    coord = geodict[k]
    lat = coord[0] 
    lon = coord[1]
    siz = bettersize(v)
    clr = colordict[k]
    mkr = symboldict[k]
    lat = float(lat)
    lon = float(lon)
    point = (k, lat, lon, siz, clr, mkr)
    Subjects.append(point)

#plot
#*****
def make_plot(projection_crs,extent,Subjects,stats2,PROJ):
    fig = plt.figure()
    rect = 0.2, 0.2, 1.6, 1.6
    ax = fig.add_axes(rect, projection=projection_crs)

    #display limits to include a set region of latitude * longitude.
    ax.set_extent(extent, crs=projection_crs)

    #bling
    ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=0.3)
    ax.coastlines(resolution='110m')
    ax.add_feature(cartopy.feature.OCEAN, facecolor='lightblue', alpha=0.1)
    used = []
    for item in Subjects:  #(subj, lat, lon, size, clr)

        #plot
        ax.plot(item[1], item[2], marker=item[5],
                markersize=item[3], markeredgewidth=2,
                markeredgecolor='black', markerfacecolor=item[4],
                linestyle='None', transform=projection_crs, alpha = 0.5, label = item[0] if item[0] not in used else "")
        
        #add dep to used list to avoid mult same name depts in legend
        used.append(item[0])
    
    #save
    savfig = resultsdir +  PROJ + '_geoplot.png'
    plt.savefig(savfig, bbox_inches='tight')
    plt.show()
    plt.close()

#plot
projection=ccrs.PlateCarree() #worldmap nice
make_plot(projection,extent,Subjects,resultsdir,PROJ)

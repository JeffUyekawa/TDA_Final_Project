#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ripser import ripser
import kmapper as km
from persim import plot_diagrams
#%%
'''
*NOTE* This code goes unused in our final paper, but it was our starting point in 
exploring the data with TDA. In this file we do various forms of exploration on 
our data in the similarity space with Rips Filtrations. Countries are compared
using various metrics and vaccination rate is studied by each parent location.
'''
merged_polio = pd.read_csv(r"C:\Users\jeffu\Downloads\scaled_polio.csv")

#List of all numeric valued columns
num_cols = ['Value','Latitude','Longitude','LifeExpect','GDP','MedianAge']
#Calculate Rips persistence on all data in R^6 and plot
x1 = merged_polio.loc[:,num_cols]
dgms1 = ripser(x1,maxdim=2)['dgms']
plot_diagrams(dgms1,show=True,title='Overall Similarity Score')

#Calculate persistence using each pair of columns including "Value"
for i in range(len(num_cols)-1):
    num_cols = ['Value','Latitude','Longitude','LifeExpect','GDP','MedianAge']
    dropped=num_cols.pop(i+1)
    cols = ['Value',dropped]
    if i==0:
        x1 = merged_polio.loc[:,['Value','Latitude','Longitude']]
        dgms2 = ripser(x1,maxdim=2)['dgms']
        plot_diagrams(dgms2,show=True,title=f'Geographic')
    elif i ==1:
        continue
    else:
        x1 = merged_polio.loc[:,cols]
        dgms2 = ripser(x1,maxdim=2)['dgms']
        plot_diagrams(dgms2,show=True,title=f'{cols}')
#%%     
# Look at geographic vs. non-geographic persistent homology
non_geog =  ['Value','LifeExpect','GDP','MedianAge']  
x1 = merged_polio.loc[:,non_geog]
dgms1 = ripser(x1,maxdim=2)['dgms']
plot_diagrams(dgms1,show=True,title='Non-Geographic')

x1 = merged_polio.loc[:,['Value','Latitude','Longitude']]
dgms1 = ripser(x1,maxdim=2)['dgms']
plot_diagrams(dgms1,show=True,title='Geographic')

#%%
#Plot non-geographic similarity score persistence diagrams by region
scaled_polio = merged_polio.copy()
no_lat_long = ['Value','LifeExpect','GDP','MedianAge']
region_dgms = {}
grouped = scaled_polio.groupby(by='ParentLocation')
for parent, group in grouped:
    x1 = group.loc[:,no_lat_long].values
    #Compute persistent homology and plot diagrams
    dgms = ripser (x1, maxdim=2)['dgms']
    plot_diagrams(dgms,show=True,title=f'{parent}')
    region_dgms[parent] = dgms
#%%
from persim import bottleneck
#Compare bottleneck distances pairwise by parent region
#Entries are lists of pairwise bottleneck distance for dimension [0,1,2]
parent_locs = set(scaled_polio.ParentLocation)
df = pd.DataFrame(index=parent_locs, columns=parent_locs)
for j in parent_locs:
    for k in parent_locs:
        if j==k:
            continue
        dists = []
        for i in range(3):
            dgms1 = region_dgms[j]
            dgms2 = region_dgms[k]
            if (dgms1[i].shape[0] == 0) or (dgms2[i].shape[0] == 0):
                dists.append(np.nan)
                continue
            d12,matching1 = bottleneck(dgms1[i],dgms2[i], matching = True)
            dists.append(d12)
        df.loc[j,k] = dists
df

# %%

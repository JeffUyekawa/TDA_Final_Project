# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import kmapper as km
from persim import plot_diagrams
import geopandas as gpd
from PIL import Image
from skimage.color import rgb2gray

'''
This file reads in the original WHO vaccination data and calculates persistent homology on
a sublevel set filtration of a world map colored by vaccination value. 
Each pixel in the image is given random noise so that creators of homology classes
can be identified and visualized in the original image.
'''
# Load the world map shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# Merge to make new gpd dataframe
#%%
#Read in original polio data, limit year to 2022
polio_df = pd.read_csv(r"C:\Users\jeffu\Downloads\polio_data.csv")
polio_df = polio_df[['ParentLocation','Location','Value','Period']]
polio_df = polio_df[polio_df.Period == 2022]

#Probably a better way to do this. Rename countries that don't match in the gpd table
#Come back if time allows
polio_df.Location[polio_df.Location=='Russian Federation']= 'Russia'
polio_df.Location[polio_df.Location == 'Bolivia (Plurinational State of)'] = 'Bolivia'
polio_df.Location[polio_df.Location=='South Sudan'] = 'S. Sudan'
polio_df.Location[polio_df.Location=='Democratic Republic of the Congo'] = 'Dem. Rep. Congo'
polio_df.Location[polio_df.Location=='Central African Republic'] = 'Central African Rep.'
polio_df.Location[polio_df.Location=='United Republic of Tanzania'] = 'Tanzania'
polio_df.Location[polio_df.Location=='Venezuela (Bolivarian Republic of)'] = 'Venezuela'

#Merge polio data with map data
merged_data = world.merge(polio_df, left_on='name', right_on='Location', how='left')
merged_data.dropna(inplace=True)

# Plot the world map with colors based on vaccination value
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
merged_data.plot(column='Value',  linewidth=0.8, ax=ax, edgecolor='0.8', legend=False, vmin=0)
ax.set_axis_off()

# Save the plot to an image file
plt.savefig('world_map_colored.png', bbox_inches='tight', pad_inches=0.1)
#Show plot of world map
plt.show()
#%%
# Read the saved colored image using PIL
world_map_colored = np.array(Image.open('world_map_colored.png'))

# Convert to grayscale using skimage
grayscale_matrix = rgb2gray(world_map_colored[:,:,:3])

# Display the grayscale matrix
plt.imshow(grayscale_matrix, cmap='gray', vmin=0, vmax=1)
plt.axis('off')
plt.show()
#%%
#Pad grayscale matrix to make it square for lower_star image
m = grayscale_matrix.shape[0]
n = grayscale_matrix.shape[1]
padded_gray = np.ones((n,n))
padded_gray[:m,:n+1] = grayscale_matrix
plt.imshow(padded_gray, cmap='gray')
plt.axis('off')
plt.show()
# %%
from scipy import ndimage
from ripser import ripser, lower_star_img

#Introduce random noise to each entry so that we have unique values
#To reference later when calculating persistent homology

gray_noise = padded_gray + 0.01 * np.random.randn(*padded_gray.shape)

#Round off values to help with matching later
rounded = np.around(gray_noise,decimals=5)
#Sublevel Set image filtration
dgm = lower_star_img(rounded)

plot_diagrams(dgm, lifetime=True)
plt.title('Lower Star Image Persistence Diagram')
plt.axhline(y=0.3, color = 'r', linestyle = 'dashed',label='Threshold')
plt.legend(bbox_to_anchor=(1.02, 0.1), loc='lower right', borderaxespad=0)
plt.show()
#%%
#Choose lifetime threshold to visualize points that showed longest persistence
thresh = 0.3
#Collect pixel values with persistence > thresh by birth time
representatives = []
for entry in dgm:
    if entry[1]-entry[0] >= thresh:
        representatives.append(entry[0])
rounded_reps = np.around(representatives, decimals = 5)
# %%
index_tuples = []
# Loop through each value in the list, add to list if in rounded reps
for index, value in np.ndenumerate(rounded):
    if value in rounded_reps:
        print(index,value)
        index_tuples.append(index)
        
#%%
#Turn tuples into x and y vectors for plotting
x,y = zip(*index_tuples)

#Plot original map with coordinates of representatives
plt.figure(figsize=(8, 5))
plt.imshow(world_map_colored, cmap='viridis', origin = 'upper')
plt.scatter(y,x, c='r')
plt.axis('off')
plt.colorbar(location='bottom')
plt.title('Representatives of $H_0$ Homology Classes')
plt.show()


# %%

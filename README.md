# TDA_Final_Project
This project was a presented as a final group project at Northern Arizona University in a class titled "Topological Data Analysis".

## **Data**

<img src="Figures and Images/Polio_table_ex.png?raw=true"/> 

In this project, we set out to explore polio vaccination data provided by the WHO. 
The original data was presented as vaccination values by year and country. We added data
for each country's GDP, life expectancy, median age, latitude, and longitude to create 
a "similarity space" upon which we would compute persistent homology. For the final 
scaled data set, we also scaled each column with min/max scaling and dropped all null values. 

In the "cleaned" folder, we utilized the scaled polio data for our alpha complex and rips filtration exploration, and we used the original polio dataset for the sublevel set filtration.
Various uncleaned datasets are included that were used in the data cleaning and preparation phase.
## **Code**
We have included the following code:

1. TDA_data_prep.py - In this code we clean, merge, and prepare our data for analysis.
2. Polio_Rips.py - This code was not used in the final presentation, however it was a crucial first step in exploring our data using TDA methods. In this file we do various forms of exploration on our data in the similarity space with Rips Filtrations. Countries are compared
using various metrics and vaccination rate is studied by each parent location.
3. Sublevel_map.py - In this code we create a sublevel set image filtration on a world map colored by vaccination value. This method allows for the creators of persistent homology classes to be traced back to points on the world map.
4. Alpha Complex.ipynb - This code explores the data set using alpha complexes.
5. Weighted Alpha Complex.ipynb - This code repeats exploration using weighted alpha complexes.
## **Writeup**
We have included our final research paper that outlines our methods and findings.

## **Presentation**
We included the slides for our final presentation.

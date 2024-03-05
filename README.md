# GapAnalysis

Programs used in the manuscript 'European Agrifood and Forestry Education for a Sustainable Future - Gap Analysis from an Informatics Approach' by Burleigh and Jönsson.

To begin you must identify universities with appropriate Masters programs using the European Tertiary Education Register database (ETER, www.eter-project.com). See manuscript for details.

#collect text from each of the university progam site(s) by running:
Gap_scrape.py

#Collect all the scraping results in a document called 'website_data.csv'.
#See our Zenodo Repository, DOI 10.5281/zenodo.6501547
    
#The following program uses 'website_data.csv' and counts the keywords in the programs using keywords.csv found at the Zenodo Repository, DOI 10.5281/zenodo.6501547:
Gap_collect_data.py

#Geolocate the countries and the total words collected from each country:
Gap_mapcountries.py

#Identify node and edge relations in terms of total words collected. This is used with Cytoscape (https://cytoscape.org/):
Gap_network.py

#create a relations plot showing the degree to which each program (colored by region) is associated with ag, food and forestry:
Gap_relations_plot.py

#for the remaining analyses, use relative values (keywords used in a given program relative to all words used in that program):
Gap_relative_values.py

#create a piechart of the various interdisciplinary combinations of ag, food and forestry scores for the programs:
Gap_piechart.py

#Create a PLS plot using ag, food and forestry as explanatory variables and NextFood vocabulary as response variables. This is equivalent to the PLS Matlab code used in the actual study.
Gap_PLS_biplot.py

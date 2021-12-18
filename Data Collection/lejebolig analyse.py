import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.close("all")

# lines-flag gør at filer der består af flere json objekter kan indlæses.
bolig = pd.read_json("../output.jl",lines="true")

bolig['Area'] = bolig['Area'].str.replace(' m', '')
bolig['Area'] = pd.to_numeric(bolig['Area'])
bolig['Price'] = bolig['Price'].str.replace(' Kr.', '').str.replace('.','')
bolig['Price'] = pd.to_numeric(bolig['Price'])

bolig['Price/Area'] = (bolig['Price']/bolig['Area'])

bolig.to_csv("lejebolig analyse.csv",index_label = "ID")
#bolig['price/area'].plot.hist()
#plt.show()

""" scatter plot via koordinater + punkterne er hyperlink som jeg bare kan trykke på
for at se i googlemaps.
"""
"""
bolig[['Y','X']] = bolig['koordinates'].str.split(',',expand = True)
bolig['X'] = pd.to_numeric(bolig['X'],errors='coerce')
bolig['Y'] = pd.to_numeric(bolig['Y'],errors='coerce')
f = plt.figure()
s = plt.scatter(x=bolig['X'],y=bolig['Y'], c=bolig['price/area'], cmap='bwr')
s.set_urls(bolig['googlemaps'])
f.savefig('scatter.svg')
#bolig.plot.scatter(x='X',y='Y', c='price/area', cmap='bwr')
#plt.show()
"""

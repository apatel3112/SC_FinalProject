#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:08:18 2019

@author: Anusha
"""

import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

# convert excel file to dataframe
parent_df = pd.read_csv('/Users/Anusha/Desktop/SC_FinalProject/movie_data.csv', sep=',', encoding ="ISO-8859-1")

# remove extra columns
# extra columns found on inspection
extra_columns = []
for i in range(138,28,-1):
    extra_columns.append(parent_df.columns[i])

# drop extra columns from movies_df
parent_df.drop(columns=extra_columns, axis=1, inplace=True)

#condense dataframe
parent_df.drop(columns=['awards', 'country', 'dvd', 'episode', 'metascore',
                        'production', 'rated', 'ratings', 'released', 'response',
                        'season', 'website', 'box_office','language','series_id','writer'], 
                axis = 1, inplace=True)

#remove duplicate fields
parent_df = parent_df.drop_duplicates()

# remove entries with all empty fields
parent_df.dropna(how='all', inplace = True)


#remove duplicate movies
parent_df = parent_df.drop_duplicates(subset='imdb_id', keep="first")


# Drop rows with null values for type
# Drop shows with values other than movie and tv show in type field
parent_df.dropna(subset=['type'], inplace=True)


print(parent_df.shape)
parent_df = parent_df[parent_df.type != 'game']
parent_df = parent_df[parent_df.type != 'episode']

# Split df into movies and series
movies_df = parent_df[parent_df['type'] == 'movie']
print(movies_df.shape)
tv_df = parent_df[(parent_df['type'] == 'series')]
print(tv_df.shape)

tv_csv = tv_df.to_csv(r'/Users/Anusha/Desktop/SC_FinalProject/tv_data.csv',mode='a',header=False,index=None,encoding = "utf-8")
movies_csv = movies_df.to_csv(r'/Users/Anusha/Desktop/SC_FinalProject/only_movie_data.csv',mode='a',header=False,index=None,encoding = "utf-8")

    




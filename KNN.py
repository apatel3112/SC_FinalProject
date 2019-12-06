#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:32:31 2019

@author: Anusha
"""

def generate_knn_tv(tv_df):
    # Process tv df
    tv_df["year"] = tv_df['year'].str.slice(start=0,stop=4,step=1) 
    tv_df['year'] = tv_df['year'].astype(float) 
    tv_df[tv_df["year"] >= 1950]
    
    tv_df.reset_index(inplace=True)
    # Fill null ratings with mean
    tv_df['imdb_rating'].fillna(tv_df['imdb_rating'].median(), inplace=True)
    tv_df['imdb_rating'] = tv_df['imdb_rating'].astype(float)
    print(tv_df.shape)
    # Fill null runtime with mean
    tv_df["runtime"] = tv_df['runtime'].str.replace(" min","")
    tv_df["runtime"] = tv_df['runtime'].str.replace(" h","60")
    tv_df["runtime"] = tv_df['runtime'].str.replace(" ","")
    tv_df["runtime"] = tv_df['runtime'].str.replace(",","")
    tv_df['runtime'].fillna(tv_df['runtime'].median(), inplace=True)
    print(tv_df.shape)
    
    # Factor in popularity
    tv_df["imdb_votes"] = tv_df['imdb_votes'].str.replace(",","")
    tv_df['imdb_votes'].fillna(tv_df['imdb_votes'].median(), inplace=True)
    tv_df['imdb_votes'] = tv_df['imdb_votes'].astype(float)
    
    ## Fill null seasons with mean
    tv_df['total_seasons'].fillna(tv_df['total_seasons'].median(), inplace=True)
    tv_df['total_seasons'] = tv_df['total_seasons'].astype(float)
    print(tv_df.shape)
    
    knn_matrix = pd.concat([tv_df['genre'].str.get_dummies(sep=", "),
                tv_df['imdb_rating'],tv_df['total_seasons'],tv_df['imdb_votes'],
                tv_df['year']],axis=1)
    
    min_max_scaler = MinMaxScaler()
    knn_matrix = min_max_scaler.fit_transform(knn_matrix)
    np.round(knn_matrix,2)
    
    return knn_matrix

def generate_knn_tv(movies_df):
    # Process tv df
    movies_df.dropna(subset=['year'])

    
    movies_df.reset_index(inplace=True)
    # Fill null ratings with mean
    movies_df['imdb_rating'].fillna(movies_df['imdb_rating'].median(), inplace=True)
    movies_df['imdb_rating'] = movies_df['imdb_rating'].astype(float)
    print(movies_df.shape)
    # Fill null runtime with mean
    movies_df["runtime"] = movies_df['runtime'].str.replace(" min","")
    movies_df["runtime"] = movies_df['runtime'].str.replace(" h","60")
    movies_df["runtime"] = movies_df['runtime'].str.replace(" ","")
    movies_df["runtime"] = movies_df['runtime'].str.replace(",","")
    movies_df['runtime'].fillna(movies_df['runtime'].median(), inplace=True)
    print(movies_df.shape)
    
    # Factor in popularity
    movies_df["imdb_votes"] = movies_df['imdb_votes'].str.replace(",","")
    movies_df['imdb_votes'].fillna(movies_df['imdb_votes'].median(), inplace=True)
    movies_df['imdb_votes'] = movies_df['imdb_votes'].astype(float)
    
    
    knn_matrix = pd.concat([movies_df['genre'].str.get_dummies(sep=", "),
                movies_df['imdb_rating'],movies_df['imdb_votes'],
                movies_df['year']],axis=1)
    
    min_max_scaler = MinMaxScaler()
    knn_matrix = min_max_scaler.fit_transform(knn_matrix)
    np.round(knn_matrix,2)
    
    return knn_matrix

def knn(knn_matrix):
    nn = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(knn_matrix)
    distances, indices = nn.kneighbors(knn_matrix)
    print(distances,indices)

def get_index_from_name(name):
    try:
        return movies_df[movies_df["title"]==name].index.tolist()[0]
    except IndexError:
        print('Show does not exist in our database, try again!')
        return None


all_tv_names = list(movies_df.title.values)

def print_similar_shows(query=None):
    found_id = get_index_from_name(query)
    if found_id is not None:
        for id in indices[found_id][1:]:
            print(movies_df.ix[id])
            
if __name__=="__main__":    
    print_similar_shows(query="Titanic")
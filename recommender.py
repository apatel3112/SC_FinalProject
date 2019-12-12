#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:32:31 2019

@author: Anusha
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import Movie_GUI
import tkinter as tk
from tkinter import font as tkfont


def movies_df_gen(file):
    """
    This function generates a tv and movie dataframe from an input media file

    INPUTS:
        file = data file

    OUTPUTS:
        movie_df = movie dataframe
        tv_df = tv dataframe

    """

    # convert excel file to dataframe

    parent_df = pd.read_csv(file, sep=',',
                            encoding='ISO-8859-1',error_bad_lines=False)

    # remove extra columns
    # extra columns found on inspection

    extra_columns = []
    for i in range(138, 28, -1):
        extra_columns.append(parent_df.columns[i])

    # drop extra columns from movies_df

    parent_df.drop(columns=extra_columns, axis=1, inplace=True)

    # condense dataframe

    parent_df.drop(columns=[
        'awards',
        'dvd',
        'episode',
        'metascore',
        'production',
        'rated',
        'ratings',
        'released',
        'response',
        'season',
        'website',
        'box_office',
        'language',
        'series_id',
        'writer',
        ], axis=1, inplace=True)

    # remove duplicate fields

    parent_df = parent_df.drop_duplicates()
    parent_df.reset_index(drop=True, inplace=True)

    # remove entries with all empty fields

    parent_df.dropna(how='all', inplace=True)
    parent_df.reset_index(drop=True, inplace=True)

    # remove duplicate movies

    parent_df = parent_df.drop_duplicates(subset='imdb_id', keep='first')
    parent_df.reset_index(drop=True, inplace=True)

    # keep only movies in the US

    parent_df = parent_df[parent_df.country == 'USA']

    # drop adult and short film categories

    to_drop = ['Adult']
    parent_df = parent_df.query('genre not in @to_drop')
    to_drop = ['Short']
    parent_df = parent_df.query('genre not in @to_drop')

    # Drop rows with null values for type
    # Drop shows with values other than movie and tv show in type field

    parent_df.dropna(subset=['type'], inplace=True)
    parent_df = parent_df.reset_index(drop=True)
    parent_df = parent_df[parent_df.type != 'game']
    parent_df = parent_df[parent_df.type != 'episode']

    # Split df into movies and series

    movies_df = parent_df[parent_df['type'] == 'movie']
    tv_df = parent_df[parent_df['type'] == 'series']

    return (movies_df, tv_df)


def data_set(movies_df, genre_indices, actor, director, start_year, end_year,
             rating_min, rating_max, max_runtime):

    """
    This processes the dataset and tailors it based on search parameters

    INPUTS:
        movies_df = movies dataframe
        genre_indices = genre
        actor, director
        start_year, end_year
        rating_min, rating_max
        max_runtime = upper time limit for each episode

    OUTPUTS:
        processed movies_df

    """
    # Process tv df
    # Sort first by actor

    if len(actor) != 0:
        movies_df['actors'].fillna('', inplace=True)
        actor = actor[0]
        movies_df = movies_df[movies_df['actors'].str.contains(actor)]
    elif len(director) != 0:

        # Sort by director

        movies_df['director'].fillna('', inplace=True)
        director = director[0]
        movies_df = movies_df[movies_df['director'].str.contains(director)]
    elif len(genre_indices) != 0:

        # Sort by genre

        to_keep = genre_indices
        for i in range(len(to_keep)):
            movies_df['genre'].fillna('', inplace=True)
            movies_df = movies_df[movies_df['genre'].str.contains(to_keep[i])]

    # Format year times to yield only numeric values
    movies_df = movies_df.reset_index()
    movies_df['year'] = movies_df['year'].astype(str)
    movies_df['year'] = movies_df['year'].str.slice(start=0, stop=4, step=1)
    movies_df['year'] = movies_df['year'].astype(float)
    movies_df.dropna(subset=['year'], inplace=True)
    movies_df.reset_index(drop=True, inplace=True)

    # Condense dataset based on start and end year

    movies_df = movies_df[(movies_df.year > start_year)
                          & (movies_df.year < end_year)]

    # Fill null ratings with mean
    movies_df['imdb_rating'].fillna(movies_df['imdb_rating'].median(),
                                    inplace=True)
    movies_df['imdb_rating'] = movies_df['imdb_rating'].astype(float)
    movies_df = movies_df[(movies_df.imdb_rating > rating_min)
                          & (movies_df.imdb_rating < rating_max)]

    # Fill null runtime with mean

    movies_df['runtime'] = movies_df['runtime'].str.replace(' min', '')
    movies_df['runtime'] = movies_df['runtime'].str.replace(',', '')

    # Rare runtime values are in terms of H:MM format. Remove these
    to_drop = ['h']
    movies_df = movies_df.query('runtime not in @to_drop')
    movies_df['runtime'].fillna(movies_df['runtime'].median(),
                                inplace=True)
    movies_df['runtime'] = movies_df['runtime'].astype(int)
    movies_df = movies_df[movies_df.runtime < max_runtime]

    # Fill popularity values with mean

    movies_df['imdb_votes'] = movies_df['imdb_votes'].str.replace(',', '')
    movies_df['imdb_votes'].fillna(movies_df['imdb_votes'].median(),
                                   inplace=True)
    movies_df['imdb_votes'] = movies_df['imdb_votes'].astype(float)

    movies_df = movies_df.reset_index()

    return movies_df


def knn_algorithm(movies_df):
    """
    This function finds 10 most similar movies to a given input

    INPUTS:
        movies_df = movies dataframe


    OUTPUTS:
        distance = distance from input movie to any other movie in processed df
        indices = index of each movie that has a corresponding distance value

    """

    # Generate knn matrix from movies df

    knn_matrix = pd.concat([movies_df['genre'].str.get_dummies(sep=', '),
                            movies_df['imdb_rating'],
                            movies_df['imdb_votes']], axis=1)

    print('SIZE',knn_matrix.size)
    # Scale values to avoid letting large values dominate results

    min_max_scaler = MinMaxScaler()
    knn_matrix = min_max_scaler.fit_transform(knn_matrix)
    np.round(knn_matrix, 2)

    # Find neighbours, distances and indices

    nn = NearestNeighbors(n_neighbors=10, algorithm='ball_tree'
                          ).fit(knn_matrix)
    (distances, indices) = nn.kneighbors(knn_matrix)

#

    return (distances, indices)


def outputs():
    """
    This function gets GUI output in form og a vector

    INPUTS:
        None

    OUTPUTS:
        media_indices,
        genre_indices,
        year_max, year_min,
        movie_name,
        actor, director,
        rating_max, rating_min,
        time_indices,

    """
    gui_output = Movie_GUI.GUI_Movie()
    print(gui_output)

    # Available genres

    genres = [
        'Documentary',
        'Short',
        'Animation',
        'Comedy',
        'Romance',
        'Sport',
        'Action',
        'News',
        'Drama',
        'Fantasy',
        'Horror',
        'Music',
        'War',
        'Crime',
        'Western',
        'Sci-Fi',
        'Family',
        'Adventure',
        'History',
        'Biography',
        'Mystery',
        'Thriller',
        'Musical',
        'Film Noir',
        'Game Show',
        'Talk Show',
        'Reality TV',
        'Adult',
        ]

    # Available media

    media = ['movie', 'tv']

    # Available time scales

    time_scale = [60, 120, 180, 1000]

    # Extract media types
    media_type = gui_output[0]

    try:    
        media_indices = [media[i] for (i, x) in enumerate(media_type) if x
                     == 1]
    except IndexError:
        media_indices = ['movie']

    # Extract genre types
    genre_type = gui_output[1]
    genre_indices = [genres[i] for (i, x) in enumerate(genre_type) if x
                     == 1]

    # Extract max and min year
    if len(gui_output[5]) == 2:
        year_min = float(gui_output[5][0])
        year_max = float(gui_output[5][1])
    else:
        year_max = 2018
        year_min = 1970

    # Extract movie name
    movie_name = gui_output[2]

    # Extract actor name
    actor = gui_output[3]

    # Extract director name
    director = gui_output[4]

    # Extract max and min rating
    gui_output_6 = np.array(gui_output[6])
    if np.count_nonzero(gui_output_6) > 0:
        rating_min = gui_output_6[0]
        rating_max = gui_output_6[1]
    else:
        rating_min = 1
        rating_max = 10

    # Extract time limit
    gui_output_7 = np.array(gui_output[7])
    if np.count_nonzero(gui_output_7) > 0:
        time = gui_output_7
        time_indices = [time_scale[i] for (i, x) in enumerate(time)
                        if x == 1]
    else:
        time_indices = [180]

    # all_tv_names = list(movies_df.title.values)

    print(
        media_indices,
        genre_indices,
        year_max,
        year_min,
        movie_name,
        actor,
        director,
        rating_max,
        rating_min,
        time_indices,
        )
    
    return (
        media_indices,
        genre_indices,
        year_max,
        year_min,
        movie_name,
        actor,
        director,
        rating_max,
        rating_min,
        time_indices,
        )


def get_index_of_movie(name, movies_df):
    """
    This function gets index of movie

    INPUTS:
        name = movie name
        movies_df = either movie or tv dataframe

    OUTPUTS:
        index of movie if present in processed dataframe
        None if other parameters dont match upto title

    """
    try:
        return movies_df[movies_df['title'] == name].index.tolist()[0]
    except IndexError:
        print('Title does not exist in our database, try again!',
              'Check parameters.')
        return None


def print_similar_shows(name, indices, movies_df):
    """
    This function searches for index of movie in KNN matrix and yields 10
    neighbours closest to it

    INPUTS:
        name = movie name
        indices = index of title from each other movie in dataframe
        movies_df = movie dataframe

    OUTPUTS:
        index of movie if present in processed dataframe
        None if other parameters dont match upto title

    """
    output = []
    found_id = get_index_of_movie(name, movies_df)
    if found_id is not None:
        for id in (indices[found_id])[1:]:
            output.append(movies_df.ix[id]['title'])
            print(movies_df.ix[id]['title'])

    return output


def knn_random_search(movies_df, tv_df, media_indices, genre_indices, year_max,
                      year_min, movie_name, actor, director, rating_max,
                      rating_min, time_indices):

    """
    This function searches for index of movie in KNN matrix and yields 10
    neighbours closest to it. If no movie title is provided, it searches
    dataframe based on input parameters and sorts output based on most
    imdb votes

    INPUTS:
        movies_df, tv_df,
        media_indices,
        genre_indices, year_max,
        year_min, movie_name,
        actor, director,
        rating_max, rating_min,
        time_indice

    OUTPUTS:
        list of 10 similar titles

    """
    max_runtime = time_indices[0]
    if media_indices[0] == 'movie':
        chosen_df = data_set(
            movies_df,
            genre_indices,
            actor,
            director,
            year_min,
            year_max,
            rating_min,
            rating_max,
            max_runtime,
            )
    else:

        chosen_df = data_set(
            tv_df,
            genre_indices,
            actor,
            director,
            year_min,
            year_max,
            rating_min,
            rating_max,
            max_runtime,
            )

    if len(movie_name) != 0:
        movie_name = movie_name[0]
        (distances, indices) = knn_algorithm(chosen_df)
        # found_id = get_index_of_movie(movie_name, chosen_df)
        shows = print_similar_shows(movie_name, indices, chosen_df)

    else:
        print(chosen_df)
        chosen_df.sort_values(by=['imdb_votes'], inplace=True)
        suggestions = chosen_df.tail(10)
        shows = suggestions.title

    return shows, chosen_df

def output_rec(shows):
    """
    This function displays shows the output page with all 10 movies

    INPUTS:
        shows - list of shows

    OUTPUTS:
        output page

    """
    shows_list = [] 
    
    for i in range(len(shows)):
        shows_list.append(shows[i])

    output = tk.Tk(className="Recommendations")
    output.geometry("800x800")

    font = tkfont.Font(size=25)
    font.configure(underline=True)

    label = tk.Label(output, text="Movie/TV Recommendations!", font=font).grid(row=0, sticky='nsew')
    for i in range(len(shows_list)):
        m = tk.Label(output, text=shows_list[i], font=15)
        m.grid(row=i+1, sticky='nsew')

    output.grid_columnconfigure(0, weight=1)
    output.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

    output.mainloop()

if __name__ == '__main__':

    file = 'movie_data.csv'
    movies_df, tv_df = movies_df_gen(file)

    (
        media_indices,
        genre_indices,
        year_max,
        year_min,
        movie_name,
        actor,
        director,
        rating_max,
        rating_min,
        time_indices,
        ) = outputs()

    shows, chosen_df = knn_random_search(
        movies_df,
        tv_df,
        media_indices,
        genre_indices,
        year_max,
        year_min,
        movie_name,
        actor,
        director,
        rating_max,
        rating_min,
        time_indices,
        )


    output_rec(shows)


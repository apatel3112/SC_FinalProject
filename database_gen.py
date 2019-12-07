#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 23:32:40 2019

@author: Anusha
"""
import pandas as pd
import omdb
from omdb import OMDBClient
import requests
import time


def media_database_builder(file, API_KEY, start_index, stop_index):
    """
    This function used requests imdb movies and tv information using the omdb
    module and appends them to a dataframe

    INPUTS:
        file = file containing imdb keys
        API Key
        Start index and Stop index for imdb keys

    OUTPUTS:
        Excel csv spreadsheet containing information

    """
    # convert unique imdb title to dataframe
    col_name = ['imdbid']
    imdb_id = pd.read_csv(file, sep='\t', names=col_name)

    omdb.set_default('apikey', API_KEY)
    client = OMDBClient(apikey=API_KEY)

    rows_list = []
    for i in range(int(start_index), int(stop_index)):
        print(i)
        movie_ID = imdb_id.iloc[i, 0]
        try:
            movie_dict = omdb.get(imdbid=movie_ID)
            rows_list.append(movie_dict)
            # Generates HTTP Error
            r = omdb.request(imdbid=movie_ID)
        # Value error - imdb ID yeilds dictionary that is empty
        # HTTPError (522) - Exceeded requests per unit time
        # Timeout - Overrules default timeout value
        except (ValueError, requests.HTTPError, requests.ReadTimeout) as err:
            if err == ValueError:
                continue
            else:
                i = i - 1
                time.sleep(2.0)
                print('Error has occured')
                print('Retry request in 2.0 seconds')
                continue

    media_df = pd.DataFrame(rows_list)
    media_csv = media_df.to_csv(r'media_data.csv', mode='a', header=False,
                                index=None, encoding="utf-8")

    return media_csv


if __name__ == "__main__":
    file = 'export_data.csv'
    API_KEY = input('Enter API Key:')
    start_index = input('Enter start index:')
    stop_index = input('Enter stop index:')
    media_csv = media_database_builder(file, API_KEY, start_index, stop_index)
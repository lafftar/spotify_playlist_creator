import pandas as pd
from spotify_playlist_creator import db_interface
import json
from sqlalchemy import create_engine
from re import sub

def grab_data_from_table(artist_name):
    '''
    Sorts through the raw API calls from the spotify db, converts from str artist_name.replace(' ', '_')to json, searches in the dict for the values
    we need, assigns appropriate keys to the values.
    :return: Pandas Data Frame Object with the info we need.
    '''
    df = pd.read_sql_query(f"SELECT * FROM a{sub('[- ]','_',artist_name)}_Songs;", db_interface.create_connection())
    data_list = [{'Name': entry['name'], 'Popularity': entry['popularity'], 'URI': entry['uri']}
     for each_row in df['api_data']
     for entry in json.loads(each_row)['items']
     for each_artists in entry['album']['artists']
     if each_artists['name'].lower() == f'{artist_name}'.lower()]
    data_frame = pd.DataFrame(data_list,columns=['Name', 'Popularity', 'URI'])
    return data_frame

def sort_and_dump_data_to_db(data_frame, artist_name):
    '''
    Sort by Popularity, grab the first 50, write this info to a table, use sql_alchemy to write to sql quickly, return
    a data frame of the table we just created, to confirm it.
    :param data_frame: Input is the data_frame from the grab_data_from_table() function.
    :return: Returns a dataframe of the new table we just created.
    '''
    sorted_data_frame = data_frame
    sorted_data_frame.sort_values(by=['Popularity'], inplace=True, ascending=False)
    sorted_data_frame.drop_duplicates(subset='Name', inplace=True)
    sorted_data_frame = sorted_data_frame[:50]

    db_connection = create_engine('sqlite:///api_calls_and_sorted_data.db')
    sorted_data_frame.to_sql(f"a{sub('[- ]','_',artist_name)}_Top_Songs",if_exists='replace',method='multi',con=db_connection)
    return pd.read_sql_table(table_name=f"a{sub('[- ]','_',artist_name)}_Top_Songs", con=db_connection)
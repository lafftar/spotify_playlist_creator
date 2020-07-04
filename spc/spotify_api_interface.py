from spotipy import Spotify, util
import json
import db_interface
from datetime import datetime, timezone
from re import sub
from spotipy.exceptions import SpotifyException


def spotify_obj():
    client_id = 'e1e98182af4a4ca881f61231e4b0787b'
    client_secret = '72d28146bcc3430fae89d259acf03d23'
    redirect_uri = 'http://localhost:8080'
    scope = 'playlist-modify-public'
    username = 'bdfgc5lgagjyvwig35m3uy834'
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    sp = Spotify(auth=token)
    return sp


def grab_all_songs(artist_name):
    """
    I thought to grab the artist ID then search through the artist_albums endpoint, but that doesn't return
    popularity.
    :param artist_name:
    """
    spotify_api = spotify_obj()
    page = spotify_api.search(q=f'artist:"{artist_name}"', type="track", limit=50)['tracks']
    data = []
    while True:
        date_time = str(datetime.now(timezone.utc).astimezone())
        data.append([json.dumps(page), date_time])
        try:
            page = spotify_api.next(page)['tracks']
        except (TypeError, SpotifyException):
            '''
            If the next() function fails, it returns TypeError, it means it can't find the 'next' key.
            SpotifyException happens when there's a next page, but it returns a 404.
            '''
            break
    create_new_table_in_db(artist_name)
    db_interface.create_api_data(sub('[- ]', '_', artist_name), data)


def find_playlist_id_if_exists(playlist_name):
    playlist_page = spotify_obj().current_user_playlists(limit=50)
    playlist_ids = [each_item['id']
                    for each_item in playlist_page['items']
                    if each_item['name'] == playlist_name]
    return playlist_ids


def delete_playlists(playlist_ids):
    """
    No way to delete playlists with the Spotify API outright. Best way to remove them from the profile is to simply
    unfollow them.
    :param playlist_ids: A list of playlist IDs
    :return: Returns the current user playlists if you would like to confirm.
    """
    spotify_api = spotify_obj()
    for each_playlist_id in playlist_ids:
        spotify_api.user_playlist_unfollow('bdfgc5lgagjyvwig35m3uy834', each_playlist_id)
    return spotify_api.current_user_playlists(limit=50)


def add_tracks_to_playlist(artist_name):
    uris_list = [item[0]
                 for item in db_interface.select_data_from_table(sub('[- ]', '_', artist_name), 'URI', 'Top_Songs')]
    while True:
        playlist_id = find_playlist_id_if_exists(f'Top 50 {artist_name} Songs Right Now')
        if len(playlist_id) == 0:
            try:
                spotify_obj().user_playlist_create('bdfgc5lgagjyvwig35m3uy834',
                                                   f"Top 50 {artist_name} Songs Right Now",
                                                   public=True,
                                                   description=
                                                   f"The most popular songs by {artist_name}! "
                                                   f"Updated Daily.")
            except SpotifyException:
                # Sometimes the fx returns a server error here, want the program to try again.
                pass
            continue
        break
    spotify_obj().user_playlist_replace_tracks('bdfgc5lgagjyvwig35m3uy834',
                                               playlist_id=playlist_id[0], tracks=uris_list)


# SQL Interactions
def create_new_table_in_db(artist_name):
    """
    This simply creates a new table in the db for our artist. Ensures there are no conflicts.
    :param artist_name:
    :return:
    """
    db_interface.delete_table(sub('[- ]', '_', artist_name))  # Replacing table if it exists
    db_interface.create_table(sub('[- ]', '_', artist_name))

import spotify_api_interface, sorter
from time import time
from datetime import datetime


def create_top_50(artist_name):
    t1 = time()
    spotify_api_interface.grab_all_songs(artist_name)
    data_frame = sorter.grab_data_from_table(artist_name)
    sorter.sort_and_dump_data_to_db(data_frame, artist_name)
    spotify_api_interface.add_tracks_to_playlist(artist_name)
    t2 = time()
    print(f'{artist_name} took {t2 - t1} seconds')

# TODO: let this load from db file, we'll save user additions here as well.
if __name__ == '__main__':
    list_of_artist_names = ['Taylor Swift',
                            'Ariana Grande',
                            'Shawn Mendes',
                            'Maroon 5',
                            'Adele',
                            'Justin Bieber',
                            'Ed Sheeran',
                            'Justin Timberlake',
                            'Charlie Puth',
                            'John Mayer',
                            'Lorde',
                            'Fifth Harmony',
                            'Lana Del Rey',
                            'James Arthur',
                            'Zara Larsson',
                            'Pentatonix',
                            'Kendrick Lamar',
                            'Post Malone',
                            'Drake',
                            'Kanye West',
                            'Eminem',
                            'Future',
                            '50 Cent',
                            'Lil Wayne',
                            'Lil Baby',
                            'DaBaby',
                            'Macklemore',
                            'Jay-Z',
                            'Bruno Mars',
                            'Beyoncé',
                            'Enrique Iglesias',
                            'Stevie Wonder',
                            'John Legend',
                            'Alicia Keys',
                            'Usher',
                            'Rihanna',
                            'Kygo',
                            'The Chainsmokers',
                            'Avicii',
                            'Marshmello',
                            'Calvin Harris',
                            'Martin Garrix',
                            'Coldplay',
                            'Elton John',
                            'OneRepublic',
                            'The Script',
                            'Jason Mraz',
                            'Frank Sinatra',
                            'Michael Bublé',
                            'Norah Jones']

    t1 = time()
    for artist in list_of_artist_names:
        create_top_50(artist)
    t2 = time()

    print('-----------------------------------------------------------------')
    print(f'Only took {t2 - t1} seconds!')
    print('-----------------------------------------------------------------')
    with open("logs.txt", "a") as logs:
        logs.write(f"Last run on {datetime.now().isoformat(timespec='minutes')} "
                   f"- Took {t2-t1} seconds")

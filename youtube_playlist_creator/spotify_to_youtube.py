from spc import spotify_api_interface as spotify_api
from bs4 import BeautifulSoup as bs
import json
from operator import itemgetter
from fuzzywuzzy import fuzz
from sqlalchemy import create_engine
from db_interface import create_connection_yt
import pandas as pd
from time import time
from aiohttp import ClientSession
import asyncio

spotfy_obj = spotify_api.spotify_obj()
'''
Ideally should just pass playlist url or something here, thinking will have a search 
playlist/album feature on the site, people can just search what they want and have a 
youtube playlist made for them.

Pass playlist ID here, get a list of songs as strings
Search the strings on youtube, grab the first result, it's likely most relevant, then add the 
result to a new playlist on my page.
Need to check if my page already has the playlist in the exact same order.
'''


# prints playlist id's currently in Best Playlist id's
# print(json.dumps(spotfy_obj.current_user_playlists(), indent=4, skipkeys=True))
# for playlist in spotfy_obj.current_user_playlists()["items"]:
#     print(playlist["id"])


def return_songs_from_playlist(playlist_id):
    song_names = []
    for song in spotfy_obj.playlist_tracks(playlist_id=playlist_id)["items"]:
        song_name = song["track"]["name"]
        song_name += f'+{song["track"]["artists"][0]["name"]}'
        song_names.append(song_name)
    return song_names


def return_songs_from_album(album_id):
    # add on all artists featured on the track for better searching
    # might be a good idea to do the same for playlist, maybe even have a singular
    # method for both
    album_tracks = []
    for album_track in spotfy_obj.album(album_id)["tracks"]["items"]:
        album_track_name = spotfy_obj.album(album_id)["name"]
        album_track_name += f'+{album_track["name"]}'
        for artist in album_track["artists"]:
            album_track_name += f'+{artist["name"]}'
        album_tracks.append(album_track_name)
    return album_tracks


async def find_song_on_youtube(song_name, session):
    song_name_query = song_name.replace(" ", "+")
    async with session.request(method='GET', url=f"https://www.youtube.com/results"
                                                 f"?search_query={song_name_query}",
                               timeout=5) as page:
        page = await page.read()
    return await sort_return_final_result(page, song_name)


async def sort_return_final_result(page, song_name):
    page = bs(page, 'lxml')
    # not sorting these because unsure how to check if it's the actual artist page
    # might be a good idea to check the channel name vs artist name, although sometimes
    # the music video is not on the artist's channel, it's on WSHH or a label or some other
    # distro

    # really just need the url of the video, might be a good idea to remove the other checks
    # for speed increase
    # all this transformation is to grab the area of html where the result json is
    # could break very easily
    page = str(page.find_all("script")[-3]).split("=", 1)[1].strip()[:-1].split("\n")[0][:-1]
    page = json.loads(page)
    # drilling down to where the video contents are
    full_page = (page["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]
    ["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"])
    # sometimes the video is not in the first position, this should drill down until it finds
    # the first video item, should be in the videoRenderer key
    first_two_results = []
    for item in full_page:
        if len(first_two_results) >= 2:
            break
        try:
            page = item["videoRenderer"]
            first_two_results.append(await parse_video_info(page))
        except KeyError:
            continue
    '''
    Sort by views first, then grab the highest viewed video by the official artist if it's 
    available
    '''
    first_two_results.sort(key=itemgetter("Views"), reverse=True)
    first_two_results.sort(key=itemgetter("Official Artist"), reverse=True)
    final_result = {}
    for item in first_two_results:
        if fuzz.partial_ratio(item["Name"], song_name.split('+')[0]) > 50:
            final_result = item
            break
    # print(final_result)
    return final_result


async def parse_video_info(page):
    # name of video
    name = page["title"]["runs"][0]["text"]
    # url of video
    url = page["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
    url = f'https://youtube.com{url}'
    # views
    views = int(page["viewCountText"]["simpleText"].split()[0].replace(",", ""))
    # official artist check
    try:
        official_artist = page["ownerBadges"][0]["metadataBadgeRenderer"]["tooltip"]
        if official_artist != "Official Artist Channel":
            raise KeyError
        official_artist = True
    except KeyError:
        official_artist = False
    return {
        "Name": name,  # encoding issues here might be a problem later
        "Url": url,
        "Views": views,
        "Official Artist": official_artist
    }


def dump_playlist_to_db(playlist, playlist_name):
    # creates db if it doesn't exist already
    playlist = pd.DataFrame(playlist, columns=["Name", "Url", "Views", "Official Artist"])
    db_connection = create_engine('sqlite:///youtube_playlists.db')
    playlist.to_sql(f"{playlist_name} - Music Videos - From Spotify", if_exists='replace',
                    method='multi', con=db_connection)
    pass


async def get_song_urls(playlist_or_album, resource_id):
    song_list = []  # to get rid of pycharm error
    rsrc_name = ""
    if playlist_or_album == "Playlist":  # rsrc id could be playlist or album id
        song_list = return_songs_from_playlist(resource_id)
        rsrc_name = spotfy_obj.playlist(resource_id)['name']
    elif playlist_or_album == "Album":
        song_list = return_songs_from_album(resource_id)
        rsrc = spotfy_obj.album(resource_id)
        rsrc_name = rsrc['name']
        rsrc_name += f" - by {rsrc['artists'][0]['name']}"
    print("Collected Songs from Playlist")
    t1 = time()
    async with ClientSession() as session:
        playlist = await asyncio.gather(*[find_song_on_youtube(song, session)
                                          for song in song_list])
    t2 = time()
    print(t2 - t1)
    dump_playlist_to_db(playlist, rsrc_name)
    for song, ytvid in zip(song_list, playlist):
        try:
            print(f"{song.split('+')[0]} | {ytvid['Name']} | {ytvid['Url']}")
        except KeyError:
            print(song)


def add_songs_to_yt_playlist(rsrc_name):
    # TODO: build yt automator here, js extension.
    # TODO:check if this fx works
    df = pd.read_sql_query(f"SELECT * FROM [{rsrc_name} "
                           f"- Music Videos - From Spotify]", create_connection_yt())
    for url in df['Url']:
        print(url)


# asyncio.run(get_song_urls("Album", "6a4HHZe13SySfC50BGy8Hm"))
# sync run takes 40s for just 13 songs. properly made async takes less than 1 second :')
# asyncio.run(get_song_urls("Playlist", "5ANamkjBXMJ2PqdpL56Bqp"))
# add_songs_to_yt_playlist("Mastermind (Deluxe) - by Rick Ross")

from spc import spotify_api_interface as spotify_api
from requests import get
from bs4 import BeautifulSoup as bs
import re
import json
from json.decoder import JSONDecodeError

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
        song_name = f'{song["track"]["name"]} {song["track"]["artists"][0]["name"]}'
        song_names.append(song_name)
    return song_names


def return_songs_from_album(album_id):
    # add on all artists featured on the track for better searching
    # might be a good idea to do the same for playlist, maybe even have a singular
    # method for both
    album_tracks = []
    for album_track in spotfy_obj.album(album_id)["tracks"]["items"]:
        album_track_name = spotfy_obj.album(album_id)["name"]
        album_track_name += f' {album_track["name"]}'
        for artist in album_track["artists"]:
            album_track_name += f' {artist["name"]}'
        album_tracks.append(album_track_name)
    return album_tracks
    pass


def find_song_on_youtube(song_name):
    song_name = song_name.replace(" ", "+")
    page = get(f"https://www.youtube.com/results?search_query={song_name}").content
    page = bs(page, 'html5lib')
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
    first_five_results = []
    for item in full_page:
        if len(first_five_results) >= 5:
            break
        try:
            page = item["videoRenderer"]
            first_five_results.append(parse_video_info(page))
        except KeyError:
            continue
    # TODO:sort for most relevant result
    '''
    https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
    
    '''
    video_info = {}
    return video_info


def parse_video_info(page):
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
    except KeyError:
        official_artist = False
    return {
        "Name": name,
        "Url": url,
        "Views": views,
        "Official Artist": official_artist
    }


def get_song_urls(playlist_or_album, resource_id):
    song_info = []
    song_list = []  # to get rid of pycharm error
    if playlist_or_album == "Playlist":  # rsrc id could be playlist or album id
        song_list = return_songs_from_playlist(resource_id)
    elif playlist_or_album == "Album":
        song_list = return_songs_from_album(resource_id)
    print("Collected Songs from Playlist")
    # need to async this
    for song in song_list:
        print(f"Searching for {song} on Youtube")
        song_info.append(find_song_on_youtube(song))
        print(f"Found {song} on Youtube")
        print("===========================================")
    print(song_info)
    pass


get_song_urls("Album", "6a4HHZe13SySfC50BGy8Hm")

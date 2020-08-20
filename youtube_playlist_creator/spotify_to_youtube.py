from spc import spotify_api_interface as spotify_api
from requests import get
from bs4 import BeautifulSoup as bs
import re
import json
from json.decoder import JSONDecodeError

spotfy_obj = spotify_api.spotify_obj()

'''
Pass playlist ID here, get a list of songs as strings
Search the strings on youtube, see if can get official video from yt, ranking by most
popular, favor videos from the artists official page.
'''
# prints playlist id's currently in Best Playlist id's
# print(json.dumps(spotfy_obj.current_user_playlists(), indent=4, skipkeys=True))
# for playlist in spotfy_obj.current_user_playlists()["items"]:
#     print(playlist["id"])

def return_songs_from_playlist(playlist_id):
    song_names = []
    for song in spotfy_obj.playlist_tracks(playlist_id=playlist_id)["items"]:
        print(song["track"]["name"])
        song_names.append(song["track"]["name"]) # need artist name as well
    return song_names

# return_songs_from_playlist("0ctxajn9gv8VEJi9UQztOg")

# song_name = "swimming pools kendrick lamar"
# song_name = song_name.replace(" ", "+")
# page = get(f"https://www.youtube.com/results?search_query={song_name}").content
# page = bs(page, 'lxml')
# print(len(page.find_all("script")))

# from requests we get a json response, different parsing for that vs html
# going


with open("src.html", "r+", encoding="utf-8") as file:
    page = bs(file, 'lxml')

# sort - official artist first, then numbers
page = str(page.find_all("script")[-3]).split("=", 1)[1].split(";")[0].strip()
# page = re.sub(r"\\", "'", page)
print(page)
# print(json.loads(page))
# try:
#     print(json.loads(page))
# except JSONDecodeError as e:
#     print(e.msg)
# for item in page.find_all("script"):
#     print("------------------------------")
#     print(item)

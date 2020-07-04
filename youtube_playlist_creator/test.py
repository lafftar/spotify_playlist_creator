from google_api_oath import main
from spc import db_interface
import json
from re import sub


class YTPlaylistCreator:
    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.title = f"Top 50 {artist_name} Songs Right Now"
        self.description = f"The most popular songs by {artist_name}! "
        self.yt_interface = main()

    def create_top50_playlist(self):
        # create the playlist with the title and descr
        self.yt_interface.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": f"{self.title}",
                    "description": f"{self.description}",
                    "tags": [
                        f"{self.artist_name}",
                        f"{self.artist_name} on spotify"
                    ],
                    "defaultLanguage": "en"
                },
                "status": {
                    "privacyStatus": "public" # change this for the user current_playlist version
                }
            }
        ).execute()

    def update_top50_playlist(self):
        yt_pl = self.yt_interface.playlists().list \
            (part="snippet, contentDetails", maxResults=25, mine=True).execute()
        # check if playlist has already been created
        for item in yt_pl["items"]:
            # if the playlist already exists, update it with our new playlist info
            if item["snippet"]["title"] == self.title:
                id = item["id"]
                # super bruteforce method, but eh
                # delete all playlist items
                # update playlist with new playlist items
                return
        # if the playlist does not exist, create it, and then try to update again
        print("Creating the playlist and trying to update again.")
        self.create_top50_playlist()
        self.update_top50_playlist()

    def playlist_video_ids(self):
        # grab video id's, put them in sqlite table to reduce quota cost. Expire after a week?
        # A day?
        # might be a good idea to grab video ids with a headless browser or somn, will save
        # 5000 quota calls, two playlists and i'm done. Going headless browser
        video_names = [f"{self.artist_name} {item[0]}"
                      for item in db_interface.select_data_from_table
                      (sub('[- ]', '_', self.artist_name), 'Name', 'Top_Songs')]
        print(video_names)
        pass


YTPlaylistCreator("Drake").playlist_video_ids()
# youtube = main()
# yt_pl = youtube.playlists().list(part="snippet, contentDetails", maxResults=25, mine=True) \
#     .execute()
# print(json.dumps(yt_pl, indent=4, sort_keys=True))
# for item in yt_pl["items"]:
#     id = item["id"]
#     youtube.playlists().delete(
#         id=id
#     ).execute()
# yt_pl = youtube.playlists().list(part="snippet, contentDetails", maxResults=25, mine=True) \
#     .execute()
# print(json.dumps(yt_pl, indent=4, sort_keys=True))
# create_playlist = youtube.playlists().insert(
#     part="snippet,status",
#     body={
#         "snippet": {
#             "title": f"Sample playlist created via API3",
#             "description": f"This is a sample playlist description.",
#             "tags": [
#                 "sample playlist",
#                 "API call"
#             ],
#             "defaultLanguage": "en"
#         },
#         "status": {
#             "privacyStatus": "public"
#         }
#     }
# )
# response = create_playlist.execute()
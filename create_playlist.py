# Step 1: Log Into Youtube
# Step 2: Grab Our Liked Videos
# Step 3: Create New Playlist
# Step 4: Search For Song
# Step 5: Add Song Into New Spotify Playlist

# Youtube Data API
# Spotify Web API
# Youtube DL Library

import json
import requests
import os

from secrets import spotify_user_id, spotify_token
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl


class CreatePlaylist:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    # Step 1: Log Into Youtube
    def get_youtube_client(self):
        """ Log Into Youtube, Copied from Youtube Data API """
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    # Step 2: Grab User Liked Videos
    def get_liked_videos(self):
        request = self.get_youtube_client().videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute()

        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

            # youtube_dl makes it easier to parse song & artist name
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)

            song_name = video["track"]
            artist = video["artist"]

            # save info
            self.all_song_info[video_title] = {
                "youtube_url": youtube_url,
                "song_name": song_name,
                "artist": artist,

                # get uri from provided info
                "spotify_uri": self.get_spotify_uri(song_name, artist)
            }

    # Step 3: Create New Playlist
    def create_playlist(self):
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        request_body = json.dumps({
            "name": "Youtube Liked Videos",
            "description": "All Youtube Liked Videos",
            "public": True
        })
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }

        response = requests.post(query, data=request_body, headers=headers)
        response_json = response.json()

        # playlist ID
        return response_json["id"]

    # Step 4: Search For Song
    def get_spotify_uri(self, song_name, artist):
        # may need this mess with this query
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }

        response = requests.get(query, headers=headers)
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        print(songs)

        # first track
        uri = songs[0]["uri"]

        return uri

    # Step 5: Add This Song Into New Spotify Playlist
    def add_song_to_playlist(self):
        # populate songs dict
        self.get_liked_videos()

        # collect all of uri
        uris = []
        for song, info in self.all_song_info.items():
            uris.append(info["spotify_uri"])

        # create new playlist
        playlist_id = self.create_playlist()

        # add all songs into new playlist

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
        request_data = json.dumps(uris)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }

        response = requests.post(query, data=request_data, headers=headers)
        response_json = response.json()
        return response_json


if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_song_to_playlist()


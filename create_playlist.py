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
from secrets import spotify_user_id, spotify_token


class CreatePlaylist:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token

    # Step 1: Log Into Youtube
    def get_youtube_client(self):
        pass

    # Step 2: Grab User Liked Videos
    def get_liked_videos(self):
        pass

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

        return response_json["id"]

    # Step 4: Search For Song
    def get_spotify_url(self, song_name, artist):
        """Search For the Song"""
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # only use the first song
        uri = songs[0]["uri"]

        return uri

    # Step 5: Add This Song Into New Spotify Playlist
    def add_song_to_playlist(self):
        pass


test = CreatePlaylist()
print(test.get_spotify_url("jungle", "casio"))


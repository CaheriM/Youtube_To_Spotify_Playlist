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

class CreatePlaylist:

    def __init__(self):
        pass

    # Step 1: Log Into Youtube
    def get_youtube_client(self):
        pass

    # Step 2: Grab User Liked Videos
    def get_liked_videos(self):
        pass

    # Step 3: Create New Playlist
    def create_playlist(self):
        request_body = json.dumps({
            "name": "Youtube Liked Videos",
            "description": "All Youtube Liked Videos",
            "public": True
        })

        print(request_body)

    # Step 4: Search For Song
    def get_spotify_url(self):
        pass

    # Step 5: Add This Song Into New Spotify Playlist
    def add_song_to_playlist(self):
        pass


test = CreatePlaylist()
test.create_playlist()
print(requests)

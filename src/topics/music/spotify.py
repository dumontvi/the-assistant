import logging
import json
import os
import sys
import time

import spotipy
import spotipy.util as util

from .music import Music

CONTEXT = {"username": os.getenv("SPOTIFY_USERNAME", None)}

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

scope = "app-remote-control streaming user-read-playback-position \
         user-read-recently-played user-top-read user-modify-playback-state \
         user-read-currently-playing user-read-playback-state \
         playlist-read-collaborative playlist-modify-private \
         playlist-modify-public playlist-read-private"


class Spotify(Music):
    def __init__(self):
        token = util.prompt_for_user_token(CONTEXT["username"], scope=scope)
        self.sp = spotipy.Spotify(auth=token)
        self.playlist_id = self.cache_master_playlist()

    def play_song(self, query):
        song, artist = self.parse_spotify_command(query.lower())

        # Search for song and artist
        response = self.sp.search(q=song, limit=10, market="CA")

        # If no artist - play first song
        if not artist:
            first_track = response["tracks"]["items"][0]

            # Play Track
            track_uri = first_track["uri"]
            self.sp.start_playback(uris=[track_uri])
            logger.info(f"Playing {song} on spotify")

            # Add related tracks to queue
            item_artist = first_track["artists"][0]
            self.add_to_song_queue(self.get_artist_top_songs(item_artist["id"]))
            return True
        else:
            # Try to match song for artist
            for item in response["tracks"]["items"]:
                item_artist = item["artists"][0]
                if artist in item_artist["name"].lower():
                    self.sp.start_playback(uris=[item["uri"]])
                    logger.info(f"Playing {item['name']} on spotify")

                    # Add related tracks to queue
                    add_to_song_queue(get_artist_top_songs(item_artist["id"]))
                    return True

        logger.error(f"ERROR: Song {query} not Found")
        return False

    def next_song(self):
        self.sp.next_track()

    def pause_song(self):
        self.sp.pause_playback()

    def about_me(self):
        print(f"The current user is {self.sp.me()['display_name']}")

    def prev_song(self):
        self.sp.previous_track()

    def parse_spotify_command(self, song):
        if "by" in song:
            parsed_command = song.split(" by ")
            song, artist = parsed_command[0], parsed_command[1]
        else:
            song, artist = song, None

        return song, artist

    def get_artist_top_songs(self, id):
        response = self.sp.artist_top_tracks(id)
        return [track["uri"] for track in response["tracks"]]

    def add_to_song_queue(self, song_list):
        for song in song_list:
            self.sp.add_to_queue(song)

    def set_volume(self, query):
        vol_num = [int(s) for s in query.split() if s.isdigit()]
        if vol_num and (vol_num[0] > 0 and vol_num[0] <= 100):
            logger.info(f"JAZZ: Setting Volume to {vol_num[0]}")
            self.sp.volume(vol_num[0])
        else:
            logger.error("ERROR: The number you stated is invalid")

    def get_playlists(self, user):
        return self.sp.user_playlists(user)["items"]

    def cache_master_playlist(self, name="Just Vibes"):
        for playlist in self.get_playlists(self.get_current_user()):
            if name.lower() in playlist["name"].lower():
                logger.info(f"JAZZ: Cached {name} as master playlist")
                return playlist["id"]

        return None

    def get_current_user(self):
        return CONTEXT["username"]

    def get_current_track(self):
        return self.sp.current_playback()["item"]["uri"]

    def get_current_playlist(self):
        return self.playlist_id

    def add_track_to_master_playlist(self):
        logger.info(f"JAZZ: Adding {self.get_current_track()} to playlist")
        return self.sp.user_playlist_add_tracks(
            self.get_current_user(), self.get_current_playlist(), [self.get_current_track()]
        )

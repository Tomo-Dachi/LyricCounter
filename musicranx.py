# make sure you add unittests, error handling, caching, rate limiting, ensure it meets pep8 standards
import json
import math

import requests as http


def count_lyrics(lyrics: str):
    # put words from lyric body into a list
    words = lyrics.split()

    # count length of list, then get full word count as musicranx only returns 30% of a track's total lyrics
    # then round up number as you can't have half a word in a song
    return math.ceil((len(words) / 3 * 10))


def check_status(response: dict):
    status_code = response["message"]["header"]["status_code"]
    if status_code == 401:
        raise http.exceptions.HTTPError("Api key is invalid")
    elif status_code == 402:
        raise http.exceptions.HTTPError("Number of requests has exceeded daily limit")
    elif status_code == 503:
        raise http.exceptions.HTTPError("The server is currently busy, please try again later")
    elif status_code != 200:
        raise http.exceptions.HTTPError("A HTTP error has occurred")

class MusicranxAPI:

    def __init__(self, apikey):
        self.API_KEY = apikey
        self.ROOT_URL = "https://api.musixmatch.com/ws/1.1/"

    def get_artist(self, artistname: str) -> str:
        """
        this method takes in the name of a musical artist, and returns a
        musicranx artist_id that can be used in subsequent requests
        """

        # Send request to musicranx
        try:
            params = {"format": "jsonp", "callback": "callback", "q_artist": artistname, "apikey": self.API_KEY}
            response = http.get(f"{self.ROOT_URL}artist.search", params).text

            # strip off jsonp content
            response = response[response.index("(") + 1: response.rindex(")")]

            # convert to python dictionary
            formatted_response = json.loads(response)
            check_status(formatted_response)

            return str(formatted_response['message']['body']['artist_list'][0]['artist']['artist_id'])
        except http.exceptions.HTTPError as err:
            print(err)

    def get_albums(self, artistid: str):
        """
        this method takes in a musicranx artistid, and returns a
        a list of album ids of all albums released by the artist
        """

        # Send request to musicranx
        try:
            params = {"format": "jsonp", "callback": "callback", "artist_id": artistid, "apikey": self.API_KEY}
            response = http.get(f"{self.ROOT_URL}artist.albums.get", params).text

            # strip off jsonp content
            response = response[response.index("(") + 1: response.rindex(")")]

            # convert to python dictionary
            formatted_response = json.loads(response)
            check_status(formatted_response)
            album_list = formatted_response['message']['body']['album_list']

            # Loop through response and add all album ids to list
            album_ids = [x['album']['album_id'] for x in album_list]
            return album_ids

        except http.exceptions.HTTPError as err:
            print(err)

    def get_tracks(self, albumid: str):
        """
        this method takes in a musicranx albumid, and returns a
        a list of track ids for all the tracks on the album
        """
        try:
        # Send request to musicranx
            params = {"format": "jsonp", "callback": "callback", "album_id": albumid, "apikey": self.API_KEY}
            response = http.get(f"{self.ROOT_URL}album.tracks.get", params).text

            # strip off jsonp content
            response = response[response.index("(") + 1: response.rindex(")")]

            # convert to python dictionary
            formatted_response = json.loads(response)
            check_status(formatted_response)
            track_list = formatted_response['message']['body']['track_list']

            # Loop through response and add all track ids to list
            track_ids = [x['track']['track_id'] for x in track_list]
            return track_ids
        except http.exceptions.HTTPError as err:
            print(err)

    def get_lyrics(self, trackid: str):
        """
        this method takes in a musicranx trackid, and returns
        the track's lyrics in string format
        """
        try:
            params = {"format": "jsonp", "callback": "callback", "track_id": trackid, "apikey": self.API_KEY}
            r = http.get(f"{self.ROOT_URL}track.lyrics.get", params).text

            # strip off jsonp content
            response = r[r.index("(") + 1: r.rindex(")")]

            # convert to python dictionary
            formatted_response = json.loads(response)
            check_status(formatted_response)
            unformatted_lyrics = formatted_response['message']['body']['lyrics']['lyrics_body']

            # remove musicranx disclaimer
            lyrics = unformatted_lyrics[:unformatted_lyrics.find('...')]
            return lyrics

        except http.exceptions.HTTPError as err:
            print(err)

    # count lyrics in a track

    def get_artist_average_wordcount(self, artist: str):
        total_word_count = 0
        total_songs = 0
        artist_id = self.get_artist(artist)
        album_ids = self.get_albums(str(artist_id))
        for album_id in album_ids:
            track_ids = self.get_tracks(str(album_id))
            for track_id in track_ids:
                total_word_count += count_lyrics(self.get_lyrics(str(track_id)))
                total_songs += 1

        return math.ceil(total_word_count / total_songs)


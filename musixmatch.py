# make sure you add unittests
import json
import math
import sys

import requests as http


def count_lyrics(lyrics: str):
    # put words from lyric body into a list
    words = lyrics.split()

    # count length of list, then get full word count as musixmatch only returns 30% of a track's total lyrics
    # then round up number as you can't have half a word in a song
    return math.ceil((len(words) / 3 * 10))


def check_status(response: dict):
    """
    This function is required as the musixmatch api always returns
    a 200 response. If an error occurs, the error is found in the
    response body itself and so it must be parsed below
    """

    status_code = response["message"]["header"]["status_code"]
    if status_code == 401:
        raise http.exceptions.HTTPError("Api key is invalid")
    elif status_code == 402:
        raise http.exceptions.HTTPError("Number of requests has exceeded daily limit")
    elif status_code == 404:
        raise http.exceptions.HTTPError("A resource could not be found")
    elif status_code == 503:
        raise http.exceptions.HTTPError(
            "The server is currently busy, please try again later"
        )
    elif status_code != 200:
        raise http.exceptions.HTTPError("A HTTP error has occurred")

ROOT_URL = "https://api.musixmatch.com/ws/1.1/"

def get_artist(apikey, artistname: str) -> str:
    """
    this method takes in the name of a musical artist, and returns a
    musixmatch artist_id that can be used in subsequent requests
    """

    # Send request to musixmatch
    try:
        params = {
            "format": "jsonp",
            "callback": "callback",
            "q_artist": artistname,
            "apikey": apikey,
        }
        response = http.get(f"{ROOT_URL}artist.search", params).text

        # strip off jsonp content
        response = response[response.index("(") + 1 : response.rindex(")")]

        # convert to python dictionary
        formatted_response = json.loads(response)
        check_status(formatted_response)

        if not formatted_response["message"]["body"]["artist_list"]:
            print("The artist you specified could not be found!")
            sys.exit(0)

        return str(
            formatted_response["message"]["body"]["artist_list"][0]["artist"][
                "artist_id"
            ]
        )
    except http.exceptions.HTTPError as err:
        print(err)
        sys.exit(0)

def get_albums(apikey, artistid: str):
    """
    this method takes in a musixmatch artistid, and returns a
    a list of album ids of all albums released by the artist
    """

    # Send request to musixmatch
    try:
        params = {
            "format": "jsonp",
            "callback": "callback",
            "artist_id": artistid,
            "apikey": apikey,
        }
        response = http.get(f"{ROOT_URL}artist.albums.get", params).text

        # strip off jsonp content
        response = response[response.index("(") + 1 : response.rindex(")")]

        # convert to python dictionary
        formatted_response = json.loads(response)
        check_status(formatted_response)
        album_list = formatted_response["message"]["body"]["album_list"]

        # Loop through response and add all album ids to list
        album_ids = [x["album"]["album_id"] for x in album_list]
        return album_ids

    except http.exceptions.HTTPError as err:
        print(err)
        sys.exit(0)

def get_tracks(apikey, albumid: str):
    """
    this method takes in a musixmatch albumid, and returns a
    a list of track ids for all the tracks on the album
    """
    try:
        # Send request to musixmatch
        params = {
            "format": "jsonp",
            "callback": "callback",
            "album_id": albumid,
            "apikey": apikey,
        }
        response = http.get(f"{ROOT_URL}album.tracks.get", params).text

        # strip off jsonp content
        response = response[response.index("(") + 1 : response.rindex(")")]

        # convert to python dictionary
        formatted_response = json.loads(response)
        check_status(formatted_response)
        track_list = formatted_response["message"]["body"]["track_list"]

        # Loop through response and add all track ids to list
        track_ids = [x["track"]["track_id"] for x in track_list]
        return track_ids
    except http.exceptions.HTTPError as err:
        print(err)
        sys.exit()

def get_lyrics(apikey, trackid: str):
    """
    this method takes in a musixmatch trackid, and returns
    the track's lyrics in string format
    """
    try:
        params = {
            "format": "jsonp",
            "callback": "callback",
            "track_id": trackid,
            "apikey": apikey,
        }
        r = http.get(f"{ROOT_URL}track.lyrics.get", params).text

        # strip off jsonp content
        response = r[r.index("(") + 1 : r.rindex(")")]

        # convert to python dictionary
        formatted_response = json.loads(response)
        check_status(formatted_response)
        unformatted_lyrics = formatted_response["message"]["body"]["lyrics"][
            "lyrics_body"
        ]

        # remove musixmatch disclaimer
        lyrics = unformatted_lyrics[: unformatted_lyrics.find("...")]
        return lyrics

    except http.exceptions.HTTPError as err:
        print(err)
        sys.exit(0)

# count lyrics in a track

def get_artist_average_wordcount(apikey, artist: str):
    total_word_count = 0
    total_songs = 0
    artist_id = get_artist(apikey, artist)
    album_ids = get_albums(apikey, artist_id)
    for album_id in album_ids:
        track_ids = get_tracks(apikey, str(album_id))
        for track_id in track_ids:
            total_word_count += count_lyrics(get_lyrics(apikey, str(track_id)))
            total_songs += 1

    return math.ceil(total_word_count / total_songs)

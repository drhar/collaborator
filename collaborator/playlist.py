import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import List
from collaborator.spotipy_utils import get_all_paged_items


client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class SpotifyPlaylist(object):
    def __init__(self, playlist_uri: str, spotify_client: spotipy.Spotify):
        """
        A Spotify playlist. Hides all the nasty API interactions and JSON .

        :param playlist_uri: The spotify uri for the playlist in the format
                             'spotify:playlist:<playlist_id>'.
        :param spotify_client: A logged in connection to Spotify.
        """
        self.playlist_uri = playlist_uri
        self.spotify = spotify_client
        # The JSON blob returned by an API search
        self.playlist_json = dict()
        # True if the owner allows other users to modify the playlist.
        self.collaborative = False
        # The playlist description. Only returned for modified, verified
        # playlists, otherwise null.
        self.description = ""
        # A link to the Web API endpoint providing full details of the
        # playlist.
        self.href = ""
        # The Spotify ID for the playlist.
        self.id = ""
        # The name of the playlist.
        self.name = ""
        # The user who owns the playlist
        self.owner = dict()
        # The playlist’s public/private status: True the playlist is public,
        # False the playlist is private, None the playlist status is not
        # relevant
        self.public = False
        # A list of Spotify 'playlist track' JSON objects.
        self.tracks = list()
        self.search_fields = "collaborative,description,href,id,name,owner," \
                             "public,tracks"
        self.not_implemented_fields = "external_urls,images,snapshot_id,type"

        self.refresh_playlist()

    def refresh_playlist(self):
        """
        Get all the info for the playlist.
        """
        self.playlist_json = self.spotify.playlist(self.playlist_uri,
                                                   fields=self.search_fields)
        self.collaborative = self.playlist_json["collaborative"]
        self.description = self.playlist_json["description"]
        self.href = self.playlist_json["href"]
        self.id = self.playlist_json["id"]
        self.name = self.playlist_json["name"]
        self.owner = self.playlist_json["owner"]
        self.public = self.playlist_json["public"]
        # Tracks are only returned in pages of 100, so this requires
        # subsequent calls to the API.
        self.tracks = get_all_paged_items(self.spotify,
                                          self.playlist_json['tracks'])

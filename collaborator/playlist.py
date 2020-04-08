import spotipy
from collaborator.spotipy_utils import get_all_paged_items


class SpotifyPlaylist(object):
    def __init__(self, playlist_uri: str, spotify_connection: spotipy.Spotify):
        """
        A Spotify playlist. Hides all the nasty API interactions and JSON.
        A Spotify connection is required for this as the tracks in a
        playlist are returned in pages.

        :param playlist_uri: The spotify uri for the playlist in the format
                             'spotify:playlist:<playlist_id>'.
        :param spotify_connection: A logged in connection to Spotify.
        """
        self.playlist_uri = playlist_uri
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
        # A list of SpotifyPlaylistTrack objects.
        self.tracks = list()
        self.search_fields = "collaborative,description,href,id,name,owner," \
                             "public,tracks"
        # Fields that we don't currently bother retrieving for this playlist.
        self.not_implemented_fields = "external_urls,images,snapshot_id,type"

        self.refresh_playlist(spotify_connection)

    def refresh_playlist(self, spotify_connection: spotipy.Spotify):
        """
        Get all the info for the playlist.

        :param spotify_connection: A logged in connection to Spotify.
        """
        self.playlist_json = spotify_connection.playlist(
                                 self.playlist_uri,
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
        track_list = get_all_paged_items(
                          spotify_connection=spotify_connection,
                          first_page=self.playlist_json['tracks'])
        for track in track_list:
            self.tracks.append(SpotifyPlaylistTrack(playlist_track_json=track))


class SpotifyTrack(object):
    def __init__(self,
                 track_json: dict = None,
                 track_uri: str = "",
                 spotify_connection: spotipy.Spotify = None):
        """
        A Spotify track. Hides all the nasty API interactions and JSON .

        :param track_json: The JSON blob returned by the Spotify API on
                           searching for this playlist. Provide either
                           this or a URI and connection to Spotify.
        :param track_uri: The spotify uri for the playlist in the format
                          'spotify:playlist:<playlist_id>'. Only required if
                          not specifying track_json.
        :param spotify_connection: A logged in connection to Spotify. Only
                                   required if not specifying track_json.
        """
        if track_json:
            self.track_json = track_json
        elif track_uri and spotify_connection:
            self.track_json = spotify_connection.track(track_uri)
        else:
            raise RuntimeError("Must specify either a track's JSON, "
                               "or a connection to Spotify and the track's"
                               "Spotify URI")

        # The album on which the track appears. Includes the album uri
        # under the key "uri" which can be used to get the full information
        # for the album.
        self.simple_album = self.track_json["album"]
        # A list of the artists who performed the track. Each artist dict
        # includes a key, "uri" containing the artist uri which can be used
        # to get the full information for the artist.
        self.simple_artist_list = self.track_json["artists"]
        # The track length in milliseconds
        self.duration = self.track_json["duration_ms"]
        # Whether or not the track has explicit lyrics (True = yes it does;
        # False = no it does not OR unknown).
        self.explicit = self.track_json["explicit"]
        # The Spotify ID for the track.
        self.id = self.track_json["id"]
        # The name of the track.
        self.name = self.track_json["name"]
        # The Spotify popularity of the track. The value will be between 0 and
        # 100, with 100 being the most popular.
        self.popularity = self.track_json["popularity"]
        # A link to a 30 second preview (MP3 format) of the track. Can be None.
        self.preview = self.track_json["preview_url"]
        # The Spotify URI for the track.
        self.uri = self.track_json["uri"]


class SpotifyPlaylistTrack(SpotifyTrack):
    def __init__(self, playlist_track_json: dict):
        """
        A Spotify 'playlist track' object. This contains the playlist
        metadata on top of a normal track.

        :param playlist_track_json: The JSON for the Spotify 'playlist
                                    track' object. This can only be retrieved
                                    from a playlist as opposed to direct from
                                    the API.
        """
        self.playlist_track_json = playlist_track_json
        super().__init__(track_json=self.playlist_track_json["track"])

        # The date and time the track was added.
        self.added_at = playlist_track_json["added_at"]
        # A SpotifyUser object for the user who added the track.
        self.added_by = SpotifyUser(user_json=playlist_track_json["added_by"])
        # Whether this track is a local file or not
        self.is_local = playlist_track_json["is_local"]


class SpotifyUser(object):
    def __init__(self,
                 user_json: dict = None,
                 user_uri: str = "",
                 spotify_connection: spotipy.Spotify = None):
        """
        A Spotify user. Hides all the nasty API interactions and JSON .

        :param user_json: The JSON blob returned by the Spotify API on
                          searching for this playlist. Provide either
                          this or a URI and connection to Spotify.
        :param user_uri: The spotify uri for the playlist in the format
                         'spotify:playlist:<playlist_id>'. Only required if
                         not specifying user_json.
        :param spotify_connection: A logged in connection to Spotify. Only
                                   required if not specifying user_json.
        """
        if user_json:
            self.user_json = user_json
        elif user_uri and spotify_connection:
            self.user_json = spotify_connection.user(user_uri)
        else:
            raise RuntimeError("Must specify either a user's JSON, "
                               "or a connection to Spotify and the user's"
                               "Spotify URI")

        self.display_name = ""
        self.id = self.user_json["id"]
        self.uri = self.user_json["uri"]

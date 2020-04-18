import spotipy
from collaborator.spotipy_utils import get_all_paged_items
from datetime import datetime
from dateutil import parser as dateparser


class SpotifyPlaylist(object):
    def __init__(
        self,
        playlist_json: dict = None,
        playlist_uri: str = "",
        spotify_connection: spotipy.Spotify = None,
    ):
        """
        A Spotify playlist. Hides all the nasty API interactions and JSON.
        A Spotify connection is required for this as the tracks in a
        playlist are returned in pages.

        :param playlist_json: The JSON blob returned by the Spotify API on searching for this playlist. Provide either
                              this or a URI and connection to Spotify. If using this, it is recommended to call
                              get_track_info and get_artist_info so that the playlist can be organised.
        :param playlist_uri: The spotify uri for the playlist in the format spotify:playlist:<playlist_id>'. Not
                             required if providing playlist_json
        :param spotify_connection: A logged in connection to Spotify. Not required if using playlist_json..
        """
        if playlist_json:
            self.playlist_uri = playlist_json["uri"]
            self.playlist_json = playlist_json
        elif playlist_uri and spotify_connection:
            self.playlist_uri = playlist_uri
            self.playlist_json = dict()
        else:
            raise RuntimeError(
                "Must specify either a track's JSON or a connection to Spotify and the playlist's"
                "Spotify URI"
            )

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
        # A sorted version of self.tracks, with the first item the first track added to the playlist and the last one
        # the last added.
        self.tracks_by_time = list()
        # A dictionary where keys are artist uris and the values are a time sorted list of the tracks they have on the
        # playlist.
        self.tracks_by_artist = dict()
        # A dictionary where keys are user uris and the values are a time sorted list of the tracks they have on the
        # playlist.
        self.tracks_by_user = dict()
        # A dictionary where keys are genre strings and the values are a time sorted list of the tracks that are by an
        # artist with that genre.
        self.tracks_by_genre = dict()
        # A dict of SpotifyArtist objects indexed by URI representing each artist with music on the playlist
        # (including features).
        self.artists = dict()
        # A dict of SpotifyUser objects indexed by URI representing each user that has added music to the playlist.
        self.users = dict()
        # The artist with the most songs on the playlist as a SpotifyArtist object.
        self.most_used_artist = None
        # The genre with the most songs on the playlist as a SpotifyArtist object.
        self.most_used_genre = ""
        self.search_fields = (
            "collaborative,description,href,id,name,owner," "public,tracks"
        )
        # Fields that we don't currently bother retrieving for this playlist.
        self.not_implemented_fields = "external_urls,images,snapshot_id,type"

        if self.playlist_json:
            self.store_playlist_info()
        else:
            self.refresh_playlist(spotify_connection)

    def refresh_playlist(self, spotify_connection: spotipy.Spotify):
        """
        Get all the info for the playlist.

        :param spotify_connection: A logged in connection to Spotify.
        """
        self.playlist_json = spotify_connection.playlist(
            self.playlist_uri, fields=self.search_fields
        )
        self.store_playlist_info()
        self.get_track_info(spotify_connection=spotify_connection)
        self.get_artist_info(spotify_connection=spotify_connection)
        self.sort_playlist()

    def store_playlist_info(self):
        """
        Store the playlist metadata. These are the only fiedlds that it's worth getting without a connection to
        Spotify.
        """
        self.collaborative = self.playlist_json["collaborative"]
        self.description = self.playlist_json["description"]
        self.href = self.playlist_json["href"]
        self.id = self.playlist_json["id"]
        self.name = self.playlist_json["name"]
        self.owner = self.playlist_json["owner"]
        self.public = self.playlist_json["public"]

    def get_track_info(self, spotify_connection: spotipy.Spotify):
        """
        Tracks are only returned in pages of 100, so this requires subsequent calls to the API.
        :param spotify_connection: A logged in connection to Spotify.
        """
        # Delete any existing track info before adding them all back in.
        self.tracks = list()

        track_list = get_all_paged_items(
            spotify_connection=spotify_connection,
            first_page=self.playlist_json["tracks"],
        )

        for track in track_list:
            self.tracks.append(SpotifyPlaylistTrack(playlist_track_json=track))

    def sort_by_track_info(self):
        """
        Organise the tracks in the playlist into some consumable formats using the properties of a SpotifyTrack object.
        To sort by information about artists (e.g. genre) use sort_by_artist_info.
        """
        # Sort tracks by time first so that all other sorts are also sorted by time. Remove duplicates by setting
        # before sorting.
        self.tracks_by_time = list(set(self.tracks))
        self.tracks_by_time.sort(key=lambda x: x.added_at)

        # Get rid of any existing data.
        self.tracks_by_artist = dict()
        self.tracks_by_user = dict()

        # we can get the users at the same time, so delete any existing info.
        self.users = dict()

        for track in self.tracks_by_time:
            user = track.added_by
            track_artist_list = track.simple_artist_list
            if user.uri not in self.tracks_by_user:
                self.tracks_by_user[user.uri] = []
                self.users[user.uri] = user
            self.tracks_by_user[user.uri].append(track)
            for artist in track_artist_list:
                if artist["uri"] not in self.tracks_by_artist:
                    self.tracks_by_artist[artist["uri"]] = []
                self.tracks_by_artist[artist["uri"]].append(track)

    def get_artist_info(self, spotify_connection: spotipy.Spotify):
        """
        We only get rudimentary information about artists with track objects. Notably, this excludes genres. The API
        can get the info of 50 artists with a single API call, rather than doing this for each artist.
        :param spotify_connection: A logged in connection to Spotify.
        """
        max_artists_per_api_call = 50

        # Delete any existing artists.
        self.artists = dict()

        # Get a list of the artists in the playlist.
        if not self.tracks_by_artist:
            self.sort_by_track_info()

        artist_uri_list = [artist_uri for artist_uri in self.tracks_by_artist]
        artist_search_queue = list()
        # Sort the list of artists into lists that can be found in a single API search.
        for api_search_num in range(
            (len(artist_uri_list) + max_artists_per_api_call - 1)
            // max_artists_per_api_call
        ):
            artist_search_queue.append(
                artist_uri_list[
                    api_search_num
                    * max_artists_per_api_call : (api_search_num + 1)
                    * max_artists_per_api_call
                ]
            )

        artist_json_list = list()
        for api_search in artist_search_queue:
            artist_json_list.extend(spotify_connection.artists(api_search)["artists"])

        for artist in artist_json_list:
            self.artists[artist["uri"]] = SpotifyArtist(artist_json=artist)

    def sort_by_artist_info(self):
        """
        Organize the playlist by properties on a SpotifyArtist object. Currently this is just genre.
        Requires get_artist_information to have been run first.
        """
        # Delete any existing information.
        self.tracks_by_genre = dict()
        for artist in self.artists:
            for genre in self.artists[artist].genres:
                if genre not in self.tracks_by_genre:
                    # Add all the tracks by this artist the first time we find a genre as we know it won't have
                    # duplicates.
                    self.tracks_by_genre[genre] = list()
                    self.tracks_by_genre[genre].extend(self.tracks_by_artist[artist])
                else:
                    # Tracks have multiple artists, which may have the same genre.
                    # Don't want duplicate tracks in genre list so check before adding.
                    for track in self.tracks_by_artist[artist]:
                        if track not in self.tracks_by_genre[genre]:
                            self.tracks_by_genre[genre].append(track)
        # Because these tracks were sorted by artist, we need to sort the time ordering of each genre tracklist now.
        for genre in self.tracks_by_genre:
            self.tracks_by_genre[genre].sort(key=lambda x: x.added_at)

        # Pull out some interesting stats.
        most_used_artist_uri = max(
            self.tracks_by_artist, key=lambda x: len(set(self.tracks_by_artist[x]))
        )
        self.most_used_artist = self.artists[most_used_artist_uri]
        self.most_used_genre = max(
            self.tracks_by_genre, key=lambda x: len(set(self.tracks_by_genre[x]))
        )

    def sort_playlist(self):
        """
        Sort the tracks in the playlist.
        """
        self.sort_by_track_info()
        self.sort_by_artist_info()


class SpotifyTrack(object):
    def __init__(
        self,
        track_json: dict = None,
        track_uri: str = "",
        spotify_connection: spotipy.Spotify = None,
    ):
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
            raise RuntimeError(
                "Must specify either a track's JSON, "
                "or a connection to Spotify and the track's"
                "Spotify URI"
            )

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

        # The datetime object for when the track was added.
        self.added_at = dateparser.isoparse(playlist_track_json["added_at"])
        # A SpotifyUser object for the user who added the track.
        self.added_by = SpotifyUser(user_json=playlist_track_json["added_by"])
        # Whether this track is a local file or not
        self.is_local = playlist_track_json["is_local"]


class SpotifyUser(object):
    def __init__(
        self,
        user_json: dict = None,
        user_uri: str = "",
        spotify_connection: spotipy.Spotify = None,
    ):
        """
        A Spotify user. Hides all the nasty API interactions and JSON .

        :param user_json: The JSON blob returned by the Spotify API on searching for
                          this playlist. Provide either this or a URI and connection
                          to Spotify.
        :param user_uri: The spotify uri for the playlist in the format
                         'spotify:playlist:<playlist_id>'. Only required if not
                         specifying user_json.
        :param spotify_connection: A logged in connection to Spotify. Only required
                                   if not specifying user_json.
        """
        if user_json:
            self.user_json = user_json
        elif user_uri and spotify_connection:
            self.user_json = spotify_connection.user(user_uri)
        else:
            raise RuntimeError(
                "Must specify either a user's JSON, or a connection "
                "to Spotify and the user's Spotify URI"
            )

        if "display_name" in user_json:
            self.display_name = user_json["display_name"]
        else:
            self.display_name = ""
        self.id = self.user_json["id"]
        self.uri = self.user_json["uri"]


class SpotifyArtist(object):
    def __init__(
        self,
        artist_json: dict = None,
        artist_uri: str = "",
        spotify_connection: spotipy.Spotify = None,
    ):
        """
        A Spotify artist. Hides all the nasty API interactions and JSON .

        :param artist_json: The JSON blob returned by the Spotify API on searching
                            for this playlist. Provide either this or a URI and
                            connection to Spotify.
        :param artist_uri: The spotify uri for the playlist in the format
                         'spotify:playlist:<playlist_id>'. Only required if not
                         specifying artist_json.
        :param spotify_connection: A logged in connection to Spotify. Only required
                                   if not specifying artist_json.
        """
        if artist_json:
            self.artist_json = artist_json
        elif artist_uri and spotify_connection:
            self.artist_json = spotify_connection.artist(artist_uri)
        else:
            raise RuntimeError(
                "Must specify either a artist's JSON, or a connection "
                "to Spotify and the artist's Spotify URI"
            )
        # The Spotify URI for the artist.
        self.uri = self.artist_json["uri"]
        # The Spotify ID for the artist.
        self.id = self.artist_json["id"]
        # The name of the artist.
        self.name = self.artist_json["name"]
        # A list of the genres the artist is associated with.
        self.genres = self.artist_json["genres"]
        # The Spotify popularity of the artist. The value will be between 0 and 100,
        # with 100 being the most popular.
        self.popularity = self.artist_json["popularity"]

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collaborator.playlist import SpotifyPlaylist, SpotifyArtist, SpotifyPlaylistTrack
from collaborator.graph_utils import plot_sorted_tracks
from collaborator.live_shows import search_songkick_locations, get_events_for_location
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
PLAYLIST_URI = 'spotify:playlist:1cIYJbMgyTsEfHtPVxWETv'


ddm = SpotifyPlaylist(playlist_uri=PLAYLIST_URI, spotify_connection=sp)

location_results = search_songkick_locations("London")
print(location_results)

user_songs = 0
for user in ddm.tracks_by_user:
    print("User: {} added {} songs".format(user, len(ddm.tracks_by_user[user])))
    user_songs += len(ddm.tracks_by_user[user])
artist_songs = []
for artist in ddm.tracks_by_artist:
    artist_songs.extend(ddm.tracks_by_artist[artist])
artist_songs = len(set(artist_songs))
print("There are {} songs in the playlist".format(len(ddm.tracks)))
print("Total according to artists: {}".format(artist_songs))
print("Total according to users: {}".format(user_songs))
print("There are {} artists in the playlist".format(len(ddm.tracks_by_artist)))
print("The most popular artist is {}, with {} songs".format(ddm.artists[ddm.most_used_artist.uri].name,
                                                            len(ddm.tracks_by_artist[ddm.most_used_artist.uri])))


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collaborator.playlist import SpotifyPlaylist, SpotifyArtist


client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
PLAYLIST_URI = 'spotify:playlist:1cIYJbMgyTsEfHtPVxWETv'

ddm = SpotifyPlaylist(playlist_uri=PLAYLIST_URI, spotify_connection=sp)

ddm.organize_playlist()

artists = {}
tracks_by_genre = {}
genre_list = []

for artist in ddm.tracks_by_artist:
    artist_object = SpotifyArtist(artist_uri=artist, spotify_connection=sp)
    artists[artist] = artist_object
    for genre in artist_object.genres:
        if genre not in tracks_by_genre:
            # Add all the tracks by this artist the first time we find a genre as we know it won't have duplicates in.
            tracks_by_genre[genre] = list()
            tracks_by_genre[genre].extend(ddm.tracks_by_artist[artist])
            genre_list.append(genre)
        else:
            # Tracks have multiple artists, which may have the same genre. Don't want duplicate tracks in genre list so
            # check now.
            for track in ddm.tracks_by_artist[artist]:
                if track not in tracks_by_genre[genre]:
                    tracks_by_genre[genre].append(track)

most_used_genre = max(tracks_by_genre, key= lambda x: len(set(tracks_by_genre[x])))
most_used_artist = max(ddm.tracks_by_artist, key= lambda x: len(set(ddm.tracks_by_artist[x])))
for user in ddm.tracks_by_user:
    print("User: {} added {} songs".format(user, len(ddm.tracks_by_user[user])))

print("There are {} artists in the plaaylist".format(len(artists)))
print("There are {} genres in the playlist".format(len(genre_list)))
print("The most poular genre is {}, with {} songs".format(most_used_genre, len(tracks_by_genre[most_used_genre])))
print("The most popular artist is {}, with {} songs".format(artists[most_used_artist].name,
                                                            len(ddm.tracks_by_artist[most_used_artist])))

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collaborator.playlist import SpotifyPlaylist, SpotifyArtist

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#
# def find_who_added_tracks_from_page(tracks_page, user_dict):
#     for i, track_item in enumerate(tracks_page['items']):
#         track = track_item['track']
#         user = track_item['added_by']['id']
#         if user not in user_dict:
#             print("Adding user {} to dict".format(user))
#             user_dict[user] = []
#         user_dict[user].append(track)
#
#
# playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv', fields='tracks')
# track_page = playlist['tracks']
# user_tracks = {}
# find_who_added_tracks_from_page(track_page, user_tracks)
#
# while track_page['next']:
#     track_page = sp.next(track_page)
#     find_who_added_tracks_from_page(track_page, user_tracks)
#
# for user in user_tracks:
#     print("User: {} added {} songs".format(user, len(user_tracks[user])))
# dan_tracks = user_tracks['1110119342']
#
# raveena = sp.artist('2kQnsbKnIiMahOetwlfcaS')

PLAYLIST_URI = 'spotify:playlist:1cIYJbMgyTsEfHtPVxWETv'


def get_items_from_page(page: dict):
    """
    Returns a list of all the items from a Spotify results page.
    :param page: A Spotify page object.
    :return: A list of all the items from the page.
    """
    item_list = []
    print("Retrieving items from page")

    for i, item in enumerate(page['items']):
        item_list.append(item)

    print("Found {} items".format(len(item_list)))

    return item_list


def get_playlist_track_info(playlist_uri: str):
    """
    Returns all the 'track items' for songs in the playlist. These contain
    the tracks themselves as well as all the metadata about the track in the
    context of the playlist (e.g. who added and when).

    :param playlist_uri: The spotify uri for the playlist in the format
                        'spotify:playlist:<playlist_id>'
    :return: A list of 'track items'
    """
    # Only return the tracks for performance reasons.
    playlist = sp.playlist(playlist_uri, fields='')

    # Spotify returns results in pages limited to a certain number of tracks.
    track_page = playlist['tracks']
    track_list = get_items_from_page(track_page)

    while track_page['next']:
        track_page = sp.next(track_page)
        track_list.extend(get_items_from_page(track_page))

    return track_list


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

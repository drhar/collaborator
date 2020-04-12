import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collaborator.playlist import SpotifyPlaylist, SpotifyArtist, SpotifyPlaylistTrack
from typing import List, Dict
import plotly.graph_objects as go
import plotly.io as pio

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
PLAYLIST_URI = 'spotify:playlist:1cIYJbMgyTsEfHtPVxWETv'

ddm = SpotifyPlaylist(playlist_uri=PLAYLIST_URI, spotify_connection=sp)

ddm.organize_playlist()


    most_used_genre = max(tracks_by_genre, key= lambda x: len(set(tracks_by_genre[x])))

    print("There are {} genres in the playlist".format(len(genre_list)))
    print("The most poular genre is {}, with {} songs".format(most_used_genre, len(tracks_by_genre[most_used_genre])))
    return tracks_by_genre


def create_track_count_over_time_data_dict(tracklist: List[SpotifyPlaylistTrack], name: str="")-> dict:
    """
    Create a dictionary from which plotly can plot line graphs from a list of SpotifyPlaylistTracks. Creates a
    dictionary that can be used as a plotly data set showing cumulative track count over time.

    :param tracklist: List of SpotifyPlaylistTrack objects.
    :param name: Optional name for this data set. Will be included as a third column if provided.
    :return: A dictionary where x is a list of datetime objects and y is the number of tracks added_at that time or
             earlier.
    """
    plot_dict = {"x": [], "y": [], "name": name, "type": "scatter", "y0": 0}

    y_total = 0
    for track in tracklist:
        time = track.added_at.isoformat()
        y_total += 1
        if time not in plot_dict["x"]:
            plot_dict["x"].append(time)
            plot_dict["y"].append(y_total)
        else:
            plot_dict["y"][-1] += 1

    return plot_dict


def plot_organized_track_dictionary(track_dict: Dict[str, List[SpotifyPlaylistTrack]], title: str="") -> dict:
    """
    Create a plotly line graph showing the track count over time for various datasets.
    :param track_dict: A dictionary where each key/value pair is a data set to plot on the same axes. Value is a list
                       of SpotifyPlaylistTrack objects. The Key will be used as the name for the data set.
    :param title: The title for the graph as a string.
    :return: A dictionary that can be used to create a graph using plotly.io.show().
    """
    figure_dict = {"data": [], "layout": {"title": title}}
    data_sets = []
    for data_name in track_dict:
        data_set = create_track_count_over_time_data_dict(track_dict[data_name], name=data_name)
        data_sets.append(data_set)

    figure_dict["data"] = data_sets

    return figure_dict


user_graph = plot_organized_track_dictionary(ddm.tracks_by_user, title="Tracks added over time by each user")

tracks_by_genre = find_genres(ddm)
genre_graph = plot_organized_track_dictionary(tracks_by_genre, title="Number of tracks in different genres")

pio.show(user_graph)
pio.show(genre_graph)

most_used_artist = max(ddm.tracks_by_artist, key= lambda x: len(set(ddm.tracks_by_artist[x])))

for user in ddm.tracks_by_user:
    print("User: {} added {} songs".format(user, len(ddm.tracks_by_user[user])))

print("There are {} artists in the playlist".format(len(ddm.tracks_by_artist)))
print("The most popular artist is {}, with {} songs".format(artists[most_used_artist].name,
                                                            len(ddm.tracks_by_artist[most_used_artist])))


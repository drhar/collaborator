from collaborator.playlist import SpotifyPlaylistTrack
from typing import List, Dict
from datetime import datetime


def produce_track_time_series(
    tracklist: List[SpotifyPlaylistTrack], name: str = ""
) -> dict:
    """
    Create a dictionary from which plotly can use as a data series from a list of
    SpotifyPlaylistTracks. The series will be total number of tracks against time.

    :param tracklist: List of SpotifyPlaylistTrack objects.
    :param name: Optional name for this data set. Will be used as the name for the
                 series if provided.
    :return: A dictionary where x is a list of datetime objects and y is the number
             of tracks added_at that time or earlier.
    """
    plot_dict = {
        "x": [],
        "y": [],
        "name": name,
        "type": "scatter",
    }

    # Sort tracks by time first so we don't have to keep iterating through the whole
    # list.
    tracklist.sort(key=lambda x: x.added_at)

    row_index = 0
    track_count = 0
    for track in tracklist:
        track_count += 1
        time = track.added_at.isoformat()
        # If we have an empty table we need to add a row.
        if row_index == 0:
            plot_dict["x"].append(time)
            plot_dict["y"].append(track_count)
            continue
        # If there are two tracks with the same time stamp, then increase the count for
        # that time.
        if plot_dict["x"][row_index] != time:
            plot_dict["x"].append(time)
            plot_dict["y"].append(track_count)
            row_index += 1
        else:
            plot_dict["y"][row_index] += 1

    # Need to plot a point for now So graphs that haven't updated for a while don't just stop.
    time = datetime.now()
    plot_dict["x"].append(time)
    plot_dict["y"].append(track_count)

    return plot_dict


def plot_sorted_tracks(
    track_dict: Dict[str, List[SpotifyPlaylistTrack]], title: str = ""
) -> dict:
    """
    Create a plotly line graph showing the track count over time for various series.
    :param track_dict: A dictionary where each key/value pair is a data series to plot
                       on the same axes. Value is a list of SpotifyPlaylistTrack
                       objects. The Key will be used as the name for the series.
    :param title: The title for the graph as a string.
    :return: A dictionary that can be used to create a graph using plotly.io.show().
    """
    series = []
    for data_name in track_dict:
        data_set = produce_track_time_series(track_dict[data_name], name=data_name)
        series.append(data_set)

    figure_dict = {"data": series, "layout": {"title": title}}

    return figure_dict

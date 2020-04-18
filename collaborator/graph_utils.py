from collaborator.playlist import SpotifyPlaylistTrack, SpotifyPlaylist
from collaborator.live_shows import SongkickEvent
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
    plot_dict["x"].append(time.isoformat())
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

    figure_dict = {
        "data": series,
        "layout": {
            "title": title,
            "paper_bgcolor": "#1a1c23",
            "plot_bgcolor": "rgb(34,37,43)",
        }
    }

    return figure_dict


def create_events_table(
    event_list: List[dict],
    playlist: SpotifyPlaylist
) -> List[dict]:
    """
    Create a dictionary that can be used as a DashTable data input. Data will be events from event_list at which an
    artist from the playlist is performing.
    :param event_list: A list of dictionaries each representing an event object received from the songkick API.
    :param playlist: A SpotifyPlaylist.
    :return: A dictionary of the following format, note each list is sorted by date, earliest first:
                'name': A list of the names of the events as strings.
                'venue': A list of the venues for the events.
                'artist': A list of the artists performing at the events.
                'date': A list of the dates of the events.
                'status': A list of the status of the events (e.g. whether they're cancelled).
                'link': A list of links to the songkick event for the events.
    """
    event_table = []

    for event in event_list:
        sk_event = SongkickEvent(event)
        for artist in sk_event.artists:
            if playlist.is_artist_in_playlist(artist):
                event_table.append({
                    "name": sk_event.display_name,
                    "venue": sk_event.venue,
                    "artist": ", ".join(sk_event.artists),
                    "date": sk_event.start.strftime("%d %b %Y"),
                    "status": sk_event.status,
                    "link": sk_event.uri
                })
                break

    if not event_table:
        event_table = [{
            "name": None,
            "venue": None,
            "artist": None,
            "date": None,
            "status": None,
            "link": None
        }]

    return event_table

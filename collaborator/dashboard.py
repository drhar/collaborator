import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from collaborator.playlist import SpotifyPlaylist, SpotifyArtist, SpotifyPlaylistTrack
from collaborator.live_shows import get_events_for_location
from collaborator.graph_utils import plot_sorted_tracks, create_events_table


client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = html.Div(
    className="row",
    children=[
        html.Div(
            className="three columns div-left-panel",
            children=[
                # Div for Left Panel App Info
                html.Div(
                    className="div-info",
                    children=[
                        html.H3(
                            className="title-header", children="Playlist Dashboard"
                        ),
                        html.P(
                            """
                            This app gives you a graphical view of your playlist so you 
                            can improve it going forwards.
                            """
                        ),
                        html.H4(id='playlist-name'),
                        html.Label("Spotify Playlist URI"),
                        dcc.Input(
                            id='playlist-uri',
                            value="spotify:playlist:1cIYJbMgyTsEfHtPVxWETv",
                            type='text'
                        ),
                        html.Label("Songkick location ID"),
                        dcc.Input(
                            id="user-location",
                            value="24426",
                            type="number"
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="nine columns div-right-panel",
            children=[
                dcc.Graph(
                    id="user-tracks-graph",
                ),
                dcc.Graph(
                    id="genre-tracks-graph",
                ),
                html.Div(
                    id="hidden-event-info",
                    style={"display": "none"}
                ),
                dash_table.DataTable(
                    id="events-table",
                    style_table={"overflowY": "scroll"},
                    style_cell={
                        "textAlign": "left",
                        "backgroundColor": "rgb(34,37,43)",
                        "color": "#b2b2b2"
                    },
                ),
            ],
        ),
    ],
)


@app.callback(Output("hidden-event-info", "children"), [Input("user-location", "value")])
def update_event_location(location: str):
    """
    Get all the upcoming gigs in the location provided. Store all this info as a JSON encoded string so that we don't
    need to re-query event info if the playlist is updated.
    :param location: The songkick metro area ID.
    """
    events = get_events_for_location(location_id=location)
    return json.dumps(events)


@app.callback(
    [Output("playlist-name", "children"),
     Output("user-tracks-graph", "figure"),
     Output("genre-tracks-graph", "figure"),
     Output("events-table", "columns"),
     Output("events-table", "data")],
    [Input("playlist-uri", "value"),
     Input("hidden-event-info", "children")])
def update_playlist(playlist_uri: str, event_json: str):
    """
    Update everything that depends on the content of the playlist.
    :param playlist_uri: The URI of the playlist to use.
    """
    playlist = SpotifyPlaylist(playlist_uri=playlist_uri, spotify_connection=sp)
    events = json.loads(event_json)
    event_table = create_events_table(playlist=playlist, event_list=events)
    columns = [{"name": header, "id": header} for header in event_table[0]]
    return playlist.name, \
        plot_sorted_tracks(playlist.tracks_by_user, title="Tracks added over time by each user"), \
        plot_sorted_tracks(playlist.tracks_by_genre, title="Number of tracks in different genres"), \
        columns, \
        event_table


if __name__ == "__main__":
    app.run_server(debug=True)

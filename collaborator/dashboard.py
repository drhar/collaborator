import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collaborator.playlist import SpotifyPlaylist, SpotifyArtist, SpotifyPlaylistTrack
from collaborator.graph_utils import plot_sorted_tracks


client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = html.Div(
    children=[
        html.Div(
            className="three columns div-left-panel",
            children=[
                # Div for Left Panel App Info
                html.Div(
                    className="div-info",
                    children=[
                        html.H6(
                            className="title-header", children="Playlist Dashboard"
                        ),
                        html.P(
                            """
                            This app gives you a graphical view of your playlist so you 
                            can improve it going forwards.
                            """
                        ),
                        html.Label("Spotify Playlist URI"),
                        dcc.Input(
                            id='playlist-uri',
                            value="spotify:playlist:1cIYJbMgyTsEfHtPVxWETv",
                            type='text'
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
            ],
        ),
    ],
)


@app.callback(
    [Output("user-tracks-graph", "figure"),
     Output("genre-tracks-graph", "figure")],
    [Input("playlist-uri", "value")])
def update_playlist(playlist_uri: str):
    playlist = SpotifyPlaylist(playlist_uri=playlist_uri, spotify_connection=sp)
    return plot_sorted_tracks(playlist.tracks_by_user, title="Tracks added over time by each user"), \
        plot_sorted_tracks(playlist.tracks_by_genre, title="Number of tracks in different genres")


if __name__ == "__main__":
    app.run_server(debug=True)

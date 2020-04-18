import dash
import dash_core_components as dcc
import dash_html_components as html
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collaborator.playlist import SpotifyPlaylist, SpotifyArtist, SpotifyPlaylistTrack
from collaborator.graph_utils import plot_sorted_tracks

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
PLAYLIST_URI = "spotify:playlist:1cIYJbMgyTsEfHtPVxWETv"


ddm = SpotifyPlaylist(playlist_uri=PLAYLIST_URI, spotify_connection=sp)


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
                    ],
                ),
            ],
        ),
        dcc.Graph(
            id="user-tracks-graph",
            figure=plot_sorted_tracks(
                ddm.tracks_by_user, title="Tracks added over time by each user"
            ),
        ),
        dcc.Graph(
            id="genre-tracks-graph",
            figure=plot_sorted_tracks(
                ddm.tracks_by_genre, title="Number of tracks in different genres"
            ),
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

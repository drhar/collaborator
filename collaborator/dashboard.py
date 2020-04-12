import dash
import dash_core_components as dcc
import dash_html_components as html
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collaborator.playlist import SpotifyPlaylist, SpotifyArtist, SpotifyPlaylistTrack
from collaborator.graph_utils import plot_sorted_tracks

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
PLAYLIST_URI = 'spotify:playlist:1cIYJbMgyTsEfHtPVxWETv'


ddm = SpotifyPlaylist(playlist_uri=PLAYLIST_URI, spotify_connection=sp)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Playlist Dashboard'),

    html.Div(children='''
        Visualisation to help plan your playlist.
    '''),

    dcc.Graph(
        id='user-tracks-graph',
        figure=plot_sorted_tracks(ddm.tracks_by_user, title="Tracks added over time by each user")
    ),
    dcc.Graph(
        id='genre-tracks-graph',
        figure=plot_sorted_tracks(ddm.tracks_by_genre, title="Number of tracks in different genres")
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
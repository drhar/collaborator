import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collaborator.playlist import SpotifyPlaylist, SpotifyArtist, SpotifyPlaylistTrack
from collaborator.graph_utils import plot_sorted_tracks
from collaborator.live_shows import search_songkick_locations, get_events_for_location

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
PLAYLIST_URI = "spotify:playlist:1cIYJbMgyTsEfHtPVxWETv"


ddm = SpotifyPlaylist(playlist_uri=PLAYLIST_URI, spotify_connection=sp)

metro_area = ""
location_results = search_songkick_locations("London")
for location in location_results:
    if location["city"]["country"]["displayName"] == "UK":
        metro_area = location["metroArea"]["id"]
        break

events = get_events_for_location(location_id=metro_area)

playlist_events = list()

for event in events:
    for artist in event.artists:
        for playlist_artist in ddm.artists.values():
            if artist.lower() == playlist_artist.name.lower():
                playlist_events.append(event)

playlist_events = set(playlist_events)

for event in playlist_events:
    print("{} is happening in London on {}.\n\n Artists: {}\n\n The show is {}\n\n\n".format(
        event.display_name, event.start.isoformat(), event.artists, event.status
    ))

print("There are {} songs in the playlist".format(len(ddm.tracks)))
print("There are {} artists in the playlist".format(len(ddm.tracks_by_artist)))
print(
    "The most popular artist is {}, with {} songs".format(
        ddm.artists[ddm.most_used_artist.uri].name,
        len(ddm.tracks_by_artist[ddm.most_used_artist.uri]),
    )
)

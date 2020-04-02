 1/1:
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
 2/1:
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
 2/2:
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('daniel harcombe')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
 2/3:
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('1110119342')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
 2/4: playlist = sp.playlist('1110119342')
 2/5: playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv')
 2/6: playlist
 2/7: dan_tracks = []
 2/8: huw_tracks = dez_tracks = ab_tracks = []
 2/9: huw_tracks.append(1)
2/10: dez_tracks
2/11: huw_tracks = []
2/12: denz_tracks = []
2/13: ab_tracks = []
2/14: user_ids = {}
2/15:
for track in playlist:
    if not track['added_by']['id'] in user_ids:
        user_ids[track['added_by']['id']] = []
2/16: playlist = sp.playlist_tracks('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv')
2/17: playlist
2/18:
for i, item in enumerate(playlist['items']):
    track = item['track']
    user = track['added_by']['id']
    if user not in user_ids:
        user_ids[user] = []
2/19: track
2/20: playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv')
2/21: tracks = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv', fields='tracks')
2/22: tracks
2/23: tracks = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv', fields='tracks,next')
2/24:
def find_who_added(tracks, user_dict):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        user = track['added_by']['id']
        if user not in user_dict:
            print("Adding user {} to dict".format(user))
            user_dict[user] = []
        user_dict[user].append(track)
2/25: find_who_added(tracks, user_ids)
2/26: tracks
2/27:
for item in tracks:
    print(item)
2/28:
for item in enumerate(tracks):
    print(item)
2/29:
for item in enumerate(tracks)['tracks']:
    print(item)
2/30:
for item in enumerate(tracks['tracks']):
    print(item)
2/31:
def find_who_added(tracks, user_dict):
    for i, item in enumerate(tracks['tracks']['items']):
        track = item['track']
        user = track['added_by']['id']
        if user not in user_dict:
            print("Adding user {} to dict".format(user))
            user_dict[user] = []
        user_dict[user].append(track)
2/32: find_who_added(tracks, user_ids)
2/33:
for item in enumerate(tracks['tracks']):
    print(item['track'])
2/34:
for item in enumerate(tracks['tracks']['items']):
    print(item['track'])
2/35:
for i, item in enumerate(tracks['tracks']['items']):
    print(item['track'])
2/36:
for i, item in enumerate(tracks['tracks']['items']):
    print(item)
2/37:
for i, item in enumerate(tracks['tracks']['items']):
    if i == 0:
        print(item)
2/38:
for i, item in enumerate(tracks['tracks']['items']):
    if i == 0:
        print(item['added_by'])
2/39:
for i, item in enumerate(tracks['tracks']['items']):
    if i == 0:
        print(item['added_by']['id'])
2/40:
def find_who_added(tracks, user_dict):
    for i, track_item in enumerate(tracks['tracks']['items']):
        track = track_item['track']
        user = track_item['added_by']['id']
        if user not in user_dict:
            print("Adding user {} to dict".format(user))
            user_dict[user] = []
        user_dict[user].append(track)
2/41: find_who_added(tracks, user_ids)
2/42:
for user in user_ids:
    print("User: {} has added {} songs".format(user, len(user_ids[user])))
2/43: tracks = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv', fields='tracks,next')
2/44: playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv', fields='tracks,next')
2/45: tracks = playlist['tracks']
2/46:
while playlist['next']:
    playlist = sp.next(playlist)
    tracks.extend(playlist['tracks'])
2/47: playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv')
2/48: tracks = playlist['tracks']
2/49:
while playlist['next']:
    playlist = sp.next(playlist)
    tracks.extend(playlist['tracks'])
2/50: playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv', fields='tracks,next')
2/51: playlist['next']
2/52: playlist
2/53: playlist['offset]
2/54: playlist['offset']
2/55: playlist[0]
2/56:
for key in playlist:
    print(key)
2/57: playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv', fields='tracks,next')
2/58: playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv')
2/59:
for key in playlist:
    print(key)
2/60: len(playlist['tracks'])
2/61: playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv', offset = 100)
2/62:
for key in tracks:
    print(key)
2/63:
while playlist['tracks']['next']:
    playlist = sp.next(playlist)
    tracks.extend(playlist['tracks'])
2/64: tracks
2/65: playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv', fields='tracks')
2/66: track_page = playlist['tracks']
2/67: tracks = track_page
2/68: tracks = deep_copy(track_page)
2/69: tracks = {}
2/70: tracks.extend track_page
2/71: tracks.extend(track_page)
2/72: tracks = []
2/73: tracks.extend(track_page)
2/74:
while track_page['next']:
    track_page = sp.next(track_page)
    tracks.extend(track_page)
2/75:
for key in tracks:
    print tracks
2/76:
for key in tracks:
    print(tracks)
2/77:
def find_who_added_tracks_from_page(tracks_page, user_dict):
    for i, track_item in enumerate(tracks['items']):
        track = track_item['track']
        user = track_item['added_by']['id']
        if user not in user_dict:
            print("Adding user {} to dict".format(user))
            user_dict[user] = []
        user_dict[user].append(track)
2/78: user_ids = {}
2/79:
for page in tracks:
    find_who_added_tracks_from_page(page, user_ids)
2/80:
for key in tracks[0]:
    print(key)
2/81: find_who_added_tracks_from_page(tracks, user_ids)
2/82: tracks
2/83: track_page
2/84: playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv', fields='tracks')
2/85: track_page = playlist['tracks']
2/86: find_who_added_tracks_from_page(track_page, user_ids)
2/87: track_page['items']
2/88: track_page['items']['added_by']
2/89: enumerate(track_page['items'])
2/90: i, item = enumerate(track_page['items'])
2/91: i, item = enumerate(track_page['items'])[0]
2/92:
def find_who_added_tracks_from_page(tracks_page, user_dict):
    for i, track_item in enumerate(track_page['items']):
        track = track_item['track']
        user = track_item['added_by']['id']
        if user not in user_dict:
            print("Adding user {} to dict".format(user))
            user_dict[user] = []
        user_dict[user].append(track)
2/93: playlist = sp.playlist('spotify:playlist:1cIYJbMgyTsEfHtPVxWETv', fields='tracks')
2/94: tracks
2/95: tracks['href']
2/96: track_page = playlist['tracks']
2/97: user_ids = {}
2/98: find_who_added_tracks_from_page(track_page, user_ids)
2/99:
while track_page['next']:
    track_page = sp.next[track_page]
    find_who_added_tracks_from_page
2/100:
while track_page['next']:
    track_page = sp.next(track_page)
    find_who_added_tracks_from_page(track_page, user_ids)
2/101:
for user in user_ids:
    print("User: {} added {} songs".format(user, len(user_ids[user])))
2/102: dan_tracks = user_ids['1110119342']
2/103: dan_tracks[0]
2/104: raveena = sp.artist('2kQnsbKnIiMahOetwlfcaS')
2/105: raveena
 3/1: %hist
 3/2: %history -g
   1: f = open("ipython_output.txt", "a")
   2: history = %history -g
   3: history
   4: f.close
   5: %hist -o -g -f ipython_history.md

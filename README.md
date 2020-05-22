# collaborator
Dashboard for collaborative playlists, breaking down what's been added and by who.

To run the dashboard you'll need a spotify api key and a songkick api key. These should be stored as environment variables on the machine used to run dashboard.py.
Spotify credentials can be created here: https://developer.spotify.com/dashboard/
Songkick API keys can only be attained by a slightly painful email exchange.

To set variables, run:

`export SPOTIPY_CLIENT_ID=<your_spotify_client_id>`

`SPOTIPY_CLIENT_SECRET=<your_spotify_client_secret>`

`SONGKICK_API_KEY=<your_songkick_api_key`

Then run `dashboard.py` from within a poetry shell to create the dashboard (will run locally). It will default to showing information for the playlist "Duw do music" with gig information in London, UK. These can be changed on the dashboard itself.

Install
-------
Install by cloning the repo and running `poetry install`

If using spotiplayoff, you may have to update SQLite in order to use Python. This is a bit of a pain but can be done by downloading the latest SQLite3 source from https://www.sqlite.org/download.html. Note that some of the following commands may need to be run using `sudo`:

`cd ~

wget https://www.sqlite.org/<YEAR>/sqlite-autoconf-<VERSION>.tar.gz

tar -zxvf sqlite-xxx.tar.gz

cd sqlite-xxx

./configure && make && make install

mv /usr/bin/sqlite3 /usr/bin/sqlite3.bak

mv xxx/sqlite3 /usr/bin/sqlite3

export LD_LIBRARY_PATH="/usr/local/lib"

export LD_RUN_PATH="/usr/local/lib"`

Make sure to make the two path alterations permanent by adding them to ~/.bashrc

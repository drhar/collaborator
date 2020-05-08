# collaborator
Dashboard for collaborative playlists, breaking down what's been added and by who.

To run the dashboard you'll need a spotify api key and a songkick api key. These should be stored as environment variables on the machine used to run dashboard.py.
Spotify credentials can be created here: https://developer.spotify.com/dashboard/
Songkick API keys can only be attained by a slightly painful email exchange.
To set variables, run:
`export SPOTIPY_CLIENT_ID=<your_spotify_client_id>`
`SPOTIPY_CLIENT_SECRET=<your_spotify_client_secret>`
`SONGKICK_API_KEY=<your_songkick_api_key`
Then run dashboard.py to create the dashboard (will run locally). It will default to showing information for the playlist "Duw do music" with gig information in London, UK. These can be changed on the dashboard itself.

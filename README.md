# twitter-spotify-bio
Script to show Spotify's "playing now" on Twitter bio.

# usage
1. Install selenium using pip
2. Install spotify using pip
3. Install dotenv using pip
4. Create an .env file on source folder and add the following values (alternatively, you can add them directly in your $PATH if you want to):
```
TWITTER_USERNAME="your_twitter_username"
TWITTER_PASSWORD="your_twitter_password"

SPOTIFY_CLIENT_ID="your_spotify_client_id"
SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
SPOTIFY_REDIRECT_URI="your_spotify_redirect_url"
SPOTIFY_SCOPE="user-read-currently-playing user-read-playback-state user-modify-playback-state user-library-read"
```

On the first time you run the script, your browser will open asking for Spotify authorization. Click on "Authorize" then copy the URL you have been redirected to and paste into the terminal. After that, a .cache file will be created and you will be authenticated with Spotify.

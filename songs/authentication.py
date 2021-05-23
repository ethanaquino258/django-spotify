import spotipy
import spotipy.util as util
import sys
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

def authCode(scope, username):
    load_dotenv()

    clientID = os.getenv('SPOTIFY_CLIENT_ID')
    clientSecret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_URI = os.getenv('REDIRECT_URI')
    
    # scope = "user-library-read user-read-recently-played user-top-read"

    # username = input("Enter username:")

    try:
        # token = util.prompt_for_user_token(
        #     username, scope, clientID, clientSecret, redirect_URI
        # )

        # sp = spotipy.Spotify(auth=token)

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri=redirect_URI, scope=scope, username=username))

    except spotipy.client.SpotifyException as e:
        print("====AUTH ERROR====")
        print(e)
        exit()
    return sp

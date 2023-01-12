"""
Backend for website
"""
import os
import datetime
from dotenv import load_dotenv
from flask import redirect,Flask, render_template, request
import spotipy
from spotipy import oauth2

load_dotenv()

app = Flask(__name__)


SPOTIPY_CLIENT_ID = client_id = os.environ.get('client_id')
SPOTIPY_CLIENT_SECRET = client_secret = os.environ.get('client_secret')
SCOPE = "user-library-read playlist-read-private playlist-modify-public user-library-modify user-read-email user-read-private"
# SPOTIPY_REDIRECT_URI = "https://turnstrat.onrender.com/login"
SPOTIPY_REDIRECT_URI = "https://angelaisthr-crispy-barnacle-rqv566r9wrx3pp6q-5000.preview.app.github.dev/login"

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE)

@app.route("/", methods=["GET"])
def home():
    """
    Homepage
    """
    auth_url = sp_oauth.get_authorize_url()
    return render_template("index.html", url=auth_url)

@app.route("/login", methods=["GET", "POST"])
def verify():
    """
    Logs the user in
    """
    code = request.args.get('code')
    if code:
        print ("Found Spotify auth code in Request URL! Trying to get valid access token...")
        try:
            token_info = sp_oauth.get_cached_token()
            print("\nCached", token_info)
            print("\n\n")
            access_token = token_info['access_token']
        except:
            token_info = sp_oauth.get_access_token(code)
            print("NEW",token_info)
            print("\n\n")
            access_token = token_info['access_token']
    if access_token:
        print ("Access token available! Trying to get user information...")
        class b():
            global spotify_object
            spotify_object = spotipy.Spotify(access_token)

    user_name = spotify_object.current_user()
    if user_name is None:
        return redirect("/")
    country = user_name["country"]
    username = user_name["display_name"]
    user_id = user_name["id"]
    profile = "https://open.spotify.com/user/" + user_id
    image = user_name["images"]
    image = image[0]
    image = image["url"]
    return render_template('home.html', country=country, username=username, profile=profile, id=user_id, image=image)


@app.route("/terms", methods=["GET"])
def terms():
    """
    Returns terms
    """
    return render_template("terms.html")

@app.route("/convert", methods=["GET", "POST"])
def convert():
    """
    Gets liked songs and puts it into a playlist
    """
    images = []
    url = []
    user_name = spotify_object.current_user()
    user_id = user_name["id"]
    current_date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    spotify_object.user_playlist_create(user_id, current_date)
    playlists = spotify_object.user_playlists(user_id)
    for playlist in playlists['items']:
        if playlist['name'] == current_date:
            playlist_id = playlist['id']
            print(playlist['id'])
            url.append("https://open.spotify.com/playlist/" + playlist['id'])
            img = spotify_object.playlist_cover_image(playlist['id'])
            print("IMAGE: ",img)
            print("\n\n")
            img = img[0]
            images.append(img['url'])
            print("Loading...")
            results = spotify_object.current_user_saved_tracks()
            show_tracks(results, playlist_id)

            while results['next']:
                print("Please wait ...")
                results = spotify_object.next(results)
                show_tracks(results, playlist_id)
    return render_template("works.html", playlistitems=playlists['items'], urls=url, images=images)

def show_tracks(results, playlist_name):
    """
    Logic for getting liked songs
    """

    for item in results['items']:
        track = item['track']
        # track_artist = (track['artists'][0]['name'])
        # track_link = (track['external_urls']['spotify'])
        # track_id = (track['id'])
        # track_preview_url = (track['preview_url'])
        # track_uri = (track['uri'])

        # WORKS ONLY IF THE uri IS A LIST!!!!!!
        spotify_object.playlist_add_items(playlist_name, [track['uri']])
        # ("%32.32s %s" % (track['artists'][0]['name'], track['name']))

# FROM https://github.com/spotipy-dev/spotipy/blob/master/examples/show_my_saved_tracks.py

@app.route("/playlists", methods=["GET", "POST"])
def playlist():
    stuff = []
    user_name = spotify_object.current_user()
    user_id = user_name["id"]
    playlists = spotify_object.user_playlists(user_id)
    for playlist in playlists['items']:
        img = spotify_object.playlist_cover_image(playlist['id'])
        if img == []:
            if request.method == "POST":
                img = "/static/no_image.gif"
            else:
                img = "/static/default.png"
        else:
            img = img[0]
            img = img['url']
        temp = {'url': "https://open.spotify.com/playlist/" + playlist['id'], 'name': playlist['name'], 'img': img}
        stuff.append(temp)
    return render_template("playlist.html", stuff=stuff)
if __name__ == "__main__":
    app.run()

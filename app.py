"""
Backend for website
"""
import os
import datetime
from dotenv import load_dotenv
from flask import redirect,Flask, render_template, request, url_for
import spotipy.util as util
import spotipy

load_dotenv()


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Returns homepage
    """
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs the user in
    """
    if request.method == "GET":
        return render_template("redirect.html")
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    scope = "user-library-read+playlist-read-private+playlist-modify-private+"
    scopes = "playlist-modify-public+user-library-modify+user-read-email+user-read-private"
    scope = scope + scopes
    redirect_uri = url_for('login', _external=True)
    print(redirect_uri)
    token = util.prompt_for_user_token(
                                        scope,
                                        client_id=client_id,
                                        client_secret=client_secret,
                                        redirect_uri=redirect_uri)
    spotify_object = spotipy.Spotify(auth=token)
    username = spotify_object.current_user()
    if username is None:
        return redirect("/")
    country = username["country"]
    username = username["display_name"]
    user_id = username["id"]
    profile = "https://open.spotify.com/user/" + id
    image = username["images"]
    image = image[0]

    image = image["url"]
    return render_template(
                        'home.html',
                        country=country,
                        username=username,
                        profile=profile,
                        id=user_id,
                        image=image)
@app.route("/convert", methods=["GET", "POST"])
def convert():
    """
    Gets liked songs and puts it into a playlist
    """
    if request.method == "GET":
        return render_template("redirect.html")
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    scope = "user-library-read+playlist-read-private+playlist-modify-private+"
    scopes="playlist-modify-public+user-library-modify+user-read-email+user-read-private"
    scope = scope + scopes
    redirect_uri = url_for('login', _external=True)
    token = util.prompt_for_user_token(
                                    scope,
                                    client_id=client_id,
                                    client_secret=client_secret,
                                    redirect_uri=redirect_uri)
    spotify_object = spotipy.Spotify(auth=token)

    current_date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    spotify_object.user_playlist_create(id, current_date)
    playlists = spotify_object.user_playlists(id)
    for playlist in playlists['items']:
        if playlist['name'] == current_date:
            playlist_id = playlist['id']
            print(playlist['id'])
            url = "https://open.spotify.com/playlist/" + playlist['id']
            print("Loading...")
            results = spotify_object.current_user_saved_tracks()
            show_tracks(results, playlist_id)

            while results['next']:
                print("Please wait ...")
                results = spotify_object.next(results)
                show_tracks(results, playlist_id)
    return render_template("works.html", playlistitems=playlists['items'], url=url)

def show_tracks(results, playlist):
    """
    Logic for getting liked songs
    """
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    scope = "user-library-read+playlist-read-private+playlist-modify-private+"
    scopes = "playlist-modify-public+user-library-modify+user-read-email+user-read-private"
    scope = scope + scopes
    redirect_uri = url_for('login', _external=True)
    token = util.prompt_for_user_token(
                                    scope,
                                    client_id=client_id,
                                    client_secret=client_secret,
                                    redirect_uri=redirect_uri)
    spotify_object = spotipy.Spotify(auth=token)

    for item in results['items']:
        track = item['track']
        # track_artist = (track['artists'][0]['name'])
        # track_link = (track['external_urls']['spotify'])
        # track_id = (track['id'])
        # track_preview_url = (track['preview_url'])
        # track_uri = (track['uri'])

        # WORKS ONLY IF THE uri IS A LIST!!!!!!
        spotify_object.playlist_add_items(playlist, [track['uri']])
        # ("%32.32s %s" % (track['artists'][0]['name'], track['name']))


# FROM https://github.com/spotipy-dev/spotipy/blob/master/examples/show_my_saved_tracks.py

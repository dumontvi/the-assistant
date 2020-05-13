import sys
import spotipy
import spotipy.util as util

scope = "app-remote-control streaming user-read-playback-position user-read-recently-played user-top-read user-modify-playback-state user-read-currently-playing user-read-playback-state"


if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token("223khjcz6yd4rrgxlsdcnegzy", scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results["items"]:
        track = item["track"]
        print(track["name"] + " - " + track["artists"][0]["name"])
        sp.start_playback(uris=["spotify:track:0AtP8EkGPn6SwxKDaUuXec"])
else:
    print("Can't get token for", username)

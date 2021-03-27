import requests
import json

BASE_URL = 'https://api.spotify.com/v1/'

# Track ID from the URI
track_id = '6y0igZArWVi6Iz0rj35c1Y'

def get_username(access_token):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    r = requests.get(BASE_URL + 'me/', headers=headers).json()
    return r['display_name']
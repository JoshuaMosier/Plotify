import requests
import json

BASE_URL = 'https://api.spotify.com/v1/'

def get_username(access_token):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    r = requests.get(BASE_URL + 'me/', headers=headers).json()
    return r['display_name']

def get_top_tracks(access_token):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    r = requests.get(BASE_URL + 'me/top/tracks?time_range=medium_term&limit=50&offset=0', headers=headers).json()
    track_names = []
    for item in r['items']:
        track_names.append(item['name'])
    return track_names

def get_top_artists(access_token):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    r = requests.get(BASE_URL + 'me/top/artists?time_range=medium_term&limit=50&offset=0', headers=headers).json()
    artists = []
    for item in r['items']:
        artists.append((item['name'],item['genres']))
    return artists
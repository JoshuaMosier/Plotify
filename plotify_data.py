import requests
import json
from collections import Counter
from itertools import chain

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
    genres = []
    for item in r['items']:
        artists.append((item['name'],item['genres']))
        genres.append(item['genres'])

    out = []
    counter = Counter(chain.from_iterable(map(set, genres)))
    idx = 0
    for name,amount in counter.most_common():
        out.append([idx,name,amount])
        idx = idx + 1
    return out
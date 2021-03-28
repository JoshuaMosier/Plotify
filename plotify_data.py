import requests
import json
from collections import Counter
from itertools import chain

BASE_URL = 'https://api.spotify.com/v1/'

def get_username(access_token):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    r = requests.get(BASE_URL + 'me/', headers=headers).json()
    return r['display_name'],r['images'][0]['url']

def get_top_tracks(access_token,term):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    r = requests.get(BASE_URL + 'me/top/tracks?time_range='+ term +'&limit=3&offset=0', headers=headers).json()
    track_names = []
    for item in r['items']:
        track_names.append([item['name'],item['popularity'],item['album']['images'][0]['url']])
    return track_names

def get_top_artists(access_token,term):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    r = requests.get(BASE_URL + 'me/top/artists?time_range='+ term +'&limit=3&offset=0', headers=headers).json()
    artist_names = []
    for item in r['items']:
        artist_names.append([item['name'],item['popularity'],item['images'][0]['url']])
    return artist_names

def get_top_genres(access_token):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    r = requests.get(BASE_URL + 'me/top/artists?time_range=medium_term&limit=50&offset=0', headers=headers).json()
    r_2 = requests.get(BASE_URL + 'me/top/artists?time_range=medium_term&limit=50&offset=50', headers=headers).json()
    artists = []
    genres = []
    for item in r['items']:
        artists.append((item['name'],item['genres']))
        genres.append(item['genres'])
    for item in r_2['items']:
        artists.append((item['name'],item['genres']))
        genres.append(item['genres'])

    out = []
    counter = Counter(chain.from_iterable(map(set, genres)))
    idx = 0
    for name,amount in counter.most_common():
        out.append([idx,name,amount])
        idx = idx + 1
    return out

def get_track_data(access_token,term):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    r = requests.get(BASE_URL + 'me/top/tracks?time_range='+ term +'&limit=50&offset=0', headers=headers).json()
    track_names = []

    # Plot release date vs genre?
    # Plot release date histogram
    # Plot length of song histogram
    # Pie chart of album/single/podcast
    ages = []
    for item in r['items']:
        ages.append(item['album']['release_date'][0:4])
    years,count = zip(*sorted(Counter(ages).items(), key=lambda pair: pair[0]))
    return years,count

def get_track_metrics(access_token,term):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    r = requests.get(BASE_URL + 'me/top/tracks?time_range='+ term +'&limit=50&offset=0', headers=headers).json()
    track_names = []
    for item in r['items']:
        ages.append(item['album'])
    
    return years,count
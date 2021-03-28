import requests
import json
from collections import Counter
from itertools import chain
from operator import *

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

def get_playlist_metrics(access_token):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    # Get all playlist ids
    r = requests.get(BASE_URL + 'me/playlists/?limit=50&offset=0', headers=headers).json()
    playlist_ids = []
    playlist_names = []
    for item in r['items']:
        playlist_ids.append(item['id'])
        playlist_names.append(item['name'])

    track_ids = []
    track_names = []
    track_pics = []
    play_data = [[] for i in range(6)]
    count = 0
    used_playlist_names = []
    for idx,playlist_id in enumerate(playlist_ids):
        r = requests.get(BASE_URL + 'playlists/'+playlist_id+'/tracks?market=US&fields=items(track(name%2Cid%2Calbum(images)))&limit=50&offset=0', headers=headers).json()
        for track in r['items']:
            track_ids.append(track['track']['id'])
            track_names.append(track['track']['name'])
            track_pics.append(track['track']['album']['images'][0]['url'])
            if count < 6 :
                play_data[count].append(track['track']['id'])
        if len(r['items']) > 2 and count < 6:
            used_playlist_names.append(playlist_names[idx])
            count = count + 1
    
    # Get data for radar plots
    delim = ','
    combined_metrics = [[] for i in range(6)]
    for idx,playlist in enumerate(play_data):
        tracks_string = delim.join(playlist)
        r = requests.get(BASE_URL + 'audio-features?ids=' + tracks_string, headers=headers).json()
        for item in r['audio_features']:
            combined_metrics[idx].append(item)
    
    # print(used_playlist_names)
    # print(combined_metrics[0])

    avgDict = {}
    rem_list = ['mode','type','id','uri','track_href','analysis_url','duration_ms','time_signature']
    # Get average metrics in list form for each playlist
    averaged = []
    for idx,plist in enumerate(combined_metrics):
        danceability = 0
        energy = 0
        speechiness = 0
        acousticness = 0
        instrumentalness = 0
        liveness = 0
        valence = 0
        for metric in plist:
            danceability = danceability + metric['danceability']
            energy = energy + metric['energy']
            speechiness = speechiness + metric['speechiness']
            acousticness = acousticness + metric['acousticness']
            instrumentalness = instrumentalness + metric['instrumentalness']
            liveness = liveness + metric['liveness']
            valence = valence + metric['valence']
        factors = [danceability,energy,speechiness,acousticness,instrumentalness,liveness,valence]
        averaged.append([x / len(metric) for x in factors])

    chunks = [track_ids[x:x+100] for x in range(0, len(track_ids), 100)]
    track_metrics = []
    for chunk in chunks:
        tracks_string = delim.join(chunk)
        r = requests.get(BASE_URL + 'audio-features?ids=' + tracks_string, headers=headers).json()
        for item in r['audio_features']:
            track_metrics.append(item['danceability'])
    # Create dictionary with track metrics and names
    metric_list = sorted(list(zip(track_names, track_metrics, track_pics)), key = lambda x: x[1],reverse=True)[:5]
    # print(metric_list)
    return metric_list,averaged,used_playlist_names
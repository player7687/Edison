from .models import SongUploadList, UserUploadHistory, GenreSongList
import requests
from .get_genre import get_genre
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Записываем в переменные:  
# cid = '48affa43619a4b6199626b726796affa' # client ID
# secret = '63e76ba496354043af79267956ad7f98' # client secret
# rur = 'http://127.0.0.1:8000/redirect/' # redirected URI
# scope = 'user-library-read' # допуск к возможностям API
# user = 'rxf62r2bta3ht0hlmica733vv' # имя пользователя

# https://accounts.spotify.com/en/login?continue=https%3A%2F%2Faccounts.spotify.com%2Fauthorize%3Fscope%3Duser-read-private%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fexample.com%252Fcallback%252F%26client_id%3Df80e2d622a82440dae2249dc056ffaa5%26show_dialog%3Dtrue
cid = 'f80e2d622a82440dae2249dc056ffaa5' # client ID
secret = 'b6292aef299a4082b031d271bd9b347c' # client secret
rur = 'http://51.250.96.17:8000/redirect/' # redirected URI
rur1 = 'https://example.com/callback/' # redirected URI
scope = 'user-library-read' # допуск к возможностям API
user = 'rxf62r2bta3ht0hlmica733vv' # имя пользователя

def saveSong(request, result, song = None, input_link = None):
    if result['result']:
        name_f = result['result']['title']
        artist_f = result['result']['artist']
        album_f = result['result']['album']
        print(result)
        duration_f = result['result']['spotify']['duration_ms']
        track_uri = result['result']['spotify']['uri']
        status_f = True
        cover_url = result['result']['spotify']['album']['images'][0]['url']

        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(cid, secret))

        track = sp.audio_features(track_uri)
        print(track)
        print(type(track))

        danceability_f = track[0]['danceability']
        energy_f = track[0]['energy']
        speechiness_f = track[0]['speechiness']
        acousticness_f = track[0]['acousticness']
        instrumentalness_f = track[0]['instrumentalness']
        valence_f = track[0]['valence']
        loudness_f = track[0]['loudness']
        tempo_f = track[0]['tempo']
        mode_f = track[0]['mode']

        cur_song = SongUploadList.objects.filter(name = name_f).filter(artist = artist_f)
        if not cur_song.exists():
            song_info = SongUploadList(name = name_f, artist = artist_f, album = album_f, duration = duration_f, status = status_f,
                danceability = danceability_f, energy = energy_f, speechiness = speechiness_f, acousticness = acousticness_f, instrumentalness = instrumentalness_f,
                loudness = loudness_f, valence = valence_f, tempo = tempo_f, mode = mode_f, song_uri = track_uri)
            song_info.get_image_from_url(cover_url)
            song_f = song_info.save()
            if input_link:
                genres = get_genre(input_link = input_link)
            else:
                genres = get_genre(song)
            for genre, pos in genres:
                genre_info = GenreSongList(song = song_f, genre = genre, probability = round(pos, 2))
                genre_info.save()
        else: 
            song_f = cur_song.get()
    else:
        name_f = 'N/A'
        artist_f = 'N/A'
        album_f = 'N/A'
        genre_f = 'N/A'
        status_f = False

        cur_song = SongUploadList.objects.filter(name = name_f).filter(artist = artist_f)
        if not cur_song.exists():
            song_info = SongUploadList(name = name_f, artist = artist_f, album = album_f, status = status_f)
            song_f = song_info.save()
            genre_info = GenreSongList(song = song_f, genre = genre_f)
            genre_info.save()
        else:
            song_f = cur_song.get()

    latest = UserUploadHistory.objects.filter(user = request.user).last()
    if latest is not None:
        order_f = latest.order + 1
    else:
        order_f = 1
    user_upload = UserUploadHistory(user = request.user, song = song_f, order = order_f)
    user_upload.save()

def uploadSong(request):
    input_link = request.POST.get('input-link')
    if input_link:
        data = {
            'url': input_link,
            'api_token': '5f3bde71a428f6f3e0a5e0ff578189d2',
            'return': 'apple_music,spotify',
        }
        result = requests.post('https://api.audd.io/', data=data).json()
        if result['result']:
            saveSong(request, result, input_link = input_link)

    songList = request.FILES.getlist('song')
    if songList:
        for song in songList:

            data = {
                'api_token': '5f3bde71a428f6f3e0a5e0ff578189d2',
                'return': 'apple_music,spotify',
            }
            files = {
                'file': song.open('rb'),
            }
            result = requests.post('https://api.audd.io/', data=data, files=files).json()
            print(result)
            saveSong(request, result, song)
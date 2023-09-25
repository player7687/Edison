from datetime import timedelta
from lib2to3.pgen2 import token
from os import access, stat
from tkinter.messagebox import NO
from urllib import response
from urllib.request import Request
from xmlrpc.client import ResponseError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from sklearn import semi_supervised
from .functions import uploadSong
from .forms import CreateUserForm
from .models import UserProfile, UserUploadHistory, SongUploadList, GenreSongList
from .decorators import unauthenticated_user
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

##New Libraries
from .functions import cid,rur,secret
from rest_framework.views import APIView
from requests import Request as req
from requests import post, put, get, delete
from rest_framework import status
from rest_framework.response import Response
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
##---------------------------------


import urllib
import lyricsgenius as lg
import json

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'main/home.html')

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user_f = form.save()
            sex_f = form.cleaned_data.get('sex')
            age_f = form.cleaned_data.get('age')
            u = UserProfile(user = user_f, sex = sex_f, age = age_f)
            u.save()
            return redirect('login')
    
    context = {'form': form}
    return render(request, 'main/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('history')
            
    context = {}
    return render(request, 'main/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def history(request):
    if 'upload_song' in request.POST:
        uploadSong(request)
    history_data = UserUploadHistory.objects.filter(user = request.user).order_by('-order').all()
    songs_genres = {}
    duration = {}
    for song in history_data:
        song_id = song.song.id
        songs_genres[song_id] = []
        song_genres = GenreSongList.objects.filter(song = song.song).all()
        for song_genre in song_genres:
            songs_genres[song_id].append(song_genre.genre)
            if song.song.duration is not None:
                m, s = divmod(round(song.song.duration/1000), 60)
                if s<10:
                    duration[song_id] = str(m) + ':0' + str(s)
                else:
                    duration[song_id] = str(m) + ':' + str(s)
    print(duration)
    context = {
        'song_data': history_data,
        'genres_data': songs_genres,
        'duration': duration
        }
    return render(request, 'main/history.html', context)

@login_required(login_url='login')
def settings(request):
    form = PasswordChangeForm(request.user)
    user = request.user
    dis_name = ''
    email = ''
    is_authenticated = is_spotify_authenticated(user)
    if is_authenticated:
        token = SpotifyToken.objects.filter(user=user).get()
        dis_name = token.user_dis_name
        email = token.user_email
    if 'upload_song' in request.POST:
        uploadSong(request)
    elif 'change_email' in request.POST:
        new_email = request.POST.get('new_email')
        user.email = new_email
        user.save()
    elif 'change_password' in request.POST:
        form = form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
    if request.GET.get('spotify_log_out'):
        SpotifyToken.objects.filter(user=user).delete()
        return redirect('history')
    context = {'form': form,
    'is_authenticated': is_authenticated,
    'dis_name': dis_name,
    'email': email}
    return render(request, 'main/settings.html', context)

@login_required(login_url='login')
def faq(request):
    if 'upload_song' in request.POST:
        uploadSong(request)
    return render(request, 'main/faq.html')

@login_required(login_url='login')
def detailsPage(request, id):
    if 'upload_song' in request.POST:
        uploadSong(request)
    
    song = get_object_or_404(SongUploadList, id = id)
    genius_access_token = 'd-6GwRdIdxOrWy5bhGbIOIH8Qun1lMBYW6uw5N27RPhUDyDk6M1Q7T638I0sAIJo'
    genius = lg.Genius(genius_access_token, verbose = False, skip_non_songs = True, excluded_terms = ['track listings'], retries = 5)
    song_g = genius.search_song(title=song.name, artist=song.artist)
    if song_g is not None:
        lyrics = song_g.lyrics
        lyrics = lyrics.split("\n",1)[1]
        lyrics = lyrics[:-5]
    else:
        lyrics = 'Oops... Lyrics not found.'

    song_genres = GenreSongList.objects.filter(song = song).all()

    genres = []
    probability = []

    for genre in song_genres:
        genres.append(genre.genre)
        probability.append(genre.probability)

    json_genres = json.dumps(genres)
    json_probability = json.dumps(probability)

    user = request.user

    is_authenticated = is_spotify_authenticated(user)
    is_saved = None

    if is_authenticated:
        song_id = song.song_uri.split(':', 2)[2]
        data = {'ids': [song_id]}
        token = get_user_tokens(user)
        is_saved = execute_spotify_api_request(token.token_type, token.access_token, '/tracks/contains', data)
        is_saved = is_saved[0]
        print(is_saved)

        if 'song_add' in request.POST:
            song_id = request.POST.get('song_add').split(':', 2)[2]
            data = {'ids': [song_id]}
            execute_spotify_api_request(token.token_type, token.access_token, '/tracks', data, put_=True)
            return redirect(request.path)
            
        if 'song_remove' in request.POST:
            song_id = request.POST.get('song_remove').split(':', 2)[2]
            data = {'ids': [song_id]}
            execute_spotify_api_request(token.token_type, token.access_token, '/tracks', data, delete_=True)
            return redirect(request.path)

    context = {
        "song": song,
        "genres": json_genres,
        "probability": json_probability,
        "lyrics": lyrics,
        "is_authenticated": is_authenticated,
        "is_saved": is_saved
    }

    return render(request, 'main/details.html', context)

##SPOTIFY AUTHORIZATION
class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'user-read-private user-read-email user-library-modify user-library-read'
            
        url = req('GET', 'https://accounts.spotify.com/en/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': rur,
            'client_id': cid,
            'show_dialog': 'true'
        }).prepare().url
            
        return Response({'url':url}, status=status.HTTP_200_OK)

@login_required(login_url='login')
def spotify_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': rur,
        'client_id': cid,
        'client_secret': secret,
    }).json()
    
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error1 = response.get('error')
    
    user = execute_spotify_api_request(token_type, access_token, '')

    user_dis_name = user['display_name']
    user_email = user['email']

    update_or_create_user_tokens(request.user, access_token, token_type, expires_in, refresh_token, user_dis_name, user_email)
    return redirect('history')

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.user)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)

def get_user_tokens(user):
    user_tokens = SpotifyToken.objects.filter(user=user)
    print(user_tokens)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

def update_or_create_user_tokens(user, access_token, token_type, expires_in, refresh_token, user_dis_name=None, user_email=None):
    tokens = get_user_tokens(user)
    print(expires_in)
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=user, access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type,
        user_dis_name=user_dis_name, user_email = user_email)
        tokens.save()
        
def is_spotify_authenticated(user):
    tokens = get_user_tokens(user)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(user)
        return True
    return False

def refresh_spotify_token(user):
    refresh_token = get_user_tokens(user).refresh_token
    
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': cid,
        'client_secret': secret
    }).json()
    
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = ""
    expires_in = response.get('expires_in')
    error1 = response.get('error')
    
    update_or_create_user_tokens(user, access_token, token_type, expires_in, refresh_token)

def execute_spotify_api_request(token_type, access_token, endpoint, data = {}, post_=False, put_=False, delete_=False):
    base_url = "https://api.spotify.com/v1/me"
    headers = {'Content-Type': 'application/json',
               'Authorization': token_type + ' ' + access_token}

    if post_:
        post(base_url + endpoint, headers=headers, data=data)
    if put_:
        put(base_url + endpoint, headers=headers, json=data)

    if delete_:
        delete(base_url + endpoint, headers=headers, json=data)


    response = get(base_url + endpoint, data, headers=headers)

    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}
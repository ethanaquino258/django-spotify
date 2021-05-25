from songs.authentication import authCode
from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from . import authentication
from .forms import termForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        request.session['username'] = request.POST.get('username')
        return render(request, 'songs/index.html', {'results': request.session['username']})
    else:
        return render(request, 'songs/index.html')

def topTracks(request):
    if request.method == 'POST':
        form = termForm(request.POST)
        if form.is_valid():
            client = authCode("user-top-read playlist-modify-public", request.session['username'])
            results = client.current_user_top_tracks(limit=50,time_range=request.POST.get('term_length'))
            tracks = results['items']
            return render(request, 'songs/topTracks.html', {'results': tracks})
    else:
        form = termForm()
    return render(request, 'songs/topTracks.html', {'form': form})

def recentlyPlayed(request):
    if request.method == 'POST':
        client = authCode("user-read-recently-played", request.session['username'])
        results = client.current_user_recently_played()
        recentResults = results['items']

        tracks = []
        for item in recentResults:
            tracks.append(item['track'])

        return render(request, 'songs/recentlyPlayed.html', {'results': tracks})
    else:
        return render(request, 'songs/recentlyPlayed.html')

def topArtists(request):
    if request.method == 'POST':
        form = termForm(request.POST)
        if form.is_valid():
            client = authCode("user-top-read playlist-modify-public", request.session['username'])
            results = client.current_user_top_artists(limit=50, time_range=request.POST.get('term_length'))
            artists = results['items']
            return render(request, 'songs/topArtists.html', {'results': artists})
    else:
        form = termForm()
    return render(request, 'songs/topArtists.html', {'form': form})


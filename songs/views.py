from songs.authentication import authCode
from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from . import authentication
from .forms import termForm

def embedifyer(url):
    cutUrl = url[8:]
    splitUrl = cutUrl.split('/')
    splitUrl.insert(0, 'https:/')
    splitUrl.insert(2, 'embed')
    embedUrl = '/'.join(splitUrl)

    return embedUrl

# Create your views here.
def index(request):
    # if request.method == 'POST':
    request.session['username'] = request.POST.get('username')
    return render(request, 'songs/index.html', {'results': request.session['username']})
    # else:
    #     return render(request, 'songs/index.html')

def topTracks(request):
    if request.method == 'POST':
        form = termForm(request.POST)
        if form.is_valid():
            client = authCode("user-top-read playlist-modify-public", request.session['username'])
            results = client.current_user_top_tracks(limit=50,time_range=request.POST.get('term_length'))
            tracks = results['items']

            trackResults = []
            for track in tracks:
                url = embedifyer(track['external_urls']['spotify'])

                trackItem = {'name': track['name'], 'embed': url}
                trackResults.append(trackItem)

            return render(request, 'songs/topTracks.html', {'results': trackResults})
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
            url = embedifyer(item['track']['external_urls']['spotify'])
            trackItem = {'name': item['track']['name'], 'embed': url}

            tracks.append(trackItem)

        return render(request, 'songs/recentlyPlayed.html', {'results': tracks})
    else:
        return render(request, 'songs/recentlyPlayed.html')

def topArtists(request):
    if request.method == 'POST':
        form = termForm(request.POST)
        if form.is_valid():
            client = authCode("user-top-read playlist-modify-public", request.session['username'])
            results = client.current_user_top_artists(limit=50, time_range=request.POST.get('term_length'))

            artists = []

            for artist in results['items']:
                url = embedifyer(artist['external_urls']['spotify'])
                artistItem = {'name': artist['name'], 'embed': url}

                artists.append(artistItem)

            return render(request, 'songs/topArtists.html', {'results': artists})
    else:
        form = termForm()
    return render(request, 'songs/topArtists.html', {'form': form})


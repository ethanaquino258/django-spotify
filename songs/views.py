from logging import error
from django.http.response import HttpResponseBadRequest
from songs.authentication import authCode
from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from . import authentication
from .forms import termForm
from .models import Artist, Song, Genre
from datetime import datetime, tzinfo
from django.utils import timezone
import pytz

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

def libraryRead(request):
    if request.method == 'POST':
        client = authCode("user-library-read", request.session['username'])
        results = client.current_user_saved_tracks()
        tracks = results['items']

        while results['next']:
            results = client.next(results)
            tracks.extend(results['items'])

        for item in tracks:
            timeAdded = item['added_at'][:-1]
            itemTime = datetime.strptime(timeAdded, "%Y-%m-%dT%H:%M:%S")

            # print(itemTime < mostRecent)
            # if itemTime < mostRecent:
            #     break

            trackObj = item['track']

            print(trackObj['name'])
            
            s, created = Song.objects.update_or_create(name = trackObj['name'], uri = trackObj['uri'], time_added = itemTime)

            for artist in trackObj['artists']:
                artistResult = client.artist(artist['id'])
                print(artist['name'])

                if artistResult['genres'] == []:
                    genreResult = ['no genre']
                else:
                    genreResult = artistResult['genres']

                a, created = Artist.objects.update_or_create(name = artist['name'], uri = artist['uri'])
                a.occurences += 1

                for genre in genreResult:
                    g, created = Genre.objects.update_or_create(name = genre)
                    g.occurences += 1
                    g.save()
                    a.genres.add(g)

                a.save()

                s.artists.add(a)

            s.save()

        return render(request, 'songs/libraryRead.html')
    else:
        return render(request, 'songs/libraryRead.html')
        


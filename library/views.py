from os import error

from django.http.response import HttpResponseBadRequest
from songs.authentication import authCode
from django.shortcuts import render
from .models import Artist, Song, Genre
from datetime import datetime
import pytz

# Create your views here.
def libraryIndex(request):
    request.session['username'] = request.POST.get('username')
    return render(request, 'library/libraryIndex.html', {'results': request.session['username']})

def libraryRead(request):
    client = authCode("user-library-read", request.session['username'])
    results = client.current_user_saved_tracks()
    tracks = results['items']

    utc = pytz.utc

    try:
        mostRecent = Song.objects.latest('time_added').time_added
    except Song.DoesNotExist:
        mostRecent = utc.localize(datetime.strptime("1970-01-01T00:0:00", "%Y-%m-%dT%H:%M:%S"))
    
    print(mostRecent)
    try:
        while results['next']:
            results = client.next(results)
            tracks.extend(results['items'])

        for item in tracks:
            timeAdded = item['added_at'][:-1]
            itemTime = utc.localize(datetime.strptime(timeAdded, "%Y-%m-%dT%H:%M:%S"))

            print(itemTime < mostRecent)
            if itemTime < mostRecent:
                break

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

        return render(request, 'library/libraryRead.html', {'results': Song.objects.all()[:100]})
    except:
        return HttpResponseBadRequest('Something went wrong!')

def topGenres(request):
    if len(Genre.objects.order_by('-occurences')[:50]) < 1:
        return HttpResponseBadRequest('ERROR: Load library first')
    else:
        return render(request, 'library/topGenres.html', {'results': Genre.objects.order_by('-occurences')[:50]})
    # try:
    #     return render(request, 'library/topGenres.html', {'results': Genre.objects.order_by('-occurences')[:50]})
    # except:
    #     return render(request, 'library/topGenres.html', {'error': 'error'})
        

def topArtists(request):
    if len(Artist.objects.order_by('-occurences')[:50]) < 1:
        return HttpResponseBadRequest('ERROR: Load library first')
    else:
        return render(request, 'library/topArtists.html', {'results': Artist.objects.order_by('-occurences')[:50]})
    # try:
    #     return render(request, 'library/topArtists.html', {'results': Artist.objects.order_by('-occurences')[:50]})
    # except:
    #     print("ERROR")
    #     return render(request, 'library/topArtists.html', {'error': 'error'})
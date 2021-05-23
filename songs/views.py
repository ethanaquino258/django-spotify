from songs.authentication import authCode
from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from . import authentication

# Create your views here.
def index(request):
    if request.method == 'POST':
        print("===============")
        print(request.POST.get('username'))
        client = authCode("user-top-read playlist-modify-public", request.POST.get('username'))
        results = client.current_user_top_tracks(limit=50,time_range="long_term")
        tracks = results['items']
        return render(request, 'songs/index.html', {'results': tracks})
    else:
        return render(request, 'songs/index.html')
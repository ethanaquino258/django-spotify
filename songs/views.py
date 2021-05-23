from songs.authentication import authCode
from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from . import authentication
from .forms import termForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = termForm(request.POST)
        if form.is_valid():
            client = authCode("user-top-read playlist-modify-public", request.POST.get('username'))
            print("============")
            print(request.POST.get('term_length'))
            results = client.current_user_top_tracks(limit=50,time_range=request.POST.get('term_length'))
            tracks = results['items']
            return render(request, 'songs/index.html', {'results': tracks})
    else:
        form = termForm()
    return render(request, 'songs/index.html', {'form': form})
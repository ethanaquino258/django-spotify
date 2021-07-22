from django.urls import path
from django.urls import path
from . import views

app_name='songs'
urlpatterns = [
    path('', views.index, name='index'),
    path('topTracks/', views.topTracks, name='topTracks'),
    path('recentlyPlayed/', views.recentlyPlayed, name='recentlyPlayed'),
    path('topArtists/', views.topArtists, name='topArtists'),
    path('libraryRead/', views.libraryRead, name='libraryRead'),
]
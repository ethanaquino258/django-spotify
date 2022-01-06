from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('', views.libraryIndex, name='libraryIndex'),
    path('libraryRead/', views.libraryRead, name='libraryRead'),
    path('genreRead/', views.genreRead, name='genreRead'),
    # path('topGenres/', views.topGenres, name='topGenres'),
    # path('topArtists/', views.topArtists, name='topArtists'),
]

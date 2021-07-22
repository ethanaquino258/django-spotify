from django.db import models

# Create your models here.
class Genre(models.Model):
    # id = models.IntegerField(db_index=True, primary_key=True)
    name = models.CharField(max_length=50)
    occurences = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Artist(models.Model):
    # id = models.IntegerField(db_index=True, primary_key=True)
    name = models.CharField(max_length=250)
    genres = models.ManyToManyField(Genre)
    occurences = models.IntegerField(default=0)
    uri = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Song(models.Model):
    # id = models.IntegerField(db_index=True, primary_key=True)
    name = models.CharField(max_length=250)
    artists = models.ManyToManyField(Artist)
    time_added = models.DateTimeField()
    uri = models.CharField(max_length=50)

    def __str__(self):
        return self.name
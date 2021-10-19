from django.db import models

from datetime import date

# Create your models here.

class Artists(models.Model):
    artist_id = models.CharField(max_length=200, primary_key=True)
    artist_name = models.CharField(max_length=200)
    artist_uri = models.TextField(default="", blank=True, null=True)
    artist_type = models.CharField(max_length=50, default="", blank=True, null=True)
    
class Album(models.Model):
    album_id = models.CharField(max_length=200, primary_key=True)
    album_name = models.CharField(max_length=200)
    album_uri = models.TextField(default="", blank=True, null=True)
    album_type = models.CharField(max_length=50, default="", blank=True, null=True)

class New_Releases(models.Model):
    album_id = models.ForeignKey(Album, related_name='albums', on_delete=models.CASCADE, blank=True, null=True)
    artist_id = models.ForeignKey(Artists, related_name='artists', on_delete=models.CASCADE, blank=True, null=True)
    release_date = models.DateField(default=date.today())
    
class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.TextField()
    access_token = models.TextField()
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)
 
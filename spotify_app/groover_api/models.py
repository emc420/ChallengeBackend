from django.db import models

from datetime import date

# Create your models here.

class Artists(models.Model):
    artist_id = models.CharField(max_length=200, primary_key=True)
    artist_followers = models.PositiveIntegerField(default=0)
    artist_genres = models.TextField(default="", blank=True, null=True)
    artist_name = models.CharField(max_length=200)
    artist_popularity = models.PositiveIntegerField(default=0)
    artist_uri = models.CharField(max_length=200)
    release_date = models.DateField(default=date.today())
    
class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.TextField()
    access_token = models.TextField()
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)
 
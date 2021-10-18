from rest_framework import serializers
from .models import Artists

class ArtistsSerializer(serializers.ModelSerializer):
    artist_id = serializers.CharField(max_length=200)
    artist_followers = serializers.IntegerField(required=False)
    artist_genres = serializers.CharField(required=False)
    artist_name = serializers.CharField(required=False, max_length=200)
    artist_popularity = serializers.IntegerField(required=False)
    artist_uri = serializers.CharField(required=False, max_length=200)
    release_date = serializers.DateField(required=False)
    
    class Meta:
        model = Artists
        fields = ('__all__')
from rest_framework import serializers
from .models import Artists, Album, New_Releases

class ArtistsSerializer(serializers.ModelSerializer):
    artist_id = serializers.CharField(max_length=200)
    artist_name = serializers.CharField(required=False, max_length=200)
    artist_uri = serializers.CharField(required=False)
    artist_type = serializers.CharField(required=False, max_length=50)
    
    class Meta:
        model = Artists
        fields = ('__all__')

class AlbumSerializer(serializers.ModelSerializer):
    album_id = serializers.CharField(max_length=200)
    album_name = serializers.CharField(required=False, max_length=200)
    album_uri = serializers.CharField(required=False)
    album_type = serializers.CharField(required=False, max_length=50)
    artists = ArtistsSerializer(many=True)
    
    class Meta:
        model = Album
        fields = ['album_id', 'album_name', 'album_uri', 'album_type', 'artists']

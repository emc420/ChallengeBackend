from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from rest_framework.decorators import api_view
from .serializers import ArtistsSerializer
from .models import Artists
from datetime import date
from .spotify_auth import SpotifyAuth
import math
import requests
import webbrowser
from requests import post, get, put

authObj = SpotifyAuth()

@api_view(['GET'])
def getArtists(request):
    session_id = request.session.session_key
    token = authObj.get_user_tokens(session_id)
    if not token:
        webbrowser.open(authObj.getUser())
        return
    elif not authObj.is_spotify_authenticated(session_id):
        authObj.refreshAuth(session_id)
        token = authObj.get_user_tokens(session_id)
    else:
        artists = Artists.objects.all()
        if not artists or artists[0].release_date!=date.today():
            if artists is not None:
                count = Artists.objects.all().delete()
            artists_new_releases = getNewReleasesFromSpotify(session_id)
            artist_serializer = ArtistsSerializer(data=artists_new_releases, many=True)
            if artist_serializer.is_valid():
                artist_serializer.save()
                return JsonResponse({"status": "success", "data": artist_serializer.data}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"status": "error", "data": artist_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        artist_serializer = ArtistsSerializer(artists, many=True)
        return JsonResponse(artist_serializer.data, safe=False) 

def getNewReleasesFromSpotify(session_id):
    offset = 0
    limit = 50
    artist_id_list= set()
    artistList = []
    while True :
        resp = authObj.get_new_releases(session_id, offset, limit)
        offset = offset+50
        for item in resp["albums"]["items"]:
            for artist in item["artists"]:
                artist_id_list.add(artist["id"])       
        if resp["albums"]["total"]<=offset+1 or resp["albums"]["next"] is None:
            break
    artist_id_list= list(artist_id_list)
    if len(artist_id_list)<=50:
        res = authObj.get_artists_new_releases_batch(session_id, artist_id_list)
        for row in res["artists"]:
            artist={}
            artist["artist_id"] = row["id"]
            artist["artist_followers"] = row["followers"]["total"]
            if len(row["genres"])!=0:
                artist["artist_genres"] = ",".join(row["genres"])
            else:
                artist["artist_genres"] = "None"
            artist["artist_name"] = row["name"]
            artist["artist_popularity"] = row["popularity"]
            artist["artist_uri"] = row["uri"]
            artistList.append(artist)                  
    else:
        res= []
        iterations = math.ceil(len(artist_id_list)/50)
        a=0
        b=50
        for i in range(iterations):
            if len(artist_id_list[a:])<50:
                res.append(authObj.get_artists_new_releases_batch(session_id, artist_id_list[a:]))
            else:
                res.append(authObj.get_artists_new_releases_batch(session_id, artist_id_list[a:b]))
            a=b
            b=b+50
        
        for row in res:
            for col in row["artists"]:
                artist={}
                artist["artist_id"] = col["id"]
                artist["artist_followers"] = col["followers"]["total"]
                if len(col["genres"])!=0:
                    artist["artist_genres"] = ",".join(col["genres"])
                else:
                    artist["artist_genres"] = "None"
                artist["artist_name"] = col["name"]
                artist["artist_popularity"] = col["popularity"]
                artist["artist_uri"] = col["uri"]
                artistList.append(artist)    
    return artistList

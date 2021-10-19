from django.shortcuts import render
from django.db import transaction

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from rest_framework.decorators import api_view
from .serializers import AlbumSerializer, ArtistsSerializer
from .models import Artists, Album, New_Releases
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
        webbrowser.open(authObj.getUser(), new=0)
        return JsonResponse({"status": "User Authorization required"}, status=status.HTTP_200_OK)
    elif authObj.is_spotify_authenticated(session_id):
        new_releases = New_Releases.objects.filter(release_date=date.today())
        if not new_releases:
            fetch_new_releases = getNewReleases(session_id)
            try:
                newList = anyNewAlbums(fetch_new_releases)
                if len(newList)==0:
                    return JsonResponse({"status": "No new releases for today"}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return JsonResponse(newList, status=status.HTTP_200_OK, safe=False) 
            except Exception as e:
                return JsonResponse({"error": str(e), "status": "Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False) 
            
        elif new_releases[0].album_id == "None":
            return JsonResponse({"status": "No new releases for today"}, status=status.HTTP_204_NO_CONTENT) 
        
        new_serial_obj = getSerializedObj(new_releases)
        
        return JsonResponse(new_serial_obj, safe=False) 
    else:
        return JsonResponse({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

def getSerializedObj(releases):
    distinct_list = releases.values('album_id').distinct()
    album_ser_List = []
    for track in distinct_list:
        album = Album.objects.filter(album_id = track["album_id"])
        artist_list = releases.values('artist_id').filter(album_id = track["album_id"])
        artists =  Artists.objects.filter(artist_id__in= artist_list)
        record ={}
        record["album_id"] = album[0].album_id
        record["album_name"] = album[0].album_name
        record["artist_uri"] = album[0].album_uri
        record["album_type"] = album[0].album_type
        record["artists"] = []
        for singer in artists:
            art ={}
            art["artist_id"] = singer.artist_id 
            art["artist_name"] =  singer.artist_name
            art["artist_uri"] = singer.artist_uri
            art["artist_type"] = singer.artist_type
            record["artists"].append(art)
        album_ser_List.append(record)
    return album_ser_List

def anyNewAlbums(fetch_new_releases):
    albumList = []
    newList = []
    new_releases = New_Releases.objects.all()
    for release in new_releases:
        albumList.append(release.album_id)
    for album in fetch_new_releases:
        if album["album_id"] not in albumList:
            newList.append(album)
            try:
                insertRecord(album)
            except Exception as e:
                print(Exception, e)
                raise Exception("Oops!", e.__class__, "occurred.")
    if len(newList) == 0:
        try:
            insertRecord()
        except Exception as e:
            raise Exception("Oops!", e.__class__, "occurred.")
    return newList
    
def insertRecord(album=None):
    if not album:
        new_rel = New_Releases(album_id=None, artist_id = None)
        new_rel.save()
    else:
        with transaction.atomic():
            albums = Album(album_id=album["album_id"], album_name=album["album_name"],
                                              album_uri=album["artist_uri"], album_type=album["album_type"])
            albums.save()
            for artist in album["artists"]:
                singer, created = Artists.objects.get_or_create(artist_id=artist["artist_id"], artist_name = artist["artist_name"],
                                        artist_uri = artist["artist_uri"], artist_type = artist["artist_type"])                                               
                new_rel = New_Releases(album_id=albums, artist_id = singer)
                new_rel.save()
    
 
def getNewReleases(session_id):
    offset = 0
    limit = 50
    albums = []
    while True :
        resp = authObj.get_new_releases(session_id, offset, limit)
        offset = offset+50
        for item in resp["albums"]["items"]:
            album = {}
            album["album_id"] = item["id"]
            album["album_name"] = item["name"]
            album["artist_uri"] = item["uri"]
            album["album_type"] = item["album_type"]
            album["artists"] = []
            for artist in item["artists"]:
                artists = {}
                artists["artist_id"] = artist["id"]    
                artists["artist_name"] =  artist["name"]   
                artists["artist_uri"] = artist["uri"]   
                artists["artist_type"] = artist["type"]   
                album["artists"].append(artists)
            albums.append(album)
        if resp["albums"]["total"]<=offset+1 or resp["albums"]["next"] is None:
            break        
    return albums
    
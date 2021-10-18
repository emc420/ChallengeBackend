from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from groover_api.spotify_auth import SpotifyAuth

authObj = SpotifyAuth()

def callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')
    response = authObj.getUserToken(code)
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    if not request.session.exists(request.session.session_key):
        request.session.create()
    authObj.update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)
    return redirect('../api/artists/')
    
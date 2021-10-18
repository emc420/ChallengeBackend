import base64, json, requests, os
from requests import post, get, put, Request
from django.utils import timezone
from datetime import timedelta
from .models import SpotifyToken


class SpotifyAuth(object):
    SPOTIFY_URL_AUTH = "https://accounts.spotify.com/authorize/"
    SPOTIFY_URL_TOKEN = "https://accounts.spotify.com/api/token/"
    RESPONSE_TYPE = "code"
    HEADER = "application/x-www-form-urlencoded"
    CLIENT_ID = 'e18d6952d6854b6c9ab1a161a013e6e3'
    CLIENT_SECRET = '7555b89676e34ac69a1c32c49b3dfef6'
    CALLBACK_URL = "http://localhost:5000/auth"
    SCOPE = "user-read-email user-read-private"
    BASE_URL = "https://api.spotify.com/v1/"

    def get_user_tokens(self, session_id):
        user_tokens = SpotifyToken.objects.filter(user=session_id)

        if user_tokens.exists():
            return user_tokens[0]
        else:
            return None
            
    def update_or_create_user_tokens(self, session_id, access_token, token_type, expires_in, refresh_token):
        tokens = self.get_user_tokens(session_id)
        expires_in = timezone.now() + timedelta(seconds=expires_in)

        if tokens:
            tokens.access_token = access_token
            tokens.refresh_token = refresh_token
            tokens.expires_in = expires_in
            tokens.token_type = token_type
            tokens.save(update_fields=['access_token',
                                       'refresh_token', 'expires_in', 'token_type'])
        else:
            tokens = SpotifyToken(user=session_id, access_token=access_token,
                                  refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
            tokens.save()   
    def is_spotify_authenticated(self, session_id):
        tokens = self.get_user_tokens(session_id)
        if tokens:
            expiry = tokens.expires_in
            if expiry <= timezone.now():
                self.refreshAuth(session_id)

            return True

        return False

            
    def getAuth(self, client_id, redirect_uri, scope):
        return (
                Request('GET', self.SPOTIFY_URL_AUTH, params={
                'scope': scope,
                'response_type': 'code',
                'redirect_uri': redirect_uri,
                'client_id': client_id
            }).prepare().url
        )

    def getToken(self, code, client_id, client_secret, redirect_uri):
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        encoded = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers = {
            "Content-Type": self.HEADER,
            "Authorization": f"Basic {encoded}",
        }

        post = requests.post(self.SPOTIFY_URL_TOKEN, params=body, headers=headers)
        return json.loads(post.text)


    def refreshAuth(self, session_id):
        refresh_token = get_user_tokens(session_id).refresh_token
        response = post(self.SPOTIFY_URL_TOKEN, data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': self.CLIENT_ID,
        'client_secret': self.CLIENT_SECRET
        }).json()
        access_token = response.get('access_token')
        token_type = response.get('token_type')
        expires_in = response.get('expires_in')

        self.update_or_create_user_tokens(
            session_id, access_token, token_type, expires_in, refresh_token)

    def getUser(self):
        return self.getAuth(
            self.CLIENT_ID, f"{self.CALLBACK_URL}/callback", self.SCOPE,
        )

    def getUserToken(self, code):
        return self.getToken(
            code, self.CLIENT_ID, self.CLIENT_SECRET, f"{self.CALLBACK_URL}/callback"
        )
    
    def execute_spotify_api_call(self, session_id, endpoint, post_=False, put_=False, other_base_url=None):
        tokens = self.get_user_tokens(session_id)
        if not tokens:
            return
        headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + tokens.access_token}

        url = self.BASE_URL if not other_base_url else other_base_url
        if post_:
            response = post(url + endpoint, headers=headers)
        elif put_:
            response = put(url + endpoint, headers=headers)
        else:
            response = get(url + endpoint, {}, headers=headers)

        # received empty object
        if not response.text:
            return response

        try:
            return response.json()
        except Exception as e:
            return {'Error': f"{e}"}
            
    
    def get_new_releases(self, session_id, offset=0, limit=50):
        return self.execute_spotify_api_call(session_id, f"browse/new-releases?&offset={offset}&limit={limit}")
    def get_artist_new_releases(self, session_id, id1):
        return self.execute_spotify_api_call(session_id, "artists/"+id1)
    def get_artists_new_releases_batch(self, session_id, ids):
        id1 = ",".join(ids)
        return self.execute_spotify_api_call(session_id, "artists/?ids="+id1)
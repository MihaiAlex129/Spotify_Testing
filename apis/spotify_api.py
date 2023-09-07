import requests
from secret_credentials import _CLIENT_SECRET, _CLIENT_ID


class SpotifyApi:
    _BASE_URL = "https://api.spotify.com/v1"
    _ALBUMS_ENDPOINT = "/albums"
    _ALBUMS_TRACKS_ENDPOINT = "/tracks"
    _ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"
    _CLIENT_ID=_CLIENT_ID
    _CLIENT_SECRET=_CLIENT_SECRET

    def get_album_route(self, album_id):
        return self._BASE_URL + self._ALBUMS_ENDPOINT + f"/{album_id}"

    def get_albums(self, album_id, access_token):
        URL = self.get_album_route(album_id)

        #alta varianta
        # URL = self._BASE_URL + self._ALBUMS_ENDPOINT + f"/{album_id}"
        # URL = self._BASE_URL + self._ALBUMS_ENDPOINT + "/4aawyAB9vmqN3uQ7FjRGTy"

        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }
        return requests.get(URL, headers=headers_token)

    def get_albums_tracks(self, album_id, access_token):
        URL = self.get_album_route(album_id) + self._ALBUMS_TRACKS_ENDPOINT
        # URL = self._BASE_URL + self._ALBUMS_ENDPOINT + f"/{album_id}" + self._ALBUMS_TRACKS_ENDPOINT

        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }
        return requests.get(URL, headers=headers_token)

    def get_access_token(self):
        URL = self._ACCESS_TOKEN_URL

        payload = f'grant_type=client_credentials&client_id={self._CLIENT_ID}&client_secret={self._CLIENT_SECRET}'
        headers_type = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        return requests.post(URL, headers=headers_type, data=payload)

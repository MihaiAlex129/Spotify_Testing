import unittest
from apis.spotify_api import SpotifyApi


class SpotifyTest(unittest.TestCase):
    accessToken = ''

    def setUp(self) -> None:
        self.spotify = SpotifyApi()
        if self.accessToken == '':
            self.accessToken = self.spotify.get_access_token().json()['access_token']

    def test_get_album_by_id_positive(self):
        response = self.spotify.get_albums("4aawyAB9vmqN3uQ7FjRGTy", access_token=self.accessToken)
        self.assertEqual(response.status_code, 200, "Status code is not the same")
        self.assertEqual(response.json()['name'], "Global Warming", "Name of the album is not the same")
        self.assertEqual(response.json()['artists'][0]['type'], "artist", "The artist index[0] is not the same")
        self.assertEqual(response.json()['tracks']['items'][0]['artists'][0]['name'], 'Pitbull',
                         "The artist name Pitbull is not correct")

    def test_get_album_by_id_non_positiv(self):
        response = self.spotify.get_albums("4aawyAB9vmqN3uQ7FjRGTy", access_token=self.accessToken)
        self.assertEqual(response.json()['tracks']['items'][0]['artists'][1]['type'], 'artist',
                         "The artist index[0][1] is not correct")

    def test_get_album_by_id_negative(self):
        response = self.spotify.get_albums("PYTA-TESTING", access_token=self.accessToken)
        self.assertEqual(response.status_code, 400, "Status code is not the same")
        self.assertEqual(response.json()['error']['message'], 'invalid id', "Error message is not the same")

import unittest
import secret_credentials
from apis.spotify_api import SpotifyApi


class SpotifyTest(unittest.TestCase):
    accessToken = ''

    def ms_to_s(self, value):
        new_val = value / 1000
        return new_val


    def setUp(self) -> None:
        self.spotify = SpotifyApi()
        if self.accessToken == '':
            self.accessToken = self.spotify.get_access_token().json()['access_token']

    def test_get_album_by_id_positive(self):
        response = self.spotify.get_albums(secret_credentials.album_id, access_token=self.accessToken)
        self.assertEqual(response.status_code, 200, "Status code is not the same")
        self.assertEqual(response.json()['name'], "Global Warming", "Name of the album is not the same")
        self.assertEqual(response.json()['artists'][0]['type'], "artist", "The artist index[0] is not the same")
        self.assertEqual(response.json()['tracks']['items'][0]['artists'][0]['name'], 'Pitbull',
                         "The artist name Pitbull is not correct")

    def test_get_album_by_id_non_positiv(self):
        response = self.spotify.get_albums(secret_credentials.album_id, access_token=self.accessToken)
        self.assertEqual(response.json()['tracks']['items'][0]['artists'][1]['type'], 'artist',
                         "The artist index[0][1] is not correct")

    def test_get_album_by_id_negative(self):
        response = self.spotify.get_albums("PYTA-TESTING", access_token=self.accessToken)
        self.assertEqual(response.status_code, 400, "Status code is not the same")
        self.assertEqual(response.json()['error']['message'], 'invalid id', "Error message is not the same")

    def test_track_lenght(self):
        response=self.spotify.get_albums_tracks(secret_credentials.album_id,access_token=self.accessToken)
        self.assertEqual(response.status_code, 200, "Status code is not the same")
        first_track_len_ms=response.json()['items'][0]['duration_ms']
        first_track_len= self.ms_to_s(first_track_len_ms)
        second_track_len_ms=response.json()['items'][1]['duration_ms']
        second_track_len= self.ms_to_s(second_track_len_ms)
        self.assertGreaterEqual(first_track_len,second_track_len,"first track is shorter than the second")
        self.assertLessEqual(first_track_len,second_track_len, "first track is longer than the second")


    def test_longest_track_lenght_shorter_than_5_minutes(self):
        response = self.spotify.get_albums_tracks(secret_credentials.album_id, access_token=self.accessToken)
        self.assertEqual(response.status_code, 200, "Status code is not the same222")

        tracks=response.json()['items']
        max_duration = 0
        track_name=None

        for track in tracks:
            track_duration_ms=track['duration_ms']
            if track_duration_ms>max_duration:
                max_duration=track_duration_ms
                track_name=track['name']

        max_duration_s=max_duration/60000               #CONVERTING MS TO MINUTES



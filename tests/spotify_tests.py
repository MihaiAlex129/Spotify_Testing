import unittest
from Spotify_Testing import secret_credentials
from Spotify_Testing.requests.spotify_api import SpotifyApi


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

    def test_get_album_by_id_non_positive(self):
        response = self.spotify.get_albums(secret_credentials.album_id, access_token=self.accessToken)
        self.assertEqual(response.json()['tracks']['items'][0]['artists'][1]['type'], 'artist',
                         "The artist index[0][1] is not correct")

    def test_get_album_by_id_negative(self):
        response = self.spotify.get_albums("PYTA-TESTING", access_token=self.accessToken)
        self.assertEqual(response.status_code, 400, "Status code is not the same")
        self.assertEqual(response.json()['error']['message'], 'invalid id', "Error message is not the same")

    def test_track_length(self):
        # RETURNS WHICH OF THE 2 FIRST SONGS IS LONGER
        response = self.spotify.get_albums_tracks(secret_credentials.album_id, access_token=self.accessToken)
        self.assertEqual(response.status_code, 200, "Status code is not the same")
        first_track_len_ms = response.json()['items'][0]['duration_ms']
        first_track_len = self.ms_to_s(first_track_len_ms)
        second_track_len_ms = response.json()['items'][1]['duration_ms']
        second_track_len = self.ms_to_s(second_track_len_ms)
        self.assertGreaterEqual(first_track_len, second_track_len, "first track is shorter than the second")
        self.assertLessEqual(first_track_len, second_track_len, "first track is longer than the second")

    def test_longest_track_length_shorter_than_6_minutes(self):
        # RETURNS
        response = self.spotify.get_albums_tracks(secret_credentials.album_id, access_token=self.accessToken)
        self.assertEqual(response.status_code, 200, "Status code is not the same")

        tracks = response.json()['items']
        max_duration = 0
        track_name = None

        for track in tracks:
            track_duration_ms = track['duration_ms']
            if track_duration_ms > max_duration:
                max_duration = track_duration_ms
                track_name = track['name']

        max_duration_s = max_duration / 60000  # CONVERT MS TO MINUTES

        self.assertLess(max_duration_s, 6, f"The track '{track_name}' duration is longer than 5 minutes")

    def test_every_song_is_played_by_artist(self):
        # Set artist_name to "Pitbull"
        artist_name = "Pitbull"

        # Get the tracks for the album
        tracks_response = self.spotify.get_albums_tracks(secret_credentials.album_id, access_token=self.accessToken)
        self.assertEqual(tracks_response.status_code, 200, "Status code is not the same")
        tracks_data = tracks_response.json()

        # Check if every song in the album is played by the artist "Pitbull"
        for track in tracks_data["items"]:
            # Retrieve the first artist's name (indexed by 0) from the "artists" list
            artist_on_track = track["artists"][0]["name"]

            # Compare the retrieved artist name with "Pitbull"
            self.assertEqual(artist_on_track, artist_name, f"Song not played by {artist_name}: {track['name']}")
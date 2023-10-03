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

    def test_get_album_by_id_non_positive(self):
        response = self.spotify.get_albums(secret_credentials.album_id, access_token=self.accessToken)
        self.assertEqual(response.json()['tracks']['items'][0]['artists'][1]['type'], 'artist',
                         "The artist index[0][1] is not correct")

    def test_get_album_by_id_negative(self):
        response = self.spotify.get_albums("PYTA-TESTING", access_token=self.accessToken)
        self.assertEqual(response.status_code, 400, "Status code is not the same")
        self.assertEqual(response.json()['error']['message'], 'invalid id', "Error message is not the same")

    def test_track_length(self):
        # Returns which of the 2 first songs is longer
        response = self.spotify.get_albums_tracks(secret_credentials.album_id, access_token=self.accessToken)
        self.assertEqual(response.status_code, 200, "Status code is not the same")
        # Store the values
        first_track_len_ms = response.json()['items'][0]['duration_ms']
        first_track_len = self.ms_to_s(first_track_len_ms)
        second_track_len_ms = response.json()['items'][1]['duration_ms']
        second_track_len = self.ms_to_s(second_track_len_ms)
        # Compare the values
        if first_track_len < second_track_len:
            r_msg = "first track is shorter than the second"
        elif first_track_len > second_track_len:
            r_msg = "first track is longer than the second"
        # r_msg value can be read as desired to check the result
        self.assertNotEqual(r_msg, 0, "invalid or equal track lengths")

    def test_longest_track_length_shorter_than_6_minutes(self):
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

        max_duration_s = max_duration / 60000  # Convert to minutes

        self.assertLess(max_duration_s, 6, f"The track '{track_name}' duration is longer than 5 minutes")

    def test_every_song_is_played_by_artist(self):

        artist_name = "Pitbull"

        tracks_response = self.spotify.get_albums_tracks(secret_credentials.album_id, access_token=self.accessToken)
        self.assertEqual(tracks_response.status_code, 200, "Status code is not the same")
        tracks_data = tracks_response.json()

        for track in tracks_data["items"]:
            artist_on_track = track["artists"][0]["name"]

            self.assertEqual(artist_on_track, artist_name, f"Song not played by {artist_name}: {track['name']}")

    def test_available_markets_list_contains_romanian(self):
        response = self.spotify.get_albums(secret_credentials.album_id, access_token=self.accessToken)
        self.assertEqual(response.status_code, 200, "Status code is not the same")
        self.assertIn("RO", container=response.json()["available_markets"], msg="Romanian language is not available")

        # Another way of doing this test is:

        # markets_list=response.json()["available_markets"]
        # for market in markets_list:
        #     if market=="RO":
        #         item_present=True
        # self.assertEqual(item_present, True, "Romanian language is not available")

    def test_second_album_contains_the_first_album_name(self):
        response = self.spotify.get_second_albums(secret_credentials.second_album_id, access_token=self.accessToken)
        self.assertEqual(response.status_code, 200, "Status code is not the same")
        self.assertIn("Global Warming", container=response.json()['name'], msg="Name of the album is not the same")

    def test_check_for_common_tracks(self):
        first_response = self.spotify.get_albums(secret_credentials.album_id, access_token=self.accessToken)
        second_response = self.spotify.get_second_albums(secret_credentials.second_album_id,
                                                         access_token=self.accessToken)
        self.assertEqual(first_response.status_code, 200, "Status code is not the same")
        self.assertEqual(second_response.status_code, 200, "Status code is not the same")

        first_list = []
        second_list = []

        # Populate first_list with track names from the first response
        for item in first_response.json()['tracks']['items']:
            track_name = item['name']
            first_list.append(track_name)

        # Populate second_list with track names from the second response
        for item in second_response.json()['tracks']['items']:
            track_name = item['name']
            second_list.append(track_name)

        # Convert both lists to sets and find the mutual elements (intersection)
        mutual_tracks = set(first_list).intersection(second_list)

        self.assertGreater(len(mutual_tracks), 0, "Common elements found between the two lists")

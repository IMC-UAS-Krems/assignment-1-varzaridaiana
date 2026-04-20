from streaming.albums import Album
from streaming.tracks import *
from streaming.artists import Artist


class TestAlbums:
    def test_album_fields(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        album = Album("alb1", "Album", artist=artist, release_year=2024)
        assert album.album_id == "alb1"
        assert album.title == "Album"
        assert album.artist is artist
        assert album.release_year == 2024

    def test_add_track_sets_album(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        album = Album("alb1", "Album", artist=artist, release_year=2024)
        track = AlbumTrack("t1", "Track", 120, "pop", artist, track_number=1)
        album.add_track(track)
        assert track.album is album

    def test_add_track_sorts_by_number(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        album = Album("alb1", "Album", artist=artist, release_year=2024)
        t1 = AlbumTrack("t1", "A", 120, "pop", artist, track_number=2)
        t2 = AlbumTrack("t2", "B", 120, "pop", artist, track_number=1)
        album.add_track(t1)
        album.add_track(t2)
        assert [t.track_id for t in album.tracks] == ["t2", "t1"]

    def test_track_ids(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        album = Album("alb1", "Album", artist=artist, release_year=2024)
        t1 = AlbumTrack("t1", "A", 120, "pop", artist, track_number=1)
        t2 = AlbumTrack("t2", "B", 120, "pop", artist, track_number=2)
        album.add_track(t1)
        album.add_track(t2)
        assert album.track_ids() == {"t1", "t2"}

    def test_duration_seconds_empty(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        album = Album("alb1", "Album", artist=artist, release_year=2024)
        assert album.duration_seconds() == 0

    def test_duration_seconds_sum(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        album = Album("alb1", "Album", artist=artist, release_year=2024)
        t1 = AlbumTrack("t1", "A", 120, "pop", artist, track_number=1)
        t2 = AlbumTrack("t2", "B", 200, "pop", artist, track_number=2)
        album.add_track(t1)
        album.add_track(t2)
        assert album.duration_seconds() == 320

    def test_add_track_keeps_track_numbers(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        album = Album("alb1", "Album", artist=artist, release_year=2024)
        t1 = AlbumTrack("t1", "A", 120, "pop", artist, track_number=3)
        album.add_track(t1)
        assert album.tracks[0].track_number == 3

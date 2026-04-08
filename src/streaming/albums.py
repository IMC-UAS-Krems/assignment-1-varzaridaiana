"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
class Album:
    def __init__(self, album_id: str, title: str, artist, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = []

    def add_track(self, track):
        track.album = self
        self.tracks.append(track)

    def track_ids(self) -> set[str]:
        return {t.track_id for t in self.tracks}

    def duration_seconds(self) -> int:
        return sum(t.duration_seconds for t in self.tracks)
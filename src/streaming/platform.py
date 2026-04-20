"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import datetime, timedelta
from collections import defaultdict
from .tracks import Song
from .users import PremiumUser, FamilyAccountUser, FamilyMember
from .playlists import Playlist, CollaborativePlaylist


class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self._catalogue = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = []

    def add_track(self, track):
        self._catalogue[track.track_id] = track

    def add_user(self, user):
        self._users[user.user_id] = user

    def add_artist(self, artist):
        self._artists[artist.artist_id] = artist

    def add_album(self, album):
        self._albums[album.album_id] = album

    def add_playlist(self, playlist):
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self._sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id):
        return self._catalogue.get(track_id)

    def get_user(self, user_id):
        return self._users.get(user_id)

    def get_artist(self, artist_id):
        return self._artists.get(artist_id)

    def get_album(self, album_id):
        return self._albums.get(album_id)

    def all_users(self):
        return list(self._users.values())

    def all_tracks(self):
        return list(self._catalogue.values())

    # Q1: Total listening time (in minutes) for a given period
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total = 0.0
        for s in self._sessions:
            if start <= s.timestamp <= end:
                total += s.duration_listened_seconds / 60
        return float(total)

    # Q2: Average number of unique tracks listened per PremiumUser
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        now = datetime.now()
        cutoff = now - timedelta(days=days)
        premiums = [u for u in self._users.values() if isinstance(u, PremiumUser)]
        if not premiums:
            return 0.0
        totals = []
        for u in premiums:
            tracks = {s.track.track_id for s in u.sessions if s.timestamp >= cutoff}
            totals.append(len(tracks))
        if not totals:
            return 0.0
        return sum(totals) / len(premiums)

    # Q3: Track with the most distinct listeners
    def track_with_most_distinct_listeners(self):
        if not self._sessions:
            return None
        listeners = defaultdict(set)
        for s in self._sessions:
            listeners[s.track.track_id].add(s.user.user_id)
        if not listeners:
            return None
        tops = max(listeners.items(), key=lambda x: len(x[1]))[0]
        return self._catalogue.get(tops)

    # Q4: Average session duration by user subtype
    def avg_session_duration_by_user_type(self):
        stats = defaultdict(list)
        for s in self._sessions:
            utype = type(s.user).__name__
            stats[utype].append(s.duration_listened_seconds)
        averages = []
        for k, v in stats.items():
            avg = sum(v) / len(v)
            averages.append((k, avg))
        averages.sort(key=lambda x: x[1], reverse=True)
        return averages

    # Q5: Total listening time of underage FamilyMember users
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total = 0.0
        for s in self._sessions:
            if isinstance(s.user, FamilyMember) and s.user.age < age_threshold:
                total += s.duration_listened_seconds / 60
        return float(total)

    # Q6: Top N artists by total listening time
    def top_artists_by_listening_time(self, n: int = 5):
        artist_time = defaultdict(float)
        for s in self._sessions:
            if isinstance(s.track, Song):
                artist = s.track.artist
                artist_time[artist] += s.duration_listened_seconds / 60
        ranking = sorted(artist_time.items(), key=lambda x: x[1], reverse=True)
        return ranking[:n]

 # Q7: User most-listened genre and its percentage
    def user_top_genre(self, user_id: str):
        user = self._users.get(user_id)
        if not user or not user.sessions:
            return None
        genre_time = defaultdict(float)
        total = 0
        for s in user.sessions:
            genre_time[s.track.genre] += s.duration_listened_seconds
            total += s.duration_listened_seconds
        if not total:
            return None
        top = max(genre_time.items(), key=lambda x: x[1])
        percentage = (top[1] / total) * 100
        return top[0], percentage

    # Q8: Collaborative playlists with more than “threshold” distinct artists
    def collaborative_playlists_with_many_artists(self, threshold: int = 3):
        found = []
        for p in self._playlists.values():
            if isinstance(p, CollaborativePlaylist):
                artists = {t.artist for t in p.tracks if isinstance(t, Song)}
                if len(artists) > threshold:
                    found.append(p)
        return found

    # Q9: Average track count for Playlist vs CollaborativePlaylist
    def avg_tracks_per_playlist_type(self):
        playlists = [p for p in self._playlists.values() if isinstance(p, Playlist)]
        collabs = [p for p in self._playlists.values() if isinstance(p, CollaborativePlaylist)]
        avg_playlists = sum(len(p.tracks) for p in playlists) / len(playlists) if playlists else 0.0
        avg_collabs = sum(len(p.tracks) for p in collabs) / len(collabs) if collabs else 0.0
        return {"Playlist": avg_playlists, "CollaborativePlaylist": avg_collabs}

    # Q10: Users who have listened to every track on an album
    def users_who_completed_albums(self):
        result = []
        for user in self._users.values():
            finished = []
            listened = {s.track.track_id for s in user.sessions}
            for album in self._albums.values():
                if album.tracks:
                    ids = {t.track_id for t in album.tracks}
                    if ids.issubset(listened):
                        finished.append(album.title)
            if finished:
                result.append((user, finished))
        return result


from spotify.config import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table


followers_table = Table(
    "followers", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    Column("artist_id", Integer, ForeignKey("artists.artist_id"), primary_key=True)
)

likes_table = Table(
    "likes", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    Column("track_id", Integer, ForeignKey("tracks.track_id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50))
    user_email = Column(String(50), unique=True)
    user_pass = Column(String)
    role = Column(String(10), default="user", nullable=False)

    followed_artists = relationship("Artist", secondary=followers_table, back_populates="followers")
    liked_tracks = relationship("Track", secondary=likes_table, back_populates="liked_by_user")


class Artist(Base):
    __tablename__ = "artists"
    artist_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    artist_name = Column(String(50))

    artist_to_album = relationship("Album", back_populates="album_to_artist")
    followers = relationship("User", secondary=followers_table, back_populates="followed_artists")


class Album(Base):
    __tablename__ = "albums"
    album_id = Column(Integer, primary_key=True, autoincrement=True)
    track_name = Column(String(200))
    artist_id = Column(Integer, ForeignKey("artists.artist_id"))

    album_to_artist = relationship("Artist", back_populates="artist_to_album")
    album_to_track = relationship("Track", back_populates="track_to_album")


class Track(Base):
    __tablename__ = "tracks"
    track_id = Column(Integer, primary_key=True, autoincrement=True)
    track_name = Column(String(200))
    album_id = Column(Integer, ForeignKey("albums.album_id"))

    track_to_album = relationship("Album", back_populates="album_to_track")
    liked_by_user = relationship("User", secondary=likes_table, back_populates="liked_tracks")

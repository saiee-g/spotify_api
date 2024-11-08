from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from spotify.config import get_db
from spotify.models import Artist

artist_router = APIRouter()

@artist_router.get("/artists/")
def get_artist_all(db:Session=Depends(get_db)):
    existing_artist = db.query(Artist).all()
    if not existing_artist:
        raise HTTPException(status_code=404, detail="No artist found")
    return existing_artist

@artist_router.get("/artists/{artist_name}/")
def get_artist(artist_name:str, db:Session=Depends(get_db)):
    existing_artist = db.query(Artist).filter(Artist.artist_name.ilike(f"%{artist_name}%")).all()
    if not existing_artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return existing_artist
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from spotify.config import get_db
from spotify.models import Album, Track

track_router = APIRouter()

@track_router.post("/tracks/")
def create_track(track_name:str, album_id:int, db: Session=Depends(get_db)):
    existing_track = db.query(Track).filter(Track.track_name == track_name and Track.album_id == album_id).first()
    if existing_track:
        raise HTTPException(status_code=400, detail="Track already exists")
    
    track = Track(track_name=track_name, album_id=album_id)
    db.add(track)
    db.commit()
    db.refresh(track)

@track_router.get("/tracks/")
def get_all_tracks(db:Session=Depends(get_db)):
    existing_track = db.query(Track).all()
    if not existing_track:
        raise HTTPException(status_code=404, detail="No track found")
    return existing_track


@track_router.get("/tracks/{track_name}/")
def get_track(track_name:str, db:Session=Depends(get_db)):
    existing_track = db.query(Track).filter(Track.track_name == track_name).all()
    if not existing_track:
        raise HTTPException(status_code=404, detail="Track not found")
    return existing_track


@track_router.put("/tracks/{track_id}/")
def update_track(track_id:int, track_name:str, album_id:int, db:Session=Depends(get_db)):
    track_to_update = db.query(Track).filter(Track.track_id == track_id).first()

    if not track_to_update:
        raise HTTPException(status_code=404, detail="Track does not exist")

    track_to_update.track_name = track_name
    track_to_update.album_id = album_id

    db.commit()
    db.refresh(track_to_update)
    return {"message": "Track information updated successfully"}

@track_router.delete("/tracks/{track_id}/")
def delete_track(track_id:int, db:Session=Depends(get_db)):
    track_to_delete = db.query(Track).filter(Track.track_id == track_id).first()

    if not track_to_delete:
        raise HTTPException(status_code=404, detail="Track does not exist")

    db.delete(track_to_delete)
    db.commit()

    return {"message": "Track deleted successfully"}
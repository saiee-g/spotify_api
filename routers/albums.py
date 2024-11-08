from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from spotify.config import get_db
from spotify.models import Album, Track, Artist
from spotify.dependencies import get_current_user, require_role

album_router = APIRouter()


@album_router.post("/albums/", dependencies=[Depends(require_role("artist"))])
def create_album(album_name:str, artist_id:int, user_id:int, db: Session=Depends(get_db), current_user: dict = Depends(get_current_user)):
    if int(current_user["user_id"]) != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to tamper another artist's album")
    existing_album = db.query(Album).filter(Album.album_name == album_name and Album.artist_id == artist_id and Artist.user_id == user_id).first()
    if existing_album:
        raise HTTPException(status_code=400, detail="Album already exists or you wrote wrong artist or user id")
    
    album = Album(album_name=album_name, artist_id=artist_id)
    db.add(album)
    db.commit()
    db.refresh(album)
    return {"message": "Album created successfully"}

@album_router.get("/albums/")
def get_all_albums(db:Session=Depends(get_db)):
    existing_album = db.query(Album).all()
    if not existing_album:
        raise HTTPException(status_code=404, detail="No album found")
    return existing_album


@album_router.get("/albums/{album_name}/")
def get_album(album_name:str, db:Session=Depends(get_db)):
    existing_album = db.query(Album).filter(Album.album_name.ilike(f"%{album_name}%")).all()
    if not existing_album:
        raise HTTPException(status_code=404, detail="Album not found")
    return existing_album


@album_router.put("/albums/{album_id}/", dependencies=[Depends(require_role("artist"))])
def update_album(album_id:int, album_name:str, artist_id:int, user_id:int, db:Session=Depends(get_db), current_user: dict = Depends(get_current_user)):
    if int(current_user["user_id"]) != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to tamper another artist's album")
    
    album_to_update = db.query(Album).filter(Album.album_id == album_id).first()

    if not album_to_update:
        raise HTTPException(status_code=404, detail="Album does not exist")

    album_to_update.album_name = album_name
    album_to_update.artist_id = artist_id

    db.commit()
    db.refresh(album_to_update)
    return {"message": "Album information updated successfully"}

@album_router.delete("/albums/{album_id}/", dependencies=[Depends(require_role("artist"))])
def delete_album(album_id:int, user_id:int, db:Session=Depends(get_db), current_user: dict = Depends(get_current_user)):
    
    if int(current_user["user_id"]) != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to upload another artist's album")
    album_to_delete = db.query(Album).filter(Album.album_id == album_id).first()

    if not album_to_delete:
        raise HTTPException(status_code=404, detail="Album does not exist")
    
    track_to_delete = db.query(Track).filter(Track.album_id == album_id).all()
    if track_to_delete:
        db.delete(track_to_delete)

    db.delete(album_to_delete)
    db.commit()

    return {"message": "Album deleted successfully"}
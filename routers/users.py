from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from spotify.config import get_db
from spotify.models import User, Artist
from passlib.hash import bcrypt

user_router = APIRouter()

@user_router.post("/register/")
def create_user(user_name:str, user_email:str, user_pass:str, role:str|None = None, db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.user_email == user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = bcrypt.hash(user_pass)
    user = User(user_name=user_name, user_email=user_email, user_pass=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)

    if role == "artist":
        artist = Artist(user_id=user.user_id, artist_name=user.user_name)
        db.add(artist)
        db.commit()
    return {"msg": "User registered successfully", "ID": user.user_id, "Name": user.user_name}


#@user_router.post("/login/")


@user_router.get("/users/{user_id}/")
def get_user(user_id:int, db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.user_id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return existing_user


@user_router.put("/users/{user_id}/")
def update_user(user_id:int, user_name:str, user_email:str, user_pass:str, role:str, db:Session=Depends(get_db)):
    user_to_update = db.query(User).filter(User.user_id == user_id).first()

    if not user_to_update:
        raise HTTPException(status_code=404, detail="User does not exist")

    hashed_password = bcrypt.hash(user_pass)

    user_to_update.user_name = user_name
    user_to_update.user_email = user_email
    user_to_update.role = role
    user_to_update.user_pass = hashed_password

    artist_to_update = db.query(Artist).filter(Artist.user_id == user_id).first()
    if artist_to_update:
        artist_to_update.artist_name = user_name

    db.commit()
    db.refresh(user_to_update)
    db.refresh(artist_to_update)
    return {"message": "User information updated successfully"}


@user_router.delete("/users/{user_id}/")
def delete_user(user_id:int, db:Session=Depends(get_db)):
    user_to_delete = db.query(User).filter(User.user_id == user_id).first()

    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User does not exist")
    
    artist_to_delete = db.query(Artist).filter(Artist.user_id == user_id).first()
    if artist_to_delete:
        db.delete(artist_to_delete)

    db.delete(user_to_delete)
    db.commit()

    return {"message": "User deleted successfully"}
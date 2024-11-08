from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from spotify.config import get_db
from spotify.models import User, Artist
from spotify.utils import verify_password, get_password_hash, create_access_token
from spotify.dependencies import get_current_user, require_role

user_router = APIRouter()


@user_router.post("/register/")
def create_user(user_name: str, user_email: str, user_pass: str, role: str = "user", db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.user_email == user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user_pass)
    user = User(user_name=user_name, user_email=user_email, user_pass=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)

    if role == "artist":
        artist = Artist(user_id=user.user_id, artist_name=user.user_name)
        db.add(artist)
        db.commit()
    return {"msg": "User registered successfully", "ID": user.user_id, "Name": user.user_name}


@user_router.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.user_pass):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": str(user.user_id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/users/{user_id}/")
def get_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    if int(current_user["user_id"]) != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this information")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return user


@user_router.put("/users/{user_id}/")
def update_user(user_id: int, user_name: str, user_email: str, user_pass: str, role: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if int(current_user["user_id"]) != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this information")
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    
    user.user_name = user_name
    user.user_email = user_email
    user.user_pass = get_password_hash(user_pass)
    user.role = role

    artist = db.query(Artist).filter(Artist.user_id == user_id).first()
    if artist:
        artist.artist_name = user_name

    db.commit()
    return {"message": "User information updated successfully"}


@user_router.delete("/users/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user:dict=Depends(get_current_user)):
    
    if int(current_user["user_id"]) != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this information")
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    artist = db.query(Artist).filter(Artist.user_id == user_id).first()
    if artist:
        db.delete(artist)
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

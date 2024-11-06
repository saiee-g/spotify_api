from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from spotify.config import get_db
from spotify.models import User, Artist, Album, Track

track_router = APIRouter()

@track_router.post("/tracks/")

@track_router.get("/tracks/")

@track_router.get("/tracks/{track_id}/")

@track_router.put("/tracks/{track_id}/")

@track_router.delete("tracks/{track_id}/")
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from spotify.config import get_db
from spotify.models import User, Artist, Album, Track

album_router = APIRouter()


@album_router.post("/albums/")

@album_router.get("/albums/")

@album_router.get("/albums/{album_id}/")

@album_router.put("/albums/{album_id}/")

@album_router.delete("albums/{album_id}/")
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from spotify.config import get_db
from spotify.models import User, Track, likes_table

like_router = APIRouter()

#Like a track
@like_router.post("/users/{user_id}/likes/{track_id}")
def like_track(user_id:int, track_id:int, db:Session=Depends(get_db)):
    existing_like = db.execute(
        likes_table.select().where(
            (likes_table.c.user_id == user_id) & 
            (likes_table.c.track_id == track_id)
        )
    ).fetchone()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="You already like this track")
    

    db.execute(
        likes_table.insert().values(user_id=user_id, track_id=track_id)
    )
    db.commit()
    return {"message": "You liked this track"}


#unlike a track
@like_router.delete("/users/{user_id}/unlike/{artist_id}/")
def unlike_track(user_id:int, track_id:int, db:Session=Depends(get_db)):
    existing_like = db.execute(
        likes_table.select().where(
            (likes_table.c.user_id == user_id) & 
            (likes_table.c.track_id == track_id)
        )
    ).fetchone()
    
    if not existing_like:
        raise HTTPException(status_code=400, detail="You don't like this track")

    db.execute(
        likes_table.delete().where(
            (likes_table.c.user_id == user_id) & 
            (likes_table.c.track_id == track_id)
        )
    )
    db.commit()
    return {"message": "You unliked this track"}

#get all liked tracks of user
@like_router.get("/users/{user_id}/liked-tracks/")
def liked_tracks(user_id:int, db:Session=Depends(get_db)):
    liked_list = db.execute(
        likes_table.select().where(
            (likes_table.c.user_id == user_id)
        )
    ).fetchall()

    if not liked_list:
        raise HTTPException(status_code=404, detail="No liked tracks yet")
    
    liked_json = [{"track_id": row.track_id} for row in liked_list]
    return liked_json
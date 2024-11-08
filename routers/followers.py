from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from spotify.config import get_db
from spotify.models import followers_table
from spotify.dependencies import get_current_user

follower_router = APIRouter()

#Follow an artist
@follower_router.post("/users/{user_id}/follow/{artist_id}/", dependencies=[Depends(get_current_user)])
def follow_artist(user_id:int, artist_id:int, db:Session=Depends(get_db), current_user: dict = Depends(get_current_user)):
    if int(current_user["user_id"]) != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this information")
    existing_follower = db.execute(
        followers_table.select().where(
            (followers_table.c.user_id == user_id) & 
            (followers_table.c.artist_id == artist_id)
        )
    ).fetchone()
    
    if existing_follower:
        raise HTTPException(status_code=400, detail="You already follow this artist")

    db.execute(
        followers_table.insert().values(user_id=user_id, artist_id=artist_id)
    )
    db.commit()
    return {"message": "You now follow this artist"}

#Unfollow an artist
@follower_router.delete("/users/{user_id}/unfollow/{artist_id}/", dependencies=[Depends(get_current_user)])
def unfollow_artist(user_id: int, artist_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if int(current_user["user_id"]) != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this information")
    existing_follower = db.execute(
        followers_table.select().where(
            (followers_table.c.user_id == user_id) & 
            (followers_table.c.artist_id == artist_id)
        )
    ).fetchone()
    
    if not existing_follower:
        raise HTTPException(status_code=400, detail="You don't follow this artist")

    db.execute(
        followers_table.delete().where(
            (followers_table.c.user_id == user_id) & 
            (followers_table.c.artist_id == artist_id)
        )
    )
    db.commit()
    return {"message": "You unfollowed this artist"}

#get all artists user follows
@follower_router.get("/users/{user_id}/following/", dependencies=[Depends(get_current_user)])
def following(user_id:int, db:Session=Depends(get_db), current_user: dict = Depends(get_current_user)):
    if int(current_user["user_id"]) != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this information")
    following_list = db.execute(
        followers_table.select().where(
            (followers_table.c.user_id == user_id)
        )
    ).fetchall()

    if not following_list:
        raise HTTPException(status_code=404, detail="You don't follow anyone yet")
    
    following_json = [{"artist_id": row.artist_id} for row in following_list]
    return following_json

from fastapi import FastAPI
from spotify.config import engine, Base
from spotify.routers.users import user_router
from spotify.routers.artists import artist_router
from spotify.routers.albums import album_router
from spotify.routers.tracks import track_router
from spotify.routers.followers import follower_router
from spotify.routers.likes import like_router

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
def home():
    return {"API name": "Spotiwy", "Message": "Welcome fellow listener!"}

app.include_router(user_router)
app.include_router(artist_router)
app.include_router(album_router)
app.include_router(track_router)
app.include_router(follower_router)
app.include_router(like_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
from fastapi import FastAPI
from spotify.config import engine, Base
from spotify.routers.users import user_router
from spotify.routers.artists import artist_router

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(user_router)
app.include_router(artist_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
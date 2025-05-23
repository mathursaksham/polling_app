from fastapi import FastAPI
from .routes import auth, poll
from .database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
app.include_router(poll.router, prefix="/polls")

@app.get("/")
def read_root():
    return {"message": "Polling App is running!"}

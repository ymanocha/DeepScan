from fastapi import FastAPI
from api import detect

app = FastAPI()

@app.get("/")
def root():
    return {"hello":"World"}

app.include_router(detect.router,prefix="/api")
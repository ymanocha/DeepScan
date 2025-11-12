from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api import detect, auth, scans

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/signup")
def serve_signup():
    return FileResponse("templates/signup.html")

@app.get("/dashboard")
def serve_signup():
    return FileResponse("templates/dashboard.html")

@app.get("/history")
def serve_signup():
    return FileResponse("templates/history.html")


@app.get("/loggedin")
def serve_signup():
    return FileResponse("templates/index_loggedin.html")

@app.get("/login")
def serve_signup():
    return FileResponse("templates/login.html")

@app.get("/")
async def root():
      return FileResponse("templates/index.html")
    
# @app.get("/protected")
# def protected_route(user: str = Depends(get_current_user)):
#     return {"msg": f"Hello, {user}"}

app.include_router(scans.router,prefix="/api")
app.include_router(detect.router,prefix="/api")
app.include_router(auth.router,prefix="/auth")
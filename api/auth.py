from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.base import sessionLocal
from models.user import User
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError

import os


router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["argon2"],deprecated="auto")



class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

def get_db():
    db = sessionLocal()
    try: 
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)): 
    name = payload.name
    email = payload.email
    password = payload.password
    print("Password received:", payload.password)
    existing = db.query(User).filter(User.email == email).first() 
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pw = pwd_context.hash(password)
    new_user = User(name=name, email=email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"message": "Signup Successful", "email":new_user.email}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    email = payload.email
    password = payload.password 
    user = db.query(User).filter(User.email ==  email).first()
    if not user or not pwd_context.verify(password, user.password): 
        raise HTTPException(status_code=401, detail="Invalid Exception")
    
    token = jwt.encode({"sub":user.email}, SECRET_KEY, algorithm=ALGORITHM) 
    return{"access_token": token, "token_type":"bearer"} 
      

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        
        db = sessionLocal()
        user = db.query(User).filter(User.email == email).first()
        db.close

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    


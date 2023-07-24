import model
from typing import Union, Annotated
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import FastAPI, Form, File, Request, Depends, HTTPException
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

class Bruh(BaseModel):
    hello: str

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/home")
def home():
    return {}

@app.post('/login')
async def login(
    username : Annotated[str, Form()],
    password : Annotated[str, Form()],
    db : Session = Depends(get_database_session),
):
    db_user = db.query(model.User).filter(model.User.username == username,model.User.password == password).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post('/register')
async def register( 
    username : Annotated[str, Form()],
    password : Annotated[str, Form()],
    db : Session = Depends(get_database_session)
):
    register = model.User(username = username, password = password)
    db.add(register)
    db.commit()
    
    return {}

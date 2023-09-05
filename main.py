import model
from typing import Union, Annotated
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import FastAPI, Form, File, Request, Depends, HTTPException
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

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
    loginjson = {"username" : username}
    return loginjson

@app.post('/register')
async def register( 
    fullname : Annotated[str, Form()],
    username : Annotated[str, Form()],
    password : Annotated[str, Form()],
    email : Annotated[str, Form()],
    phone : Annotated[int, Form()],

    db : Session = Depends(get_database_session)
):
    register = model.User(username = username, password = password, email = email, phone = phone , fullname = fullname)
    db.add(register)
    db.commit()
    registerjson = {"username" : username}

    return registerjson

@app.post('/add-books')
async def addbooks(
    username :Annotated[str, Form()],
    bookname : Annotated[str, Form()],
    rating :Annotated[str, Form()],
    status : Annotated[str, Form()],
    db : Session = Depends(get_database_session)
):
    book = model.Book(username = username, book_name = bookname,  rating = rating, status = status)
    db.add(book)
    db.commit()

    return {}

@app.post('/get-books')
async def getbooks(
    username : Annotated[str, Form()],
    db : Session = Depends(get_database_session)
):
    list = []
    books = db.query(model.Book).filter(model.Book.username == username).all()
    for i in books:
        list.append(i)
    if list is None:
        raise HTTPException(status_code=404, detail="User not found")
    return list

@app.post('/profile')
async def profile(
    username : Annotated[str, Form()],
    db : Session = Depends(get_database_session)
):
    db_user = db.query(model.User).filter(model.User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
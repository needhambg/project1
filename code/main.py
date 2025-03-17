from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from db_models import Base, Users, Posts
from api_models import BaseModel, UsersModel,PostsModel


#Start the Database Session
DATABASE_URL = "sqlite:///./social_media.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

#Factory For Generating Sessions
session_factory = sessionmaker(bind=engine)
#Create A Single Session
session = session_factory()

app = FastAPI()


#Get All Users
@app.get("/users/")
async def get_users():
    try:
        users = session.query(Users).filter().all()
        return users
    except:
        raise HTTPException(404, "Item not found")

#Get User By Name 
@app.get("/users/{username}")
async def get_user(username:str):
    try:
        userreq = session.query(Users).filter(Users.username == username).first()
        user = Users(**userreq)
        return user
    except:
        raise HTTPException(404, "Item Not Found")    

#Edit User (Patch)
#Update here

#Patch User - Admin Only
#@app.patch("/users/{id}") 
#async def update_user(name:str):
#    try:
#        results = session.query(Users).filter(Users).update({"name":name})
#        return results
#    except:
#        print

#Delete User

#Get All Posts
@app.get("/posts/")
async def get_posts():
    try:
        posts = session.query(Posts).filter().all()
        return posts
    except:
        raise HTTPException(404, "Item Not Found")

#Get User By Id
#@app.get("/users/{id}")
#async def get_user(id:int):
#    try:
#        userreq = session.query(Users).filter(Users.id == id).all()
#        return userreq
#    except:
#        raise HTTPException(404, "Item Not Found")

#Get Post By User
#@app.get("/posts/{user_id}")

#Patch Post - Like
#Update Here, Updating Posts Likes Value

#Patch Post - Dislike

#Edit Post (Put)

#Create User (Post)
#@app.post("/users/")

#Create Post (Post)
#@app.post("/posts/")

#def async create_post()
#Delete Post
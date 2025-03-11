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
#@app.get("/users/{username}")
#async def get_user(username:str):
#    try:
#        userreq = session.execute(select(Users).where(Users.username == username)).one()
#    except:
#        raise HTTPException(404, "Item Not Found")    
#    return userreq

#Edit User (Put)
#Update here

#Patch User - Admin Only

#Delete User

#Get All Posts
#@app.get("/posts/")

#Get User By Id
#@app.get("/users/{user_id}")

#Get Post By User
#@app.get("/posts/{user_id}")

#Patch Post - Like
#Update Here, Updating Posts Likes Value

#Patch Post - Dislike

#Edit Post (Put)

#Create User (Post)

#Create Post (Post)
#@app.post("/posts/")
#def async create_post()
#Delete Post

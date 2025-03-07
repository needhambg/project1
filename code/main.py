from fastapi import FastAPI, HTTPException

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from db_models import Base, Users, Posts
from api_models import BaseModel, UsersModel,PostsModel


#Start the Database Session
DATABASE_URL = "sqlite:///./social_media.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

#Factory For Generating Sessions
session_factory = sessionmaker(bind=engine)
#Create A Single Session
session = session_factory

app = FastAPI()

#Get All Users
@app.get("/users/{username}")
async def get_users(username:str):
    try:
        user = session.query(Users).filter(Users.username == username).one()
    except:
        raise HTTPException(404, "Item not found")
    return user
#Get User By Name 
#@app.get("/users/")
#Edit User (Put)

#Patch User - Admin Only

#Delete User

#Get All Posts

#Get User By Id

#Get Post By User

#Patch Post - Like

#Patch Post - Dislike

#Edit Post (Put)

#Create User (Post)

#Create Post (Post)

#Delete Post

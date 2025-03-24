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
        return userreq
    except:
        raise HTTPException(404, "Item Not Found")    

#Edit User (Patch)
#Update here
@app.patch("/users/{username}")
async def update_user(username:str, image_url:str):
    try:
        user = session.query(Users).filter(Users.username == username).first()
        user.image_url = image_url
        session.commit()
        return user
    except:
        raise HTTPException(404, "Item Not Found")

#Patch User - Admin Only
@app.patch("/users/{id}") 
async def update_user(name:str):
    try:
        results = session.query(Users).filter(Users).update({"name":name})
        return results
    except:
        print

#Delete User
@app.delete("/users/{id}")
async def delete_user(id:int):
    try:
        user = session.query(Users).filter(Users.id == id).first()
        session.delete(user)
        session.commit()
        return user
    except:
        raise HTTPException(404, "Item Not Found")
    
#Get All Posts
@app.get("/posts/")
async def get_posts():
    try:
        posts = session.query(Posts).filter().all()
        return posts
    except:
        raise HTTPException(404, "Item Not Found")

#Get User By Id
@app.get("/users/{id}")
async def get_user(id:int):
    try:
        userreq = session.query(Users).filter(Users.id == 1).all()
        return userreq
    except:
        raise HTTPException(404, "Item Not Found")

#Get Post By User
@app.get("/posts/{user_id}")
async def get_posts(user_id:int):
    try:
        posts = session.query(Posts).filter(Posts.user_id == user_id).all()
        return posts
    except:
        raise HTTPException(404, "Item Not Found")
    
#Patch Post - Like
@app.patch("posts/{id}/increment_likes")
async def incrementpostlikes(id:int):
    try:
        post = session.query(Posts).filter(Posts.id == id).first()
        post.likes += 1
        session.commit()
        return post
    except:
        raise HTTPException(404, "Item Not Found")
    
#Patch Post - Dislike
@app.patch("posts/{postId}/decrement_likes")
async def decrementpostlikes(id:int):
    try:
        post = session.query(Posts).filter(Posts.id == id).first()
        post.likes -= 1
        session.commit()
        return post
    except:
        raise HTTPException(404, "Item Not Found")
    
#Edit Post (Put) 
@app.put("/posts/{id}")
async def update_post(id:int, title:str, post_text:str):
    try:
        post = session.query(Posts).filter(Posts.id == id).first()
        post.title = title
        post.post_text = post_text
        session.commit()
        return post
    except:
        raise HTTPException(404, "Item Not Found")

#Create User (Post)
@app.post("/users/")
async def create_user(username:str, image_url:str):
    try:
        #if Users does not contain the username, create a new user
        if session.query(Users).filter(Users.username == username).first():
            raise HTTPException(409, "Item Already Exists")
        else:
            new_user = Users(username=username, image_url=image_url, is_admin=False)
            session.add(new_user)
            session.commit()
    except:
        raise HTTPException(500, "Error Creating User")
#Create Post (Post)
@app.post("/posts/")
async def create_post(id:int, user_id:str, title:str, post_text:str, likes:int):
    try:
        new_post = Posts(id, user_id, title, post_text, likes)
        session.add(new_post)
        session.commit()
    except:
        raise HTTPException(404, "Item Not Found")

#Delete Post
@app.delete("/posts/{id}")
async def delete_post(id:int):
    try:
        post = session.query(Posts).filter(Posts.id == id).first()
        session.delete(post)
        session.commit()
    except:
        raise HTTPException(404, "Item Not Found")
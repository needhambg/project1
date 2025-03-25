from fastapi import FastAPI, HTTPException

from sqlalchemy import create_engine
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
session = session_factory()

app = FastAPI()

## USERS ##

#Get User By Name 
@app.get("/users/")
async def get_user(name:str):
    try:
        if name:
            userreq = session.query(Users).filter(Users.username == name).all()
        else:
            userreq = session.query(Users).all()
        return userreq
    except:
        raise HTTPException(404, "Item Not Found")  

#Create User (Post)
@app.post("/users/")
async def create_user(user:UsersModel):
    username = user.username
    image_url = user.image_url
    try:
        #if Users does not contain the username, create a new user
        if session.query(Users).filter(Users.username == username).first():
            raise HTTPException(409, "Item Already Exists")
        else:
            new_user = Users(username=username, image_url=image_url, is_admin=False)
            session.add(new_user)
            session.commit()
            return new_user
    except:
        raise HTTPException(500, "Error Creating User")  

#Get User By Id
@app.get("/users/{userId}")
async def get_user(userId:int):
    try:
        userreq = session.query(Users).filter(Users.id == userId).first()
        return userreq
    except:
        raise HTTPException(404, "Item Not Found")

#Edit User (Put)
@app.put("/users/{userId}")
async def update_user(userId:int, user:UsersModel):
    try:
        if session.query(Users).filter(Users.id == userId).first():
            session.query(Users).filter(Users.id == userId).update({"username":user.username, "image_url":user.image_url, "is_admin":user.is_admin})
            session.commit()
    except:
        raise HTTPException(404, "Item Not Found")

#Patch User - Admin Only
@app.patch("/users/{id}/") 
async def update_user(name:str, userId:int, image_url:str):
    try:
        if session.query(Users).filter(Users.id == userId).first():
            if image_url:
                results = session.query(Users).filter(Users.id == userId).update({"image_url":image_url})
                session.commit()
            if name:
                results = session.query(Users).filter(Users.id == userId).update({"name":name})
                session.commit()
            return results
    except:
        raise HTTPException(404, "Item Not Found")

#Patch User Is Admin - Admin Only
@app.patch("/users/{id}/is_admin")
async def update_user(id:int, is_admin:bool):
    try:
        if session.query(Users).filter(Users.id == id).first():
            results = session.query(Users).filter(Users.id == id).update({"is_admin":is_admin})
            session.commit()
            return results
    except:
        raise HTTPException(404, "Item Not Found")
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
    
## POSTS ##

#Create Post (Post)
@app.post("/posts/")
async def create_post(post:PostsModel):
    user_id = post.user_id
    title = post.title
    post_text = post.post_text
    try:
        if session.query(Posts).filter((Posts.user_id == user_id) & (Posts.title == title)).first():
            raise HTTPException(409, "Item Already Exists")
        else:
            new_post = Posts(user_id=user_id, title=title, post_text=post_text, likes=0)
            session.add(new_post)
            session.commit()
            return new_post
    except:
        raise HTTPException(500, "Internal Server Error")
    
#Get All Posts
@app.get("/posts/")
async def get_posts():
    try:
        postsreq = session.query(Posts).filter().all()
        posts = []
        for val in postsreq:
            post = {"id":val.id, "user_id":val.user_id, "title":val.title, "post_text":val.post_text, "likes":val.likes}
            posts.append(post)
        return posts
    except:
        raise HTTPException(404, "Item Not Found")
    
#Get Post By Id
@app.get("/posts/{postId}")
async def get_post(postId:int):
    try:
        post = session.query(Posts).filter(Posts.id == postId).one()
        return post
    except:
        raise HTTPException(404, "Item Not Found")

#Get Posts By User
@app.get("/posts/user/{user_id}")
async def get_posts(user_id:int):
    try:
        posts = session.query(Posts).filter(Posts.user_id == user_id).all()
        return posts
    except:
        raise HTTPException(404, "Item Not Found")

#Update Post (Put) 
@app.put("/posts/{postId}")
async def update_post(postId:int, post:PostsModel):
    try:
        oldpost = session.query(Posts).filter(Posts.id == postId).first()
        oldpost.title = post.title
        oldpost.post_text = post.post_text
        session.commit()
        return
    except:
        raise HTTPException(404, "Item Not Found")
    
#Patch Post - Admin Only
@app.patch("/posts/{post_Id}/")
async def update_post(post_Id:int, title:str, post_text:str):
    try:
        if session.query(Posts).filter(Posts.id == post_Id).first():
            if title:
                results = session.query(Posts).filter(Posts.id == post_Id).update({"title":title})
                session.commit()
            if post_text:
                results = session.query(Posts).filter(Posts.id == post_Id).update({"post_text":post_text})
                session.commit()
            return results
    except:
        raise HTTPException(404, "Item Not Found")    

#Patch Post - Like
@app.patch("posts/{postId}/increment_likes")
async def updatelike(postId:int):
    try:
        post = session.query(Posts).filter(Posts.id == postId)
        post.likes = post.likes + 1
        session.commit()
        return post
    except:
        raise HTTPException(404, "Item Not Found")
    
#Patch Post - Dislike
@app.patch("posts/{postId}/decrement_likes")
async def updatelike(postId:int):
    try:
        post = session.query(Posts).filter(Posts.id == postId).first()
        post.likes = post.likes - 1
        session.commit()
        return post
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
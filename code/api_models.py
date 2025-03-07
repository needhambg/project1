from pydantic import BaseModel

class UsersModel(BaseModel):
    username:str
    image_url:str
    is_admin:bool
class PostsModel(BaseModel):
    user_id:int
    title:str
    post_text:str
    likes:int
    
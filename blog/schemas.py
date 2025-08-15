from typing import List
from pydantic import BaseModel

class Blog(BaseModel):
    title: str 
    body: str 

class ShowUser(BaseModel):
    name: str 
    email: str
    blogs: List[Blog] = []

class ShowBlog(BaseModel):
    title: str
    
    #for relationship
    creator: ShowUser

class User(BaseModel):
    name: str 
    email: str 
    password: str 
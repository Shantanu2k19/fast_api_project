from typing import List, Optional
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

class Login(BaseModel):
    email: str 
    password: str 

class Token(BaseModel):
    access_token: str 
    token_type: str

class TokenData(BaseModel):
    email: Optional[str]=None
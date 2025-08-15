from fastapi import FastAPI
from blog import models
from .database import engine
from blog.routers import blog, user

app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)
#Base.metadata is a container of table definitions for all models registered with that Base
#create_all(engine) Sends CREATE TABLE IF NOT EXISTS ... SQL commands to the database via the engine


@app.get('/', tags=['init'])
def hello_world():
    return {"message": "Hello world"}
from blog import schemas, models
from fastapi import status, HTTPException
from sqlalchemy.orm import Session


def fetch_all_logic(db: Session):
    return db.query(models.Blog).all()


def create_blog_logic(db:Session, request: schemas.Blog):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit() #saves the data to db from memory/session
    db.refresh(new_blog)  #reloads object from db with latest data
    return new_blog

#validates and shapes data into schema before returning 
#here the response will return in form of ShowBlog
def fetch_blog_with_id_logic(db:Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "messg": "blog not found"
        })
        # response_obj.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     "Message": "Blog not found"
        # }
    return blog


def delete_blog_logic(db:Session, id:int):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"mssg":"Blog not found"})
    
    db.delete(blog)
    db.commit()
    return {"mssg": "Delete success"}


def update_blog_logic(db:Session, id:int, request_obj: schemas.Blog):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    # blog = db.query(models.Blog).filter(models.Blog.id==id).update({'title':'Updated title'})
    # db.query(models.Blog).filter(models.Blog.id==id).update(request_obj)
    if blog:
        blog.title = request_obj.title
        blog.body = request_obj.body
        db.commit()
        return {"mssg": "updated"} 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"mssg": "Not found"})
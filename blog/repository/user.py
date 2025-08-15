from blog import schemas, models
from fastapi import status, HTTPException
from sqlalchemy.orm import Session

def create_user_logic(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=request.password)
    # new_user = models.User(**request.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

def fetch_user_logic(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"mssg":"user not found"})
    return user 

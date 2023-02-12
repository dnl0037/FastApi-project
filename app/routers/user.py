from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, esquemas, utils

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=esquemas.UserOut)
def create_user(user: esquemas.UserCreate, db: Session = Depends(get_db)):
    """registra usuario"""
    hashed_password = utils.hashing(user.password)
    user.password = hashed_password
    u = models.USER(**user.dict())
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=esquemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    u = db.query(models.USER).filter(models.USER.id == id).first()
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")
    return u

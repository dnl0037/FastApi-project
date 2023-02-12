from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db
from .. import models, esquemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=esquemas.Post)
def create_post(post: esquemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    """postea"""
    p = models.POST(owner_id=current_user.id, **post.dict())
    db.add(p)
    db.commit()
    db.refresh(p)  # p es un ORM model (de models.Post) No es diccionario
    # response_model es un pydantic model (de esquemas). (pydantic trabaja con diccionarios desempacados)
    # por esto, p no puede transformarse en responde_model así nomás
    # se necesita un cambio en los esquemas: ORM_MODE
    return p


@router.get("/", response_model=List[esquemas.PostVotes])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
              search: Optional[str] = ""):
    """devuelve todos los posts"""
    results = db.query(models.POST,
                       func.count(models.VOTE.post_id).
                       label("votes")). \
        join(models.VOTE, models.VOTE.post_id == models.POST.id, isouter=True). \
        group_by(models.POST.id)

    results1 = results.filter(models.POST.title.contains(search)).limit(limit).offset(skip).all()
    results2 = [u._asdict() for u in results1]
    return results2


@router.get("/{id}", response_model=esquemas.PostVotes)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    """devuelve un post"""
    p = db.query(models.POST, func.count(models.VOTE.post_id).label("votes")). \
        join(models.VOTE, models.VOTE.post_id == models.POST.id, isouter=True). \
        group_by(models.POST.id).filter(models.POST.id == id).first()
    if p is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    # if p.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    p = p._asdict()
    return p


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    """borra un post"""
    p_query = db.query(models.POST).filter(models.POST.id == id)
    post = p_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    p_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=esquemas.Post)
def update_post(id: int, post: esquemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    """modifica un post"""
    query = db.query(models.POST).filter(models.POST.id == id)
    p = query.first()
    if p is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    if p.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    return query.first()

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, esquemas, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: esquemas.Vote, db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.POST).filter(models.POST.id == vote.post_id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} does not exists")

    vote_query = db.query(models.VOTE).filter(models.VOTE.user_id == current_user.id,
                                              models.VOTE.post_id == vote.post_id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.VOTE(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if found_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}

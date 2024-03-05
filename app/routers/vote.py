from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import schemas,database,model,oauth2
from sqlalchemy.orm import Session



router = APIRouter(prefix="/votes",tags=['Vote'])

@router.post("",status_code=201)
def vote(vote: schemas.Vote,db: Session = Depends(database.get_db),current_user: int = Depends(oauth2.get_current_user)):


    #we query to see if the vote is already exist so that a user can't like a post more than once
    vote_query = db.query(model.Vote).filter(model.Vote.post_id == vote.post_id,model.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {vote.post_id} does not exist")#here we say if we could not find the post we return 404 error

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user{current_user.id} has already voted on post {vote.post_id}")
        new_vote = model.Vote(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added votes"}
    else:
        if not found_vote:  #if we user provides 0 we can raise that it is not voted before
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False) #here if we liked it before but wanna get our like back we can delete it by using this code
        db.commit()
        return {"message":"successfuly deleted vote"}
from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from .. import database , schemas, model , utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(tags=["Authentication"])
# just to note when we test the code below on postman instead of running it on Body-Row we have to run it on Body-form-data and there we plug in to the key USERNAME and to value its corresponding thing and for the password same
@router.post("/login",response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    
    # OAuth2PasswordRequestForm is gonna return our username and our password
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()  #so in this case .username corresponds to the email

    if not user:
        raise HTTPException(status_code=403,detail=f"invalid credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=403,detail=f"invalid credentials")
    
    #create token
    #return token

    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token":access_token,"token_type":"bearer"}   #so this will create token for the user we specified with ID above


    
    

    

    

    

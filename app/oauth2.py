from jose import JWTError , jwt
from datetime import datetime,timedelta
from . import schemas,database,model
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#We need SECRET KEY 
#we need to provide the algorithm we use
#we need to provide the expiration time of the token, how long should be the user logged in 

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes   #after one minute our token that we create expires so after 10 minute of its creation we cant use it

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):

    try:

        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        id_str = str(id) #as pydantic expects string in our datatoken model we convert it to string


        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id_str)
    
    except JWTError:
        raise credentials_exception
    
    return token_data  #it is basically the id that we return 
    
#the code below fetches the user from the database
def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):  #we pass this function as dependency to any of our path operation , it takes the token from the request automatcially extract the id for us , it is gonna verify if the token is correct by calling verify_access_token function and so it is gonna extract the id 
    credentials_exception = HTTPException(status_code=401,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})

    validated_token =  verify_access_token(token,credentials_exception)

    user = db.query(model.User).filter(model.User.id == int(validated_token.id)).first()

    return user


# to recap the last 2 functions we defined: any time any user that is required to be login we will expect them to provide an access token so in the file post the parameter ,get_current_user: int = Depends(oauth2.get_current_user) serves to this purpose
#and we created a dependency on this parameter so it will all the function get_current_user and there we passed in the token which is coming from the request, we gonna run the verify_access_token function this will verify if the token is ok if there is no error it wont return anything so it means they are authenticated, if we return error users will get 401 error

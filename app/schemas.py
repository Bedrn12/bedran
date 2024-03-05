from pydantic import BaseModel,EmailStr,conint #we use BaseModel for data validation #EmailStr for validating the email its alreadt installed in our fastapi if it was not pip install emaill-validator
from datetime import datetime
from typing import Optional

class Post(BaseModel):   #so this is for defining our schema/pydantic models so we specify what value our title should take string in this case such as 
    title:str
    content:str
    published: bool=True
    
    #rating: Optional[int] = None  #it is default to None if the user does not provide any value for rating

class create_post(Post):
    pass      #so here we created a different schema that we can use for creating post we inherited the same properties of the previous model (Post). we have to update the arguments to schemas.created_post where we create post on our main file but ı did not do it

class User_response(BaseModel):     # we define the schema of the response that the user gets   #here we created our scheme such that the user does not get his passowrd back in the response
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class respond_post(BaseModel): #so here we define the schema of our respond to the client while the previous ones were for setting the schema of request
    title: str
    content: str
    published: bool
    created_at: datetime     
    owner_id: int
    owner: User_response # User_response should be above our class so that this line of code can recognize it
    
    
    class Config:
        from_attributes = True   #tells Pydantic to allow ORM mode, which means the Pydantic model will behave more like an ORM model

class PostOut(BaseModel):
    
    Post:respond_post
    votes:int
    
    class Config:
        from_attributes = True 




#instead of writing all the columns we wanna respond to the user we can inherit from a base model and just pass into our new model the ones that does not have the columns in our base model like the following:
#for example we could structure respond_post like this:
"""class respond_post(Post):  #inherit the properties of Post model, it is useful when we have too many columns
    created_at: datetime"""

class UserCreate(BaseModel):  #we define the schema of our user input
    email: EmailStr
    password: str

class User_response(BaseModel):     # we define the schema of the response that the user gets   #here we created our scheme such that the user does not get his passowrd back in the response
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):  #where are creating a schema for users when they login 
    email: EmailStr
    password: str


class Token(BaseModel): #we are creating schema for the token that the user will provide
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None      #this is the data we embeed to our access token


class Vote(BaseModel):
    post_id: int
    dir:int = conint(ge=0,le=1)   #we set it either 0 or 1 where like represents 1 and 0 represents that user did not perform like 
    


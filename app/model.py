from .database import Base  #here we import base from the database file we created
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.sql.expression import null , text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import datetime
from sqlalchemy.orm import relationship

class Post(Base):   # here we define the columns of the table we gonna create at postgres  so sqlalchemy will create it if it sees that it does not exist on postgres
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='TRUE',nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False) # we set it as integer bcz it has to match with our users.id value, our foregin key is from users table id column so users.id, ondelete parameter is to specify that we want to delete the posts if user gets deleted that is associated with posts and nullable indicates it can not be empty      
# so with owner_id we creating relational database where the posts are associated with the users that creates them
    owner = relationship("User") #relationship function fetches the data of user automatticaly from the user model

class User(Base):
    __tablename__ = "users"     #we creating a table on postgres named users

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True) # we want the email in the string format, it can not be left empty so nullable is for this, and it should be unique email
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))      


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
#we created composite keys : that is primary key that spans multiple columns, it cares about that multiple columns whether they are the same or not at different rows(entries) it does not allow a user a to like a post more than once
    

class User(Base):
    __tablename__ = "newusers"
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,server_default=text('now()'))
    phone_number = Column(String)


class Nvotes(Base):
    __tablename__ = "newvotes"
    user_id = Column(Integer,nullable=False,primary_key=True)
    post_id = Column(Integer,nullable=False,primary_key=True)
    max_id = Column(Integer,nullable=False)





#some of the libraries we dont need(the gray ones) but ı kept them for documentation in the future

from fastapi import FastAPI , Response, HTTPException, Depends
from fastapi import Body
from pydantic import BaseModel  #we use BaseModel for data validation
from typing import Optional,List
from random import randrange
from psycopg2.extras import RealDictCursor # This allows you to access row values using column names as keys
import psycopg2
from . import model,schemas,utils  # we created the model file where we set the table
from .database import engine,SessionLocal, get_db   #this is the access to our database
from sqlalchemy.orm import Session
from .routers import post, user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware #this code is for enabling our program to communicate with different domains



#model.Base.metadata.create_all(bind=engine)    # so this enable us to create the table on postgres which we named as posts
#when we work with alembic we dont need this bcz alembic does the job





app = FastAPI()

origins = ["https://www.google.com","chrome://new-tab-page"] #this specifies what origins can talk with our api

app.add_middleware( #this code is for enabling our program to communicate with different domains
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#this code below helps us to break our code to seperate files
app.include_router(post.router)  #so what this code does is when we run our main file it goes to our post file and checks if anything matches with the HTTP request

app.include_router(user.router) # it does the same thing above goes to user file

app.include_router(auth.router)

app.include_router(vote.router)







"""#below we using sqlalchemy method to retrieve data from our database
@app.get("/sqlalchemy",response_model=list[schemas.respond_post]) # in this code block we create a schema for our response model Since you are fetching all posts from the database and returning them, you expect the response to be a list of posts
def test_posts(db: Session = Depends(get_db)): #every time we work with the database we have to pass in the things inside test_posts

    posts = db.query(model.Post).all()    #fetches all posts(entries) from the database (Post) using SQLalchemy query
    return posts

@app.post("/posts",status_code=201,response_model=schemas.respond_post) 
def create_posts(new_post: schemas.Post,db: Session = Depends(get_db)):   #we said schemas.post bcz we are importing from another file
   #newest_post = model.Post(title = new_post.title,content = new_post.content, published = new_post.published)
   newest_post = model.Post(**new_post.dict()) #this is more concise way to create object instead of writing like above so we can use this to unpack dictionary

   db.add(newest_post)   #adds the newly created post (newest_post) to the database session (db)
   db.commit()  #commits the transaction, saving the changes (i.e., inserting the new post) to the database.
   db.refresh(newest_post)
   return newest_post

@app.get("/posts/{id}",response_model=schemas.respond_post)  
def get_posts(id: int,db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()  # here we querying our database and return the first match that equalts to a value
    
    return post

@app.delete("/posts/{id}",status_code=204)#we dont use any response model bcz we already indicated a status code #above we defined a function to get the index and then we removed that index from our list array with the pop method
def delete_post(id:int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id)  #it queries the database to find the post with the given ID
    if post.first()  == None:
        raise HTTPException(status_code=404,detail=f"post with id:{id} does not exist")
    post.delete(synchronize_session=False)  #if the post exists, it deletes the post from database and with the code below it commits the transaction
    db.commit() 


@app.put("/posts/{id}",response_model=schemas.respond_post)  #this is for updating the data in the list(or database)
def update_post(id: int,post:schemas.Post,db: Session = Depends(get_db)):
    
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post_i = post_query.first()
    if post_i == None:
        raise HTTPException(status_code=404,detail=f"post with {id} does not exist")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()


#below we creating user
@app.post("/users",status_code=201,response_model=schemas.User_response) 
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):

    #hash the password - user.password
    hashed_password = utils.hash(user.password)  #we hashed the password
    user.password = hashed_password  # we saved our hashed password and saved to our database which is computationaly irreversible

    new_user = model.User(**user.dict()) 
    db.add(new_user)   
    db.commit()
    db.refresh(new_user)

    return new_user
 
#so with the code below we return user an ouput that does not contain password which makes sense

@app.get("/users/{id}",response_model=schemas.User_response)    
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404,detail=f"user with {id} not found")    
    
    return user"""



    
    



 #if we used psycopg driver to make it dynamic as well we could replace each with {settings.____} variables 
"""try:
    conn = psycopg2.connect(host = "localhost",dbname = "fastapi",user = "postgres",password = "Bedran123",cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was succesfull")
except Exception as error:
    print("database connection was failed")
    print("error:",error)"""


"""my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favorite foods","content":"I like pizza","id":2}]
#my_posts is a memory we create that would function sortta database but not database in fact for extracting updating etc.

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p"""

"""@app.get("/posts/{id}")   #when a user types in an id in path as parameter such as we go to our defined function find_post which checks if it exists in our list which works sortta database and return to the user 
def get_posts(id: int,response: Response):  #it checks if the id provided by the user is int if not it gives the user(front end) the error idnicating it is not integer    
    pos_t = find_post(int(id))
    if not pos_t:
        raise HTTPException(status_code = 404 ,detail=f'post with id: {id} was not found') #beside using the codes below we can import HTTPException and keep the code shorter
        
        #response.status_code = 404  # we imported Response and used status_code method when the post id typed in is not present in database so we give 404 error to indicate data is not there
        #return {"message":"id was not found"}
    return {"post detail": pos_t}"""

'''@app.get("/posts/{id}")  
def get_posts(id: int,response: Response): 
    cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))    # so here we retrieving from the postgres database the row with id = 1
    test_post = cursor.fetchone()
    print(test_post)
    return {"post detail": test_post}'''

   
    


@app.get("/")  #@app is our decorator ,  get is our http method , ("/") is our path url  
def root():  # that carries all the logic when get is requestd
    return {"message": "Hello Bedran, you k it"}

"""@app.get("/posts")#to go this url we have to port numb./posts  to make sure what method to use (whether get, put or smt else) we can check documentation
def get_posts():
    cursor.execute('''SELECT * FROM posts''')  #we passed in our sql statement and now we can call database
    posts = cursor.fetchall() #with this statement we retun all the rows that is retrieved by using the above statement
    print(posts)
    return {"data": posts}"""

# for getting posts if we retrieve all the posts we use it like above .get("/posts") but if we get one specific post .get("/posts/{id}") bcz every post has a unique id attached to it

# with HTTP get request we are getting data from API but with the HTTP post request we are giving data to the API to do whatever it has to do

# when we go to postman and type in smt to the body it will print out a result based on our following return statement
"""@app.post("/posts",status_code=201) #anytime sb creates post we have 201 created
def create_posts(new_post: Post):  #new_post parameter represent the data sent in the request body. the Post type indicates data should be validated and parsed according to the Post data model
    #print(new_post.title) print title attribute of the new_post object
    post_dict = new_post.dict()
    post_dict["id"] = randrange(1,1000)
    my_posts.append(post_dict)  # we store our new data in my_posts data array
    return (post_dict) """

'''@app.post("/posts",status_code=201) #anytime sb creates post we have 201 created
def create_posts(new_post: Post):  #new_post parameter represent the data sent in the request body. the Post type indicates data should be validated and parsed according to the Post data model
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(new_post.title,new_post.content,new_post.published))    
    newest_post = cursor.fetchone()  #so we return the new entry we make
    
    conn.commit()  #this is for commiting the database to finalize the changes on postgres and save it
    return {"data": newest_post}'''

"""def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] ==id:
            return i"""

"""@app.delete("/posts/{id}",status_code=204) #above we defined a function to get the index and then we removed that index from our list array with the pop method
def delete_post(id:int):
    #deleting post
    #find the index in the array that has required ID
    #my_posts.pop(index)
    index = find_index_post(id)
    my_posts.pop(index)
    return {"message":"post was successfully created"}"""

'''@app.delete("/posts/{id}",status_code=204) #above we defined a function to get the index and then we removed that index from our list array with the pop method
def delete_post(id:int):
    
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()'''
    


"""@app.put("/posts/{id}")  #this is for updating the data in the list(or database)
def update_post(id: int,post:Post):
    index = find_index_post(id)

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}"""

'''@app.put("/posts/{id}")  #this is for updating the data in the list(or database)
def update_post(id: int,post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content,post.published,str(id)))

    update_post = cursor.fetchone()
    conn.commit()'''







# to get to virtual environment on terminal   .\vens\Scripts\activate
# every time we change our code we are calling our server again so : uvicorn main:app --port 80**   (as we put main.py file into app package which we created we have to call it :  uvicorn app.main:app --port****)
# if we want our server to update itself without us needing to manually update just write : uvicorn main:app --reload --port 8080
# we can use postman to visualize and test our server
# we created a file named __init__.py inside the app folder(package) to make our folder function as a package

#all of our user operations dealing with users are gonna be in this file which is in the routers folder

from .. import model,schemas,utils  # in the main file we used one . this was because main was inside our app folder but here we use 2 . bcz we are in the routers folder so first we go to routers then to app folder
from fastapi import FastAPI , Response, HTTPException, Depends ,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
import psycopg2
from psycopg2.extras import RealDictCursor


router = APIRouter(prefix="/user",tags=['Users'])    # so this will function as @app which we were using before and so we changed app with router below in our codes
# in our code above tags parameter is for naming our fastapi documentation so we name it Users



#below we creating user
@router.post("",status_code=201,response_model=schemas.User_response) 
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

@router.get("/{id}",response_model=schemas.User_response)    
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404,detail=f"user with {id} not found")    
    
    return user



    
    



 
try:
    conn = psycopg2.connect(host = "localhost",dbname = "fastapi",user = "postgres",password = "Bedran123",cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was succesfull")
except Exception as error:
    print("database connection was failed")
    print("error:",error)


my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favorite foods","content":"I like pizza","id":2}]
#my_posts is a memory we create that would function sortta database but not database in fact for extracting updating etc.

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

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

   
    



@router.get("/")  #@app is our decorator ,  get is our http method , ("/") is our path url  
def root():  # that carries all the logic when get is requestd
    return {"message": "Hello Bedran, you k it"}

@router.get("/posts")#to go this url we have to port numb./posts  to make sure what method to use (whether get, put or smt else) we can check documentation
def get_posts():
    cursor.execute("""SELECT * FROM posts""")  #we passed in our sql statement and now we can call database
    posts = cursor.fetchall() #with this statement we retun all the rows that is retrieved by using the above statement
    print(posts)
    return {"data": posts}
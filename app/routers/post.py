#all of our post operations dealing with posts are gonna be in this file which is in the routers folder

from .. import model,schemas  # in the main file we used one . this was because main was inside our app folder but here we use 2 . bcz we are in the routers folder so first we go to routers then to app folder
from fastapi import FastAPI , Response, HTTPException, Depends ,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional,List
from .. import oauth2
from sqlalchemy import func #this gives us access to functions like count,sum that we use in postgres sql


router = APIRouter(prefix="/posts",tags=['Posts'])   #so this puts the posts path to our url as default then if we plug in id below our code to our url path it will still be there
# in our code above tags parameter is for naming our fastapi documentation so we name it Posts


#below we using sqlalchemy method to retrieve data from our database
@router.get("/sqlalchemy",response_model=list[schemas.respond_post]) # in this code block we create a schema for our response model Since you are fetching all posts from the database and returning them, you expect the response to be a list of posts
def test_posts(db: Session = Depends(get_db)): #every time we work with the database we have to pass in the things inside test_posts

    posts = db.query(model.Post).all()    #fetches all posts(entries) from the database (Post) using SQLalchemy query
    return posts

@router.post("",status_code=201,response_model=schemas.respond_post) 
def create_posts(new_post: schemas.Post,db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):   #we said schemas.post bcz we are importing from another file
   #newest_post = model.Post(title = new_post.title,content = new_post.content, published = new_post.published) 
   newest_post = model.Post(owner_id =get_current_user.id ,**new_post.dict()) #this is more concise way to create object instead of writing like above so we can use this to unpack dictionary
#when we create a post we created a schema where the user receives a response that indicates the owner_id so to associate user with the post we coded owner_id =get_current_user.id

#we created dependency by using  oauth2.get_current_user  this would check if the user is logged in to let him post smt
   #on postman we go to headers choose authorization for key and pass in "Bearer <token>" to the value 
   print(get_current_user)
   db.add(newest_post)   #adds the newly created post (newest_post) to the database session (db)
   db.commit()  #commits the transaction, saving the changes (i.e., inserting the new post) to the database.
   db.refresh(newest_post) #ensure that the object reflects any changes made to it during the database transaction before returning it from the function
   return newest_post

#@router.get("",response_model=List[schemas.respond_post])#to go this url we have to port numb./posts  to make sure what method to use (whether get, put or smt else) we can check documentation
@router.get("",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: dict = Depends(oauth2.get_current_user),limit: int = 10,skip: int = 0,search: Optional[str] = ""): #just to note for general we specified a type hint which is dict but it has no impact our code in general it is just a note
    #above we defined a query parameter limit and assigned it a default value 10 , so it means in default it will return 10 posts
    #but if user set value for limit to the query parameter (just a note: URL consists of three parts: the IP which is the domain name like facebook then search? then the rest is query parameters )
    #if in the query parameter user types in http://127.0.0.1:8020/posts?limit=3  it will receive 3 posts
    
    #we used skip which is for skipping some posts that we would call in limited number for that we use function offset 
    #when we type in many query parameters we can use &  so http://127.0.0.1:8020/posts?limit=3&skip=2  for example

    #we used search query parameter such that user can type in the keyword it searchs for and retrieves the ones that contain this keyword
    #the contains function below serves to that purpose by checking if the keyword provided in the url is present somewhere in the title (btw it does not need to match , as long as it contains it is enough)
    #we kept it optional so it is okay if user does not provide anything
    #the path would be like that : {{URL}}/posts?limit=3&search=ber
    #if we wanna leave space between the keywords we search for we use %20 such as: {{URL}}/posts?limit=3&search=something%20beaches

    #post = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    post = db.query(model.Post,func.count(model.Vote.post_id).label("votes")).join(model.Vote,model.Vote.post_id ==model.Post.id,isouter=True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    #this will count the total votes each unique posts received and name it as votes, it will join the vote and post table with join function and specifies the condition of join,by using isouter = True it will still return in the set the ones that does not match vote id and post it, and finally it groups the results by post id
    # it is the same as writing on sql: SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at, posts.owner_id AS posts_owner_id, count(votes.post_id) AS votes FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id GROUP BY posts.id;
    
    
    #post = db.query(model.Post).filter(model.Post.owner_id ==current_user.id).all()  #if we wanted the users to retrieve the posts that they created we could write such a code but as we want the posts public we will run the code above
    """if post.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="not authorized to perform requested action") """ #in the case we want our posts private we can add this line of code as well
    #return post
    return post
   

#@router.get("/{id}",response_model=schemas.respond_post)
@router.get("/{id}",response_model=schemas.PostOut)  
def get_posts(id: int,db: Session = Depends(get_db)):
    #post = db.query(model.Post).filter(model.Post.id == id).first()  # here we querying our database and return the first match that equalts to a value
    post = db.query(model.Post,func.count(model.Vote.post_id).label("votes")).join(model.Vote,model.Vote.post_id ==model.Post.id,isouter=True).group_by(model.Post.id).filter(model.Post.id == id).first()
    if not post:
        # Handle case where post is not found (e.g., raise 404 Not Found)
        raise HTTPException(status_code=404, detail="Post not found")
    return post
    
    

@router.delete("/{id}",status_code=204)#we dont use any response model bcz we already indicated a status code #above we defined a function to get the index and then we removed that index from our list array with the pop method
def delete_post(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)  #it queries the database to find the post with the given ID
    post = post_query.first()
    if post  == None:
        raise HTTPException(status_code=404,detail=f"post with id:{id} does not exist")
    if post.owner_id != current_user.id: #here we check if the id of the user trying to perform deleting post matches with the owner_id who basically created the post   so this way we prevent anyone to delete any post 
        raise HTTPException(status_code=403,detail="not authorized to perform requested action") 
    post_query.delete(synchronize_session=False)  #if the post exists, it deletes the post from database and with the code below it commits the transaction
    db.commit() 


@router.put("/{id}",response_model=schemas.respond_post)  #this is for updating the data in the list(or database)
def update_post(id: int,post:schemas.Post,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post_i = post_query.first()
    if post_i == None:
        raise HTTPException(status_code=404,detail=f"post with {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="not authorized to perform requested action") 

    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
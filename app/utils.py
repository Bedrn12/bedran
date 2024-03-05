#this file is for password hashing

from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")  #here we telling passlib what  hashing algorithm we wanna use

def hash(password: str):
    return pwd_context.hash(password)  #here we are hashing the password


def verify(plain_password,hashed_password):   #the plain pssword user provides and the hashed password stored in our database
    return pwd_context.verify(plain_password,hashed_password)   # this code compares and veerifies our plain password with our hashed password

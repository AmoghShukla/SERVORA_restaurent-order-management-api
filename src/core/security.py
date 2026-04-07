from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 1

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(password : str):
    '''
    the password is hashed into something gibberish based on the context and it is non reversable
    also it will be different everytime. 
    '''
    if len(password.encode('utf-8')) > 72:
        raise ValueError("Password too long  (max 72 bytes)") 
    return password_context.hash(password)

def verify_password(plain_password : str, hashed_password : str):
    '''
    it will help us verify the plain and hashed password    
    '''
    return password_context.verify(plain_password, hashed_password)


def create_access_token(data : dict):
    data_to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    data_to_encode.update({"exp" : expire})

    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data : dict):
    
    data_to_encode = data.copy()
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    data_to_encode.update({"exp" : expire, "type": "refresh"})
    
    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_refresh_token(token: str):
    '''
    Verify and decode a refresh token
    Returns the payload if valid, raises JWTError if invalid or expired
    '''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if payload.get("type") != "refresh":
            raise JWTError("Invalid token type")
        
        return payload
    except JWTError:
        raise


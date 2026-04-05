from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from src.core.security import SECRET_KEY, ALGORITHM

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token : str = Depends(oauth2scheme)):
    try : 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        
        return {
            "user_id" : user_id,
            "role" : role 
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def require_role(roles : list):
    def role_checker(user=Depends(get_current_user)):
        if user['role'] not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker
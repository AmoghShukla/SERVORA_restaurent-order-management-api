from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.core.security import SECRET_KEY, ALGORITHM

bearer_scheme = HTTPBearer(auto_error=True)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try : 
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid Token" )

        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        
        return {
            "user_id" : user_id,
            "role" : role 
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    


def require_role(roles : list):
    def role_checker(user=Depends(get_current_user)):
        all_roles = [r.upper() for r in roles]
        if str(user['role']).upper() not in all_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker

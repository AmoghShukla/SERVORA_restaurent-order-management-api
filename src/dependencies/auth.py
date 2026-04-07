from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.core.security import SECRET_KEY, ALGORITHM, create_access_token, verify_refresh_token

bearer_scheme = HTTPBearer(auto_error=True)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), request: Request = None):
    '''
    Authenticate user from access token in Authorization header.
    If access token is expired, attempts to use refresh token from Refresh Token header
    to automatically get a new access token without failing the request.
    '''
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid Token")

        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        
        return {
            "user_id": user_id,
            "role": role
        }
    except JWTError as e:

        if request:
            refresh_token = request.headers.get("Refresh Token")
            if refresh_token:
                try:
                    refresh_payload = verify_refresh_token(refresh_token)
                    
                    user_id = refresh_payload.get("sub")
                    role = refresh_payload.get("role")
                    
                    if user_id and role:
                        new_access_token = create_access_token({
                            'sub': user_id,
                            'role': role
                        })
                        
                        request.state.new_access_token = new_access_token
                        
                        return {
                            "user_id": user_id,
                            "role": role,
                            "new_access_token": new_access_token
                        }
                except JWTError:
                    pass  
        
        raise HTTPException(status_code=401, detail="Invalid or expired token. Provide a valid refresh token in Refresh Token header.")


def require_role(roles: list[str]):
    roles = {r.upper() for r in roles}
    def role_checker(user=Depends(get_current_user)):
        if user["role"].upper() not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return role_checker

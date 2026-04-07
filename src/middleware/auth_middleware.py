from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


class TokenRefreshMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        if hasattr(request.state, 'new_access_token'):
            response.headers["New-Access-Token"] = request.state.new_access_token
        
        return response

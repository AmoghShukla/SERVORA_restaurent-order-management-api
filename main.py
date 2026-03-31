from fastapi import FastAPI, APIRouter
from src.routers.order_routers import router


app = FastAPI()
app.include_router(router, prefix="/Orders/api/v1", tags=['Orders'])

app.get('/')
def HealthCheck():
    return {"message": "Welcome to the Order Management API!"}
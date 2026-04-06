from fastapi import FastAPI, APIRouter
from src.routers.order import router as orderrouter
from src.routers.restaurent import router as restaurentrouter
from src.database.base import Base
from src.database.session import engine
from src.routers.auth import router as loginrouter
from src.routers.user import router as userrouter
import src.model


app = FastAPI(title="Zwigato")
app.include_router(orderrouter, prefix="/api/v1", tags=['Orders'])
app.include_router(restaurentrouter, prefix="/api/v1", tags=['Restaurent'])
app.include_router(loginrouter, prefix="/api/v1", tags=['Auth'])
app.include_router(userrouter, prefix="/api/v1", tags=['User'])

# Base.metadata.create_all(bind=engine)

@app.get('/')
def home():
    return {"message": "Welcome to the Order Management API!"}
from fastapi import FastAPI, APIRouter
from src.routers.order import router as orderrouter
from src.routers.restaurent import router as restaurentrouter
from src.routers.menu import router as menurouter
from src.routers.items import router as itemsrouter
from src.routers.cart import router as cartrouter
from src.database.base import Base
from src.database.session import engine
from src.routers.auth import router as loginrouter
from src.routers.user import router as userrouter
import src.model


app = FastAPI(title="Zwigato")
app.include_router(orderrouter, prefix="/api", tags=['Orders'])
app.include_router(restaurentrouter, prefix="/api", tags=['Restaurent'])
app.include_router(menurouter, prefix="/api", tags=['Menu'])
app.include_router(itemsrouter, prefix="/api", tags=['Items'])
app.include_router(cartrouter, prefix="/api", tags=['Cart'])
app.include_router(loginrouter, prefix="/api", tags=['Auth'])
# app.include_router(userrouter, prefix="/api", tags=['User'])

# Base.metadata.create_all(bind=engine)

@app.get('/')
def home():
    return {"message": "Welcome to the Order Management API!"}
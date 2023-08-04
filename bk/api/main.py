from fastapi import FastAPI
from .routers import router as todos_router

api = FastAPI()

api.include_router(todos_router)

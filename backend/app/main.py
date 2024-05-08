from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.users import routers as users_routers
from app.posts import routers as posts_routers
from .config import settings

app = FastAPI()




@app.get("/")
async def root():
    return {"message": "Hello World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(users_routers.router)
app.include_router(posts_routers.router)
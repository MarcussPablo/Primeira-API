from fastapi import FastAPI
from app.database import engine, Base
from app.routes import auth_routes, post_routes, admin_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(post_routes.router)
app.include_router(admin_routes.router)

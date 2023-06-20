from dotenv import load_dotenv
import os

from fastapi import APIRouter
from models.user_model import User

from controllers.user_controller import show_users, create_new_user, login_user

load_dotenv()
JWT_SECRET = os.environ.get("JWT_SECRET") or ""

user_routes = APIRouter(prefix="/users")

@user_routes.get("/all")
async def all():
    return show_users()
    
@user_routes.post("/create")
async def create(user: User):
    return create_new_user(user)

@user_routes.post("/login")
async def login(user: User):
    return login_user(user, JWT_SECRET)
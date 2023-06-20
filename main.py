from fastapi import FastAPI
from routes.user_routes import user_routes
from routes.task_routes import task_routes

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Welcome"
    }

app.include_router(user_routes)
app.include_router(task_routes)
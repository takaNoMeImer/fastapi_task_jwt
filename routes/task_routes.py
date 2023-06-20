from fastapi import APIRouter,Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.task_model import Task
from controllers.task_controller import get_all_tasks, create_new_task, delete_task, update_task, find_task


security = HTTPBearer()

task_routes = APIRouter(prefix="/tasks")

@task_routes.get("/all")
async def all(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return get_all_tasks(credentials)

@task_routes.post("/create")
def create(task: Task, credentials: HTTPAuthorizationCredentials = Depends(security)):
    return create_new_task(task, credentials)
    
    
@task_routes.delete("/delete/{task_id}")
def delete(task_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    return delete_task(credentials, task_id)
    
    
@task_routes.put("/update/{task_id}")
def update(task_id: int, task: Task, credentials: HTTPAuthorizationCredentials = Depends(security)):
    return update_task(credentials, task, task_id)

@task_routes.get("/find/{task_id}")
def find(task_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    return find_task(credentials, task_id)
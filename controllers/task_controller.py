import json
import jwt
from database.config import conn
from fastapi import HTTPException
import redis

from dotenv import load_dotenv
import os
load_dotenv()

# ALTER SEQUENCE task_id_seq RESTART;
# DELETE FROM users;
# DELETE FROM tasks;

# Configuracion de redis
redis_host = "localhost"
redis_port = 6379
redis_db = 0
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

JWT_SECRET = os.environ.get("JWT_SECRET") or ""

def get_all_tasks(credentials):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, ["HS256"])

        # Verificar datos en Redis
        tasks_key = f"tasks:{payload['username']}"
        cached_tasks = redis_client.get(tasks_key)
        if cached_tasks:
            tasks = json.loads(cached_tasks)
            return tasks

        cursor = conn.cursor()
        query = "SELECT id, description FROM tasks"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        tasks = [{"id": row[0], "description": row[1]} for row in results]

        # Guardar datos en Redis como cadena JSON
        redis_client.set(tasks_key, json.dumps(tasks))

        return tasks
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
def create_new_task(task, credentials):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, ["HS256"])
        cursor = conn.cursor()
        
        # Siguiente valor
        cursor.execute("SELECT nextval('task_id_seq')")
        task_id = cursor.fetchone()[0]
        task.id = task_id

        query = "INSERT INTO tasks (id, description) VALUES (%s, %s)"
        cursor.execute(query, (task.id, task.description))
        conn.commit()
        cursor.close()

        # Eliminar en caché
        tasks_key = f"tasks:{payload['username']}"
        redis_client.delete(tasks_key)

        return {"message": "Tarea creada exitosamente"}
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Token Invalido")
    
def delete_task(credentials, task_id: int):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, ["HS256"])
        cursor = conn.cursor()
        query = "DELETE FROM tasks WHERE id = %s"
        cursor.execute(query, (task_id,))
        conn.commit()
        cursor.close()

        # Eliminar la entrada en caché
        tasks_key = f"tasks:{payload['username']}"
        redis_client.delete(tasks_key)

        return {"message": "Tarea eliminada exitosamente"}
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Token Invalido")
    
def update_task(credentials, task, task_id: int): 
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, ["HS256"])
        cursor = conn.cursor()
        query = "UPDATE tasks SET description = %s WHERE id = %s"
        cursor.execute(query, (task.description, task_id))
        conn.commit()
        cursor.close()

        # Eliminar la entrada en caché
        tasks_key = f"tasks:{payload['username']}"
        redis_client.delete(tasks_key)

        return {"message": "Tarea actualizada"}
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Token Invalido")
    
def find_task(credentials, task_id: int):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, ["HS256"])
        cursor = conn.cursor()
        query = "SELECT id, description FROM tasks WHERE id = %s"
        cursor.execute(query, (task_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            task = {"id": result[0], "description": result[1]}
            return task
        else:
            raise HTTPException(status_code=404, detail="La tarea no existe")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Token Invalido")
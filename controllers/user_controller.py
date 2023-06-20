from database.config import conn
from helpers.libs import get_password_hash, authenticate_user
from models.user_model import User
from fastapi import HTTPException
import jwt

def show_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    cursor.close()
    return {"data": results}

def create_new_user(user: User):
    cursor = conn.cursor()

    # Verificar si el usuario ya existe
    query = "SELECT COUNT(*) FROM users WHERE username = %s"
    cursor.execute(query, (user.username,))
    result = cursor.fetchone()
    if result and result[0] > 0:
        cursor.close()
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Insertar nuevo usuario
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    hashed_password = get_password_hash(user.password)
    cursor.execute(query, (user.username, hashed_password))
    conn.commit()
    cursor.close()
    return {"message": "Usuario creado exitosamente"}

def login_user(user: User, secret_key: str):
    authenticated_user = authenticate_user(user.username, user.password)
    if authenticated_user:
        token = jwt.encode(authenticated_user, secret_key, "HS256")
        return {"access_token": token}
    else:
        raise HTTPException(status_code=401, detail="Usuario o contraseña invalida")
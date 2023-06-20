from passlib.context import CryptContext
from database.config import conn

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username, password):
    cursor = conn.cursor()
    query = "SELECT username, password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()

    if result and verify_password(password, result[1]):
        return {"username": result[0]}
    return None
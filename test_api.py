import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_new_user(client: TestClient):
    response = client.post("/users/create", json={"username": "user1", "password": "password1"})

    assert response.status_code == 200
    expected_response = {"message": "Usuario creado exitosamente"}
    assert response.json() == expected_response

def test_create_new_task(client: TestClient):
    # Iniciamos sesion con un usuario y extraemos token
    response = client.post("/users/login", json={"username": "user1", "password": "password1"})
    access_token = response.json()["access_token"]

    # Creamos una tarea para eliminar
    response = client.post("/tasks/create", json={"description": "Descripcion de la tarea"}, headers={"Authorization": f"Bearer {access_token}"})

    # Verificar el código de respuesta
    assert response.status_code == 200

    # Verificar el contenido de la respuesta
    expected_response = {"message": "Tarea creada exitosamente"}
    assert response.json() == expected_response

def test_update_task(client):
    # Iniciamos sesion con un usuario y extraemos token
    response = client.post("/users/login", json={"username": "user1", "password": "password1"})
    access_token = response.json()["access_token"]

    # Creamos una tarea para actualizar
    response = client.post("/tasks/create", json={"description": "Esta "}, headers={"Authorization": f"Bearer {access_token}"})

    # Actualizamos
    response = client.put(f"/tasks/update/{2}",
                          json={"description": "Nueva descripcion"},
                          headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    expected_response = {"message": "Tarea actualizada"}
    assert response.json() == expected_response

def delete_task(client):
     # Iniciamos sesion con un usuario y extraemos token
    response = client.post("/users/login", json={"username": "user1", "password": "password1"})
    access_token = response.json()["access_token"]

    # Creamos una tarea para eliminar
    response = client.post("/tasks/create", json={"description": "Esta es la tarea que se va a eliminar"}, headers={"Authorization": f"Bearer {access_token}"})

    # Realizar la llamada a la API
    response = client.delete(f"/tasks/delete/{3}",
                             headers={"Authorization": f"Bearer {access_token}"})

    # Verificar el código de respuesta
    assert response.status_code == 200

    # Verificar el contenido de la respuesta
    expected_response = {"message": "Tarea eliminada exitosamente"}
    assert response.json() == expected_response
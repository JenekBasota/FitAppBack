import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from flask import Flask
from create_app import create_app



@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,  #
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client() 

@pytest.fixture()
def runner(app):
    return app.test_cli_runner() 


def test_login_success(client):
    response = client.post('/api/auth/login', json={
        "username": "admin",
        "password": "123456"
    })

    assert response.json["msg"] == "Login success"  
    assert response.json["status"] == 200
    assert "access_token" in response.json  

def test_hello_world(client):
    response = client.get('/') 
    
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello, World!'

def test_login_failure(client):
    response = client.post('/api/auth/login', json={
        "username": "wronguser",
        "password": "wrongpassword"
    })
    assert response.json["status"] == 401
    assert "msg" in response.json  

def test_invalid_data_format(client):
    response = client.post('/api/auth/login', json={
        "username": 123,  
        "password": 456   
    })
    assert "msg" in response.json  
    assert response.json["msg"] == "Incorrect data type detected"  
    assert response.json["status"] == 400


def test_missing_username(client):
    response = client.post('/api/auth/login', json={
        "password": "123456"  
    })
    
    assert "msg" in response.json
    assert response.json["msg"] == "Missing data" 
    assert response.json["status"] == 400  

def test_missing_password(client):
    response = client.post('/api/auth/login', json={
        "username": "admin"  
    })
    
    assert "msg" in response.json
    assert response.json["msg"] == "Missing data"  
    assert response.json["status"] == 400  

def test_empty_username(client):
    response = client.post('/api/auth/login', json={
        "username": "",  
        "password": "123456"
    })
    
    assert "msg" in response.json
    assert response.json["msg"] == "Missing data"  
    assert response.json["status"] == 400  

def test_empty_password(client):
    response = client.post('/api/auth/login', json={
        "username": "admin",
        "password": ""  
    })
    
    assert "msg" in response.json
    assert response.json["msg"] == "Missing data"  
    assert response.json["status"] == 400  

def test_invalid_password_type(client):
    response = client.post('/api/auth/login', json={
        "username": "admin",
        "password": 123456 
    })
    
    assert "msg" in response.json
    assert response.json["msg"] == "Incorrect data type detected"
    assert response.json["status"] == 400  

def test_existing_username(client):
    response = client.post('/api/auth/unique_check', json={
        "username": "admin",  
        "email": "admin123@mail.ru"
    })
    
    assert "msg" in response.json
    assert response.json["msg"] == "AUTH_REGISTER_EXISTING_LOGIN" 
    assert response.json["status"] == 401  

def test_existing_email(client):

    response = client.post('/api/auth/unique_check', json={
        "username": "adminasd",
        "email": "admin@mail.ru"  
    })
    
    assert "msg" in response.json
    assert response.json["msg"] == "AUTH_REGISTER_EXISTING_EMAIL"
    assert response.json["status"] == 401  

def test_unique_username_and_email(client):
    response = client.post('/api/auth/unique_check', json={
        "username": "newuniqueuser",  
        "email": "uniqueemail@example.com"  
    })
    
    assert "msg" in response.json
    assert response.json["msg"] == "AUTH_UNIQUE_SUCCESSFUL" 
    assert response.json["status"] == 200  

def test_invalid_username_format(client):
    response = client.post('/api/auth/unique_check', json={
        "username": 12345,  
        "email": "validemail@example.com"
    })
    
    assert "msg" in response.json
    assert response.json["msg"] == "Incorrect data type detected"  
    assert response.json["status"] == 400  

def test_invalid_email_format(client):
    response = client.post('/api/auth/unique_check', json={
        "username": "validusername",
        "email": 12313  
    })
    
    assert "msg" in response.json
    assert response.json["msg"] == "Incorrect data type detected"  
    assert response.json["status"] == 400  

def test_missing_data(client):
    response = client.post('/api/auth/unique_check', json={
        "username": "",  
        "email": ""  
    })
    
    assert "msg" in response.json
    assert response.json["msg"] == "Missing data" 
    assert response.json["status"] == 400  

def test_missing_json(client):
    response = client.post('/api/auth/unique_check', data="Non-JSON Data")
    
    assert "msg" in response.json
    assert response.json["msg"] == "Missing JSON in request"  
    assert response.json["status"] == 400  

def test_successful_registration(client):
    response = client.post('/api/auth/register', json={
        "username": "newuser5",
        "email": "newuser5@example.com",
        "weight": 70,
        "height": 175,  # ПОМЕНЯТЬ ПЕРЕД СТАРТОМ костыль))))))
        "gender": "m",
        "password": "securepassword123",
        "programs": 1
    })
    

    assert "access_token" in response.json
    assert response.json["msg"] == "User created"
    assert response.json["status"] == 200
    assert "data" in response.json

def test_missing_data(client):
    response = client.post('/api/auth/register', json={
        "username": "newuser",  
        "email": "",
        "weight": 70,
        "height": 175,
        "gender": "male",
        "password": "",
        "programs": 1
    })
    
    assert response.json["msg"] == "Missing data"
    assert response.json["status"] == 400

def test_incorrect_data_format(client):

    response = client.post('/api/auth/register', json={
        "username": "newuser",
        "email": "newuser@example.com",
        "weight": "seventy",
        "height": 175,
        "gender": "male",
        "password": "securepassword123",
        "programs": 1
    })

    assert response.json["msg"] == "Incorrect data type detected"
    assert response.json["status"] == 400

def test_missing_json(client):
    response = client.post('/api/auth/register', data="Non-JSON Data")
    
    assert response.json["msg"] == "Missing JSON in request"
    assert response.json["status"] == 400

def test_user_creation_error(client):
    response = client.post('/api/auth/register', json={
        "username": "existinguser",
        "email": "existinguser@example.com",  
        "weight": 70,
        "height": 175,
        "gender": "male",
        "password": "securepassword123",
        "programs": 1
    })
    
    assert response.json["msg"] == "WTF_U_ENTER"
    assert response.json["status"] == 400

def test_missing_programs(client):
    response = client.post('/api/auth/register', json={
        "username": "newuser",
        "email": "newuser@example.com",
        "weight": 70,
        "height": 175,
        "gender": "male",
        "password": "securepassword123",
        "programs": None 
    })
    
    assert response.json["msg"] == "Missing data"
    assert response.json["status"] == 400

def test_invalid_programs_data(client):
    response = client.post('/api/auth/register', json={
        "username": "newuser",
        "email": "newuser@example.com",
        "weight": 70,
        "height": 175,
        "gender": "male",
        "password": "securepassword123",
        "programs": "notinteger"  
    })
    
    assert response.json["msg"] == "Incorrect data type detected"
    assert response.json["status"] == 400

def test_check_token_success(client):
    response_login = client.post('/api/auth/login', json={
        "username": "admin",
        "password": "123456"
    })
    access_token = response_login.json["access_token"]

    response_check = client.get('/api/jwt/check', headers={
        "Authorization": f"Bearer {access_token}"
    })
    

    assert response_check.json["msg"] == "success"
    assert response_check.json["status"] == 200

def test_check_token_missing(client):
    response = client.get('/api/jwt/check')
    assert response.json["msg"] == "Missing Authorization Header"
    
def test_check_token_invalid(client):
    invalid_token = "invalid_token_1234567890"
    
    response = client.get('/api/jwt/check', headers={
        "Authorization": f"Bearer {invalid_token}"
    })

    assert response.json["msg"] == "Not enough segments"

def test_check_token_invalid(client):
    invalid_token = "BearerNotAJWT abc123"
    
    response = client.get('/api/jwt/check', headers={
        "Authorization": f"Bearer {invalid_token}"
    })

    assert response.json["msg"] == "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'"


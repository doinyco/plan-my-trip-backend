import json

def test_register_success(client, auth_header):
    response = client.post('/auth/register', 
                           data=json.dumps({'username': 'testuser', 'email': 'test@example.com', 'password': 'Password1'}),
                           headers=auth_header)
    assert response.status_code == 200
    assert b'Registration successful' in response.data

def test_register_missing_fields(client, auth_header):
    response = client.post('/auth/register', 
                           data=json.dumps({'username': 'testuser', 'password': 'Password1'}),
                           headers=auth_header)
    assert response.status_code == 400
    assert b'Username, email, and password are required fields' in response.data

def test_register_existing_username(client, auth_header):
    client.post('/auth/register', 
                data=json.dumps({'username': 'testuser', 'email': 'test1@example.com', 'password': 'Password1'}),
                headers=auth_header)
    
    response = client.post('/auth/register', 
                           data=json.dumps({'username': 'testuser', 'email': 'test2@example.com', 'password': 'Password2'}),
                           headers=auth_header)
    assert response.status_code == 400
    assert b'Username already exists' in response.data

def test_register_existing_email(client, auth_header):
    client.post('/auth/register', 
                data=json.dumps({'username': 'testuser1', 'email': 'test@example.com', 'password': 'Password1'}),
                headers=auth_header)
    
    response = client.post('/auth/register', 
                           data=json.dumps({'username': 'testuser2', 'email': 'test@example.com', 'password': 'Password2'}),
                           headers=auth_header)
    assert response.status_code == 400
    assert b'Email address already registered' in response.data

def test_register_password_rules(client, auth_header):
    response = client.post('/auth/register', 
                           data=json.dumps({'username': 'testuser', 'email': 'test3@example.com', 'password': 'short'}),
                           headers=auth_header)
    assert response.status_code == 400
    assert b'Password must be at least 8 characters long' in response.data

    response = client.post('/auth/register', 
                           data=json.dumps({'username': 'testuser', 'email': 'test4@example.com', 'password': 'nouppercase1'}),
                           headers=auth_header)
    assert response.status_code == 400
    assert b'Password must contain at least one uppercase letter' in response.data

    response = client.post('/auth/register', 
                           data=json.dumps({'username': 'testuser', 'email': 'test5@example.com', 'password': 'NoDigit!'}),
                           headers=auth_header)
    assert response.status_code == 400
    assert b'Password must contain at least one digit' in response.data

def test_login_success(client, auth_header):
    client.post('/auth/register', 
                data=json.dumps({'username': 'testuser', 'email': 'test6@example.com', 'password': 'Password1'}),
                headers=auth_header)
    
    response = client.post('/auth/login', 
                           data=json.dumps({'username/email': 'testuser', 'password': 'Password1'}),
                           headers=auth_header)
    assert response.status_code == 200
    assert b'Login successful' in response.data

def test_login_invalid_credentials(client, auth_header):
    response = client.post('/auth/login', 
                           data=json.dumps({'username/email': 'nonexistent', 'password': 'WrongPassword'}),
                           headers=auth_header)
    assert response.status_code == 401
    assert b'Invalid username or password' in response.data

def test_logout(client):
    # Simulate login to create a session
    client.post('/auth/register', 
                data=json.dumps({'username': 'testuser', 'email': 'test7@example.com', 'password': 'Password1'}),
                headers={'Content-Type': 'application/json'})
    client.post('/auth/login', 
                data=json.dumps({'username/email': 'testuser', 'password': 'Password1'}),
                headers={'Content-Type': 'application/json'})
    
    response = client.get('/auth/logout')
    assert response.status_code == 200
    assert b'You have been logged out' in response.data

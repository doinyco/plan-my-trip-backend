import pytest
from unittest.mock import patch, Mock
from app import db, create_app


@pytest.fixture(scope='session', autouse=True)
def mock_openai():
    # Mock the OpenAI client early
    with patch('app.routes.trip_routes.OpenAI') as mock_openai:
        mock_instance = Mock()
        mock_instance.some_method.return_value = 'mocked_response'
        mock_openai.return_value = mock_instance
        yield mock_openai

@pytest.fixture
def app(mock_openai):
    # Create and configure the app for testing
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db', 'SECRET_KEY': 'plan_my_trip',})
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_header():
    return {'Content-Type': 'application/json'}

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pytest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Initialize SQLAlchemy before Migrate
migrate = Migrate(app, db)  # Then initialize Migrate

from models import Author, Post  # Import models after initializing db to avoid circular import issues

@app.route('/')
def index():
    return 'Validations lab'

@pytest.fixture(scope='session')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for tests

    with app.app_context():
        db.create_all()  # Creates all tables based on your models

    test_client = app.test_client()

    yield test_client  # this is where the testing happens

    with app.app_context():
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    app.run(port=5555, debug=True)

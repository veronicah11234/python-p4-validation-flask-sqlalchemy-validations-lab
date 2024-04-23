from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if name == "":
            raise ValueError("Name should not be an empty string")
        else:
            if Author.query.filter(Author.name == name).first():
                raise ValueError("Name already exists")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError("Number should have 10 digits")
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, words):
        if len(words) != 250 or len(words) > 250:
            raise ValueError("Content should be at least 250 characters long")
        return words

    @validates('summary')
    def validate_summary(self, key, words):
        if len(words) != 250:
            raise ValueError("Content should be 250 characters long")
        return words

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
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
        if key == 'name':
            if not name or Author.query.filter_by(name=name).first():
                raise ValueError("N/A")
            return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if  self.name and not (phone_number.isdigit() and len(phone_number) == 10):
            raise ValueError('N/A')
        return phone_number

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
    @validates('title')
    def validate_title(self, key, title):
        phrases = ["Won't Believe", "Secret", "Top","Guess"]
        if not title:
            raise ValueError('N/A')
        elif not any(phrase in title for phrase in phrases):
            raise ValueError('N/A')
        return title

    @validates('content')
    def validate_content(self, key, content):
        if not len(content) >= 250:
            raise ValueError("N/A")
        return content    
    @validates('summary')
    def validate_summary(self, key, summary):
        if not len(summary) <= 250:
            raise ValueError('N/A')
        return summary
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('N/A')
        return category 
   

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

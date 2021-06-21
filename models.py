import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

db = SQLAlchemy()

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

# database_path = "postgresql://postgres:12postgres34@localhost:5432/castingagency"

def setup_db(app):

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    # moment = Moment(app)
    db.init_app(app)
    # db.create_all()
    migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    actor = Actor(
        name = 'actor1',
        gender = 'male',
        age = '54'
    )
    actor.insert()

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.String())
    gender = db.Column(db.String())


    def format(self):
        return {
        'id':self.id,
        'name': self.name,
        'gender': self.gender,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    release_date = db.Column(db.String())
    
    def format(self):
        return {
        'id':self.id,
        'name': self.name,
        'genres': self.genres,
        }
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



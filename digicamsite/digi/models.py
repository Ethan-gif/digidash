from digi import db
from flask_login import UserMixin
from datetime import datetime
#This file is responsible for creating the database models



class Photo(db.Model):
    __tablename__ = "photo"
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(400))
    name = db.Column(db.String(200))
    creation_date=db.Column(db.Date)



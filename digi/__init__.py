from flask import Flask 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db=SQLAlchemy(session_options={"autoflush":False})
#create a function that creates a web application
# a web server will run this web application

def init_db():
    """For use on command line for setting up
    the database.
    """

    db.drop_all()
    db.create_all()


def create_app():
    print(__name__)  
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=True
    app.secret_key='dafdfsfgdhh'
    #config
    app.config['SQLALCHEMY_DATABASE_URI']=os.environ['DATABASE_URL']
    #init
    db.init_app(app)
    
    bootstrap=Bootstrap(app)
    
    #initialise the login manager
 



    from . import views
    app.register_blueprint(views.mainbp)  
    

    return app


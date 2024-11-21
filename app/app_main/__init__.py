from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db=SQLAlchemy()
migrate=Migrate()

def mydb():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:password1234@127.0.0.1/new_database"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    db.init_app(app)
    migrate.init_app(app,db)
    JWTManager(app)

    from app.app_main.models import Users


    return app
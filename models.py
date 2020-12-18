from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy() #DATABASE SETTING

def connect_db(app):
    db.app= app
    db.init_app(app)

#models go below:


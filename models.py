from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db=SQLAlchemy() #DATABASE SETTING

def connect_db(app):
    db.app= app
    db.init_app(app)

#models go below:


class User(db.Model):
    """define user model"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                         primary_key=True)

    username = db.Column(db.String(20),
    nullable=False, unique=True)

    password = db.Column(db.String(50),
                         nullable=False)

    profile_img = db.Column(db.String(30),
                         nullable=False)

    #feedback = db.relationship("Feedback",backref="user",cascade="all,delete")
    
     # start_register
    @classmethod
    def register(cls, username, pwd,profile_img):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        user = cls(
            username = username,
            password = hashed_utf8,
            profile_img = profile_img
        )

        return user
    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate  


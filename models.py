from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()  # DATABASE SETTING
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)

# models go below:


class User(db.Model):
    """define user model"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)

    username = db.Column(db.Text,
                         nullable=False, unique=True)

    password = db.Column(db.Text,
                         nullable=False)

    profile_img = db.Column(db.Text,
                            nullable=False,
                            default='https://cdn.business2community.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png'
                            )

    shoppinglist = db.relationship(
        "ShoppingList", backref="user", cascade="all,delete")
    userfav = db.relationship("UserFav", backref="user", cascade="all,delete")

    # start_register

    @classmethod
    def register(cls, username, pwd, profile_img):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(
            username=username,
            password=hashed_utf8,
            profile_img=profile_img
        )

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


# shopping lists model
class ShoppingList(db.Model):
    """define the shopping list model"""

    __tablename__ = "shoppinglists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    username = db.Column(db.Text, db.ForeignKey(
        "users.username"), nullable=False)

 # user favorite model


class UserFav(db.Model):
    """ user favorite relationship model"""
    __tablename__ = "user_fav"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, db.ForeignKey(
        'users.username'), nullable=False)
    asin = db.Column(db.Text, nullable=False)
    fav = db.Column(db.Boolean, default=True)

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,PasswordField,BooleanField,SubmitField,SelectField
from wtforms.validators import InputRequired,Email,NumberRange,AnyOf, DataRequired

## the loginForm

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    
## signup form

class RegisterForm(FlaskForm):
    """form for register user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    profile_img= StringField("Profile Image URL", validators=[InputRequired()])



### THE Asin SEARCH FORM 

class AsinSearchForm(FlaskForm):
    """using the validator to request input"""
    class Meta:
        csrf = False
    
    ASIN = StringField("ASIN",validators=[InputRequired()])
    country = SelectField('country', choices=[
    ('US','US'),('AU','AU'),('BR','BR'),('CA','CA'),('CN','CN'),('FR','FR'),('DE','DE'),('IN','IN'),('IT','IT'),
    ('MX','MX'),('NL','NL'),('SG','SG'),('ES','ES'),('TR','TR'),('AE','AE'),('GB','GB'),('JP','JP')
    ])
 

### The reviews by asin form

class ReviewsByAsinForm(FlaskForm):
    """using the validator, return reviews by asin"""
    
    class Meta:
        csrf = False
    
    reviewsByAsin = StringField("Reviews by Asin",validators=[InputRequired()])

    country = SelectField('country', choices=[
    ('US','US'),('AU','AU'),('BR','BR'),('CA','CA'),('CN','CN'),('FR','FR'),('DE','DE'),('IN','IN'),('IT','IT'),
    ('MX','MX'),('NL','NL'),('SG','SG'),('ES','ES'),('TR','TR'),('AE','AE'),('GB','GB'),('JP','JP')
    ])


class ShoppingListForm(FlaskForm):
    """create shopping list form"""
    class Meta:
        csrf = False
    
    content = StringField("Add Shopping List", validators=[InputRequired()])

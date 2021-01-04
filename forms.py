from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,PasswordField,BooleanField,SubmitField
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



### THE UPC SEARCH FORM 

class AsinSearchForm(FlaskForm):
    """using the validator to request input"""
    class Meta:
        csrf = False
    
    ASIN = StringField("ASIN",validators=[InputRequired()])
 




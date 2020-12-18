from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,PasswordField,BooleanField,SubmitField
from wtforms.validators import InputRequired,Email,NumberRange,AnyOf, DataRequired

## the loginForm

class LoginForm(FlaskForm):
    """user login"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



### THE SEARCH FORM 

class SearchForm(FlaskForm):
    """using the validator to request input"""
    class Meta:
        csrf = False
    
    brand = StringField("Brand",validators=[InputRequired()])
    productname = StringField("ProductName",validators=[InputRequired()])
    version =StringField("version")




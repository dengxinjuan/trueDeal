from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired,Email,NumberRange,AnyOf


### THE SEARCH FORM 

class SearchForm(FlaskForm):
    """using the validator to request input"""
    class Meta:
        csrf = False
    
    brand = StringField("Brand",validators=[InputRequired()])
    productname = StringField("ProductName",validators=[InputRequired()])
    version =StringField("version")




##class LoginForm(FlaskForm):


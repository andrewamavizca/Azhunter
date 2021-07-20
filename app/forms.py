from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()]) 
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditParameters(FlaskForm):
    rank1 = IntegerField('rank', validators=[Optional()])
    price1 = IntegerField('price',validators=[Optional()])
    rank2 = IntegerField('rank2', validators=[Optional()])
    price2 = IntegerField('price2', validators=[Optional()])
    rank3 = IntegerField('rank3', validators=[Optional()])
    price3 = IntegerField('price3', validators=[Optional()])
    rank4 = IntegerField('rank4', validators=[Optional()])
    price4 = IntegerField('price4', validators=[Optional()]) 
    rank5 = IntegerField('rank5', validators=[Optional()])
    price5 = IntegerField('price5', validators=[Optional()])
    submit = SubmitField('Save Settings')

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, FloatField, DateField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Length


class PixForm(FlaskForm):
    secret_key = StringField(validators=[DataRequired()])
    amount = FloatField(validators=[DataRequired(), NumberRange(min=0.01, message='O valor deve ser maior do que 0.')])
    
class TransactionDateSearch(FlaskForm):
    date = DateField(validators=[DataRequired()])
    
class RegistrationForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=16, max=16)])
    cpf = StringField(validators=[DataRequired(), Length(min=11, max=11)])
    email = EmailField(validators=[DataRequired()])
    phone = StringField(validators=[DataRequired()])
    accept_terms = BooleanField(validators=[DataRequired()])
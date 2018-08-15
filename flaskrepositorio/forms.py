from flask_wtf import FlaskForm
from wtforms import DecimalField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    matricula = DecimalField('Matricula',
                             validators=[DataRequired()])
    password = PasswordField('Senha',
                             validators=[DataRequired()])

    submit = SubmitField('Entrar')

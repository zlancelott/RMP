from flask_wtf import FlaskForm
from wtforms import DecimalField, PasswordField, SubmitField, StringField, SelectField, FileField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, regexp


class LoginForm(FlaskForm):
    matricula = DecimalField('Matricula',
                             validators=[DataRequired()])
    password = PasswordField('Senha',
                             validators=[DataRequired()])

    submit = SubmitField('Entrar')


class UploadFileForm(FlaskForm):
    subject_class = SelectField(u'Disciplina', coerce=int, validators=[DataRequired()])
    lesson = SelectField(u'Aula', coerce=int, validators=[DataRequired()])
    topics = SelectMultipleField(u'Tópicos', coerce=int, validators=[DataRequired()])
    fileUpload = FileField(u'Arquivo', validators=[DataRequired()])
    submit = SubmitField('Submeter')

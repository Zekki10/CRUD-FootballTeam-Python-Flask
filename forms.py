from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class SignupForm(FlaskForm):
    txtNombre = StringField('Name', validators=[DataRequired(), Length(min=4,max=64)])
    txtFoto = FileField('Picture', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'png'], 'Only images files allowed')
    ])
    submit = SubmitField('Add Player')
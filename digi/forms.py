from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField,
    StringField,
    FileField,

)

from wtforms.validators import InputRequired

# this file has all the functions that create the different forms users 



class PhotoForm(FlaskForm):
    name = StringField("Title", )
    image = FileField("Cover Image",validators=[InputRequired()])
    submit = SubmitField("Submit")

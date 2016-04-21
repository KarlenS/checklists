from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required,Optional

class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[Required()])
    date = DateField('Date', validators=[Required()])
    room = StringField('Room', validators=[Optional()])
    submit = SubmitField('Enter the form')

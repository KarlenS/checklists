from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required,Optional

class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Observer', validators=[Required()])
    date = DateField('Date (UTC)', validators=[Required()])
    room = StringField('Room', validators=[Optional()])
    submit_start = SubmitField('Start of Night Form')
    submit_end = SubmitField('End of Night Form')

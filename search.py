from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class Search(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Enter')
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#use FlaskForm to create the backend of search engine
class Search(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Enter')
    load = SubmitField('Load More')
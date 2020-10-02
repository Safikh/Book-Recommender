from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField



class SearchForm(FlaskForm):
    text = StringField('Title')
    submit = SubmitField('')

class RatingForm(FlaskForm):
    rating = RadioField(choices=[1,2,3,4,5])
    submit = SubmitField('Rate the book')

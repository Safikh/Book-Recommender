from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField


class RatingForm(FlaskForm):
    rating = RadioField(choices=[1,2,3,4,5])
    submit = SubmitField('Rate the book')

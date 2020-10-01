from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FieldList, FormField


class SearchForm(FlaskForm):
    text = StringField('Title')
    submit = SubmitField('Search')

from flask import render_template, Blueprint, redirect, url_for
from project.core.forms import SearchForm
import pandas as pd
import os

curr_dir = os.path.abspath(os.path.dirname(__file__))
df_path = os.path.join(curr_dir, 'data/processed_books.csv')
df = pd.read_csv(df_path)
#print(df.head)
M = df['book_id_new'].nunique()

core = Blueprint('core', __name__)

@core.route('/')
def index():
    return render_template('index.html')


@core.route('/info')
def info():
    return render_template('info.html')


@core.route('/search', methods=['GET', 'POST'])
def search():

    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for('core.search_results', text=form.text.data))

    return render_template('search.html', form=form)


@core.route('/search_results?<text>')
def search_results(text):

    results = df[df['title'].str.contains(text, case=False)]
    return render_template('search_results.html', results=results)

from flask import render_template, Blueprint, redirect, url_for
from project.core.forms import SearchForm, RatingForm
from project.core import predict
import pandas as pd
import numpy as np
import os

curr_dir = os.path.abspath(os.path.dirname(__file__))
df_path = os.path.join(curr_dir, 'data/processed_books.csv')
df = pd.read_csv(df_path)
#print(df.head)
M = df['book_id_new'].nunique()
df['given_rating'] = np.zeros(M)

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


@core.route('/book/<int:book_id_new>', methods=['GET', 'POST'])
def book(book_id_new):

    if book_id_new < M:

        book = df.loc[df['book_id_new'] == book_id_new]
        form = RatingForm()

        if form.validate_on_submit():
            df.at[book_id_new, "given_rating"] = form.rating.data
            book = df.loc[df['book_id_new'] == book_id_new]
            return redirect(url_for('core.user_ratings'))

        return render_template('book_page.html', book=book, form=form)

    # Have to render error page for invalid book ID
    #return render_template('book_page.html', title='Invalid Book ID!')


@core.route('/user_ratings')
def user_ratings():

    rated_books = df[df["given_rating"] != 0]
    return render_template('user_ratings.html', rated_books=rated_books)


@core.route('/recommendations')
def recommendations():

    if (df['given_rating'] != 0).sum() < 10:
        return redirect(url_for('core.user_ratings'))

    preds = predict(df['given_rating'].values.reshape(1, M)).reshape(-1, 1)

    df['predicted_rating'] = [np.round(pred, 2) for pred in preds]
    print(preds.max(), preds.min(), preds.mean())
    recc_books = df[df['given_rating'] == 0].sort_values(by='predicted_rating', ascending=False)[:10]
    return render_template('recommendations.html', recc_books=recc_books)

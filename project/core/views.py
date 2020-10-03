from flask import render_template, Blueprint, redirect, url_for, request
from project.core.forms import RatingForm
from project.core import predict
import pandas as pd
import numpy as np
import os

curr_dir = os.path.abspath(os.path.dirname(__file__))
df_path = os.path.join(curr_dir, 'data/processed_books.csv')
df = pd.read_csv(df_path)
M = df['book_id_new'].nunique()
df['given_rating'] = np.zeros(M) # Adding an empty column to store user ratings

core = Blueprint('core', __name__)

@core.route('/')
def index():
    return render_template('index.html') # Home Page template


@core.route('/info')
def info():
    return render_template('info.html') # About Page template


@core.route('/search')
def search():

    text = request.args['title']
    results = df[df['title'].str.contains(text, case=False)] # Search the titles for books based on text entered
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

    return render_template('error_pages/404.html'), 404 # When book_id exceeds limit


@core.route('/user_ratings')
def user_ratings():

    rated_books = df[df["given_rating"] != 0] # Capturing books only which were rated
    return render_template('user_ratings.html', rated_books=rated_books)


@core.route('/recommendations')
def recommendations():

    if (df['given_rating'] != 0).sum() < 5: # Need at least 5 ratings
        return redirect(url_for('core.user_ratings'))

    preds = predict(df['given_rating'].values.reshape(1, M)).reshape(-1, 1)
    df['predicted_rating'] = [np.round(pred, 2) for pred in preds]
    recc_books = df[(df['given_rating'] == 0) & (df['predicted_rating'] > 3.5)].sample(n=10) # GEtting a random sample of the books

    return render_template('recommendations.html', recc_books=recc_books)

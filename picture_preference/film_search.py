from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from picture_preference import web_scrape


bp = Blueprint('film_search',__name__)


@bp.route('/',methods=('GET','POST'))
def search():
    if request.method == 'POST':
        film = request.form['film']
        error = None

        if not film:
            error = 'Please input a film title.'

        if error is not None:
            flash(error)
        else:
            obscurity.check_popularity(film)


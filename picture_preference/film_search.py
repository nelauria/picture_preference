from flask import (
    Blueprint, flash, session, redirect, render_template, request, url_for, current_app
)
import requests
import json


bp = Blueprint('film_search', __name__)


@bp.route('/', methods=('GET', 'POST'))
def film_search():
    if not request.script_root:
        request.script_root = url_for('home', _external=True)
    if request.method == 'POST':
        session["film"] = request.form["film"]
        # print(session["film"])
        error = None

        if not session['film']:
            error = 'Please input a film title.'

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('output.results'))
    return render_template('film_search.html')


@bp.route('/_search')
def _search():
    query = request.args.get('searchQuery')
    api_key = current_app.config["TMDB_KEY"]
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US'
    results = []
    if query:
        query = query.replace(' ', '%20')
        search_url = search_url + f'&query={query}&page=1&include_adult=false'
        response = requests.get(search_url)
        results = response.json()['results']
        results = results[0:5]
    return json.dumps(results)

from flask import (
    Blueprint, flash, session, redirect, render_template, request, url_for, current_app
)


bp = Blueprint('film_search',__name__)


@bp.route('/',methods=('GET','POST'))
def film_search():
    if request.method == 'POST':
        session['film'] = request.form['film']
        error = None

        if not session['film']:
            error = 'Please input a film title.'

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('output.results'))
    return render_template('film_search.html',TMDB_KEY=current_app.config["TMDB_KEY"])

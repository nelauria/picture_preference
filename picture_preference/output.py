from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from picture_preference import film_data


bp = Blueprint('output',__name__)


@bp.route('/results')
def results():
    film = str(session['film'])
    g.title, g.rank, g.obscurity = film_data.check_popularity(film)
    return render_template('results.html')

from flask import (
    Blueprint, g, render_template, session
)
from .film_db import FilmModel
import math

bp = Blueprint('output', __name__)


@bp.route('/results')
def results():
    g.title = session["film"]
    error = None
    g.film = FilmModel.query.filter(
        FilmModel.title == g.title
    ).first() #change this to all when addressing duplicate films
    if g.film:
        g.rank = f"#{g.film.rank}"
        g.popularity = math.exp(-(g.film.rank-1)/2000)
        g.obscurity = (1-g.popularity)*10
        g.obscurity = "%.2g" % g.obscurity
    else:
        g.rank = "Pretty damn low"
        g.obscurity = "10"

    return render_template('results.html')

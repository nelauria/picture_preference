from flask import (
    Blueprint, g, render_template, session
)
from .film_db import FilmModel

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
        g.obscurity = ((g.film.rank-1)/544834)*100
        g.obscurity = "%.3g%%" % g.obscurity
    else:
        g.rank = "Pretty damn low"
        g.obscurity = "Inefficiently Obscure"

    return render_template('results.html')

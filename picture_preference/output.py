from flask import (
    Blueprint, g, render_template, session
)
from .film_db import FilmModel
import math
# from .easter_eggs import easter_eggs

bp = Blueprint('output', __name__)


@bp.route('/results')
def results():
    # g.easter_eggs = easter_eggs
    g.title = session["film"]
    error = None
    g.film = FilmModel.query.filter(
        FilmModel.title == g.title
    ).first() #change this to all when addressing duplicate films
    if g.film:
        g.rank = f"#{g.film.rank}"
        g.popularity = math.exp(-(g.film.rank - 1) / 2000)
        g.obscurity = (1 - g.popularity) * 10
        if g.obscurity >= 0.75:
            min_rank = 1 - 2000 * math.log(1 - (g.obscurity - 0.5) / 10)
            min_rank = math.floor(min_rank)
            g.mainstream = FilmModel.query.filter(
                FilmModel.rank.between(min_rank, g.film.rank)
            ).all()
            g.main_ids = [i.tmdb_id for i in g.mainstream]
        if g.obscurity <= 9.0:
            max_rank = 1 - 2000 * math.log(1 - (g.obscurity + 0.5) / 10)
            max_rank = math.floor(max_rank)
            g.obscure = FilmModel.query.filter(
                FilmModel.rank.between(g.film.rank, max_rank)
            ).all()
            g.obs_ids = [i.tmdb_id for i in g.obscure]
        g.obscurity = "%.2g" % g.obscurity
    else:
        g.rank = None
        g.obscurity = "10"

    return render_template('results.html')

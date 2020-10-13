from flask import (
    Blueprint, g, render_template, session, current_app
)
from .film_db import FilmModel, recommend
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
        import requests
        g.rank = f"#{g.film.rank}"
        recs, g.obscurity = recommend(g.film)
        g.obscurity = "%.2g" % g.obscurity
        for i in ["main", "obscure"]:
            titles = []
            posters = []
            if not recs[i]:
                continue
            for tmdb_id in recs[i]:
                details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={current_app.config['TMDB_KEY']}&language=en-US"
                response = requests.get(details_url)
                details = response.json()
                title_year = details["title"] + f" ({details['release_date'][0:4]})"
                titles.append(title_year)
                img_url = "https://image.tmdb.org/t/p/w92/"
                try:
                    poster_path = img_url + details["poster_path"]
                except KeyError:
                    details_url = details_url.replace("/movie/", "/tv/")
                    response = requests.get(details_url)
                    details = response.json()
                    poster_path = img_url + details["poster_path"]
                posters.append(poster_path)
            recs_tuple = list(zip(titles, posters))
            recs[i] = recs_tuple
        g.main_recs = recs["main"]
        print(g.main_recs)
        g.obs_recs = recs["obscure"]
        print(g.obs_recs)
    else:
        g.rank = None
        g.obscurity = "10"

    return render_template('results.html')

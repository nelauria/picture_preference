from flask import (
    Blueprint, g, render_template, session
)
from picture_preference.db import get_db
from picture_preference import film_data


bp = Blueprint('output',__name__)


@bp.route('/results')
def results():
    g.title = session["film"]
    db = get_db()
    error = None
    # g.title, g.rank, g.obscurity = film_data.check_popularity(film)
    # try:
    g.rank = db.execute(
        'SELECT rank FROM film WHERE title = ?', (g.title,)
    ).fetchone()[0]
    g.obscurity = ((g.rank-1)/544834)*100

    return render_template('results.html')

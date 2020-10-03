from picture_preference import web_scrape
from flask_sqlalchemy import SQLAlchemy, event
from flask import current_app
import time

db = SQLAlchemy()


class FilmModel(db.Model):
    __tablename__ = "films"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    rank = db.Column(db.Integer, unique=True)
    href = db.Column(db.String(), unique=True)
    tmdb_id = db.Column(db.Integer)

    def __init__(self, title, rank, href, tmdb_id):
        self.title = title
        self.rank = rank
        self.href = href
        self.tmdb_id = tmdb_id

    def __repr__(self):
        return f"<Film {self.title}>"


@current_app.cli.command("db-fill")
def build_top(*args, **kwargs):
    time_start = time.time()
    FilmModel.query.delete()
    chapters = 5
    chapter_length = 25
    for chapter in range(chapters):
        print(f"Filling from chapter {chapter+1} ({chapter_length} pages)...")
        start = 1+chapter*chapter_length
        end = (chapter+1)*chapter_length
        titles, ranks, hrefs, tmdb_ids = web_scrape.top_pages(start_page=start, end_page=end)
        if not (len(titles) == len(ranks) == len(hrefs) == len(tmdb_ids)):
            raise Exception("Error in web_scrape.py: titles, ranks, hrefs, tmdb_ids are not of the same length.")
        db.session.add_all([FilmModel(titles[i], ranks[i], hrefs[i], tmdb_ids[i]) for i in range(len(titles))])
        db.session.commit()
    time_end = time.time()
    print(f"Top {72*(chapters*chapter_length)} films initialized.")
    print(f"Time: {time_end-time_start}")

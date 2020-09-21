from . import db
from picture_preference import web_scrape
from flask_sqlalchemy import event
from flask import current_app


class FilmModel(db.Model):
    __tablename__ = "films"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    rank = db.Column(db.Integer, unique=True)
    href = db.Column(db.String(), unique=True)

    def __init__(self, title, rank, href):
        self.title = title
        self.rank = rank
        self.href = href

    def __repr__(self):
        return f"<Film {self.title}"


@event.listens_for(FilmModel.__table__, 'after_create')
def build_top(*args, **kwargs):
    chapters = 2
    chapter_length = 15
    for chapter in range(chapters):
        start = 1+chapter*chapter_length
        end = (chapter+1)*chapter_length
        titles, ranks, hrefs = web_scrape.top_pages(start_page=start, end_page=end)
        if not (len(titles) == len(ranks) == len(hrefs)):
            raise Exception("Error in web_scrape.py: titles, ranks, hrefs are not of the same length.")
        db.session.add_all([FilmModel(titles[i], ranks[i], hrefs[i]) for i in range(len(titles))])
        db.session.commit()
    print(f"Top {72*(chapters*chapter_length)} films initialized.")

from picture_preference import web_scrape
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import time
import math
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

db = SQLAlchemy()


class FilmModel(db.Model):
    __tablename__ = "films"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    rank = db.Column(db.Integer, unique=True)
    href = db.Column(db.String(), unique=True)
    tmdb_id = db.Column(db.Integer)
    film_meta = db.Column(db.String())

    def __init__(self, title, rank, href, tmdb_id, film_meta):
        self.title = title
        self.rank = rank
        self.href = href
        self.tmdb_id = tmdb_id
        self.film_meta = film_meta

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
        titles, ranks, hrefs, tmdb_ids, film_meta = web_scrape.top_pages(start_page=start, end_page=end)
        if not (len(titles) == len(ranks) == len(hrefs) == len(tmdb_ids)):
            raise Exception("Error in web_scrape.py: titles, ranks, hrefs, tmdb_ids are not of the same length.")
        db.session.add_all([
            FilmModel(titles[i], ranks[i], hrefs[i], tmdb_ids[i], film_meta[i]) for i in range(len(titles))
        ])
        db.session.commit()
    time_end = time.time()
    print(f"Top {72*(chapters*chapter_length)} films initialized.")
    print(f"Time: {time_end-time_start}")


def recommend(film):
    popularity = math.exp(-(film.rank - 1) / 2000)
    obscurity = (1 - popularity) * 10
    if obscurity >= 1:
        min_rank = 1 - 2000 * math.log(1 - (obscurity - 0.95) / 10)
        min_rank = math.floor(min_rank)
        mainstream = FilmModel.query.filter(
            FilmModel.rank.between(min_rank, film.rank)
        ).all()
        main_soup = {i.tmdb_id: i.film_meta for i in mainstream}
    else:
        main_soup = None
    if obscurity <= 8.7:
        max_rank = 1 - 2000 * math.log(1 - (obscurity + 0.95) / 10)
        max_rank = math.floor(max_rank)
        obscure = FilmModel.query.filter(
            FilmModel.rank.between(film.rank, max_rank)
        ).all()
        obs_soup = {i.tmdb_id: i.film_meta for i in obscure}
    else:
        obs_soup = None
    recs = {"main": None, "obscure": None}
    for i in list(recs.keys()):
        if i == "main":
            soup = main_soup
        elif i == "obscure":
            soup = obs_soup
        else:
            raise Exception("SoupError")
        if not soup:
            continue
        count = CountVectorizer(stop_words="english")
        count_matrix = count.fit_transform(list(soup.values()))
        cosine_sim = cosine_similarity(count_matrix)
        sims = cosine_sim[0]
        # print(sims)
        sim_inds = np.argpartition(sims, -3)[-3:-1]
        recs[i] = [list(soup.keys())[ind] for ind in sim_inds if (sims[ind] > 0.2)]
        # print(sims[sim_inds])
    return recs, obscurity

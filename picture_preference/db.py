import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from picture_preference import web_scrape


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def build_top(chapters, chapter_length):
    for chapter in range(chapters):
        start = 1+chapter*chapter_length
        end = (chapter+1)*chapter_length
        db = get_db()
        titles, ranks, hrefs = web_scrape.top_pages(start_page=start, end_page=end)
        data = zip(titles, ranks, hrefs)
        db.executemany(
            'INSERT INTO film (title, rank, href) VALUES (?,?,?)', data
        )
        db.commit()
    print(f"Top {72*(chapters*chapter_length)} films initialized.")


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

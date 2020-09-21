import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, event
from flask_migrate import Migrate
import psycopg2


db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # create & configure app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load instance config (if it exists) when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config if passed in
        app.config.from_mapping(test_config)

    # uncomment below for Heroku deployment
    app.config.update(
        DATABASE_URL=os.environ['DATABASE_URL'],
        SQLALCHEMY_DATABASE_URI=os.environ['SQLALCHEMY_DATABASE_URI'],
        TMDB_KEY=os.environ['TMDB_KEY'],
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.environ['SECRET_KEY']
    )
    conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode='require')

    migrate.init_app(app, db)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():
        from . import film_db
        # if film_db.FilmModel.__table__.exists(db.engine):
        film_db.FilmModel.__table__.drop(db.engine)
        film_db.db.create_all()
        # film_db.build_top(chapters=1, chapter_length=15)
        # event.listen(db.FilmModel.__table__, 'after_create', build_top(chapters=1,chapter_length=15))

        from . import film_search
        app.register_blueprint(film_search.bp)
        app.add_url_rule('/', endpoint='home')

        from . import output
        app.register_blueprint(output.bp)

    return app


# if __name__ == '__main__':
#     app = create_app()
#     app.run()

import os
from flask import Flask
from flask_migrate import Migrate
import psycopg2


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

    # db.init_app(app)
    # migrate.init_app(app, db)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import film_db
        film_db.db.init_app(app)
        migrate.init_app(app, film_db.db)
        # if film_db.FilmModel.__table__.exists(film_db.db.engine):
        #     film_db.FilmModel.__table__.drop(film_db.db.engine)
        film_db.db.create_all()

        from . import film_search
        app.register_blueprint(film_search.bp)
        app.add_url_rule('/', endpoint='home')

        from . import output
        app.register_blueprint(output.bp)

    return app

import os
from flask import Flask


def create_app(test_config=None):
    # create & configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(
        DATABASE=os.path.join(app.instance_path, 'picture_preference.sqlite'),
    )

    if test_config is None:
        # load instance config (if it exists) when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        # load test config if passed in
        app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import film_search
    app.register_blueprint(film_search.bp)
    app.add_url_rule('/', endpoint='home')

    from . import output
    app.register_blueprint(output.bp)

    TMDB_KEY = app.config["TMDB_KEY"]

    from . import db
    db.init_app(app)
    with app.app_context():
        db.init_db()
        db.build_top(chapters=4, chapter_length=15)

    return app


# app = create_app()

import os
from flask import Flask


def create_app():
    '''Flask package entry point. Create, initialize and return the
    applicaiton object.'''
    # create and configure the application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'songcat.db'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # stub route to test initialization
    @app.route('/test')
    def hello():
        return "This is a test for application {}".format(__name__)

    return app


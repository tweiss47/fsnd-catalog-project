import os
from flask import Flask


def create_app():
    '''Flask package entry point. Create, initialize and return the
    applicaiton object.'''
    # create and configure the application
    app = Flask(__name__, instance_relative_config=True)
    dbpath = os.path.join(app.instance_path, 'songcat.db')
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + dbpath,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # attach the database
    from . import model
    model.db.init_app(app)
    app.cli.add_command(model.init_model_command)
    app.cli.add_command(model.add_test_data)

    # register blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import catalog
    app.register_blueprint(catalog.bp)

    from . import api
    app.register_blueprint(api.bp)

    return app

import os
from flask import Flask
import click
from mp_feihu.settings import config

from mp_feihu.extensions import db
from mp_feihu.blueprints.api import api_bp
from mp_feihu.models import AddInfo



def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('mp_feihu')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_shell_context(app)
    return app

def register_extensions(app):
    db.init_app(app)

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, AddInfo=AddInfo)

def register_blueprints(app):
    app.register_blueprint(api_bp)

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            db.drop_all()
        db.create_all()
        click.echo('Initialized database.')
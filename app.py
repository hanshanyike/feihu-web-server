import os
import sys

import click
import json
from flask import Flask,request,make_response
from flask import redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# handlers
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, AddInfo=AddInfo)

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

# Models
class AddInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mailaddress = db.Column(db.String)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    hobby = db.Column(db.String)

    # optional
    def __repr__(self):
        return '<Note %r>' % self.phone

@app.route('/')
def index():
    #return render_template('index.html')
    return ("首页")

@app.route('/addinfo', methods=['get','POST'])
def new_AddInfo():
    data = json.loads(request.get_data().decode("utf-8"))
    if data and request.method == 'POST':
        addinfo = AddInfo(mailaddress=data['mailaddress'],address=data['address'],phone=data['phone'],hobby=data['hobby'])
        db.session.add(addinfo)
        db.session.commit()
        return make_response("add success")

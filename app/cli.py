import click
from flask.cli import with_appcontext
from .models import db


@click.command("create_db")
@with_appcontext
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Database tables created")

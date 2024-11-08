from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import click

engine = create_engine('sqlite:///database.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initalised the db')
def close_db(exception=None):
    db_session.remove()
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
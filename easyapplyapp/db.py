from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import click
from dotenv import load_dotenv
import os

load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ADDRESS = os.getenv("DB_ADDRESS")

engine = create_engine(f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ADDRESS}/initial_database')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_test_db(path):
    engine1 = create_engine(path)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine1))
    Base = declarative_base()
    Base.query = db_session.query_property()
    from . import models
    Base.metadata.create_all(bind=engine1)
    return db_session
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
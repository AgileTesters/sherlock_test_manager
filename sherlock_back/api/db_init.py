from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import exc
import sys

def initial_db_check():
    db_url = 'root:12345@127.0.0.1/sherlock'
    sqlalchemy_database_uri = 'mysql+pymysql://{}'.format(db_url)
    try:
        if not database_exists(sqlalchemy_database_uri):
            create_database(sqlalchemy_database_uri)
    except exc.OperationalError as e:
        print(e)
        sys.exit()

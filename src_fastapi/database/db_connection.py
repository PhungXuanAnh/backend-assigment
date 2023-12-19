import os
from sqlalchemy import orm
from sqlalchemy import create_engine
from controller.utilities import get_connection_string

conn = get_connection_string()

engine = create_engine(
    conn,
    pool_size=25,
    max_overflow=100,
    isolation_level="READ COMMITTED",
    connect_args={"connect_timeout": 10},
)

Session = orm.scoped_session(orm.sessionmaker(bind=engine))

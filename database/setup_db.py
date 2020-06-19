import config
import sqlalchemy as sa
import sqlalchemy_utils as sau
from database.schema import metadata

if __name__ == "__main__":
    engine = sa.create_engine(config.DATABASE_URL)
    if not sau.database_exists(engine.url):
        sau.create_database(engine.url)

    metadata.create_all(engine)

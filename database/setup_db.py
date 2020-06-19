import sqlalchemy as sa
import sqlalchemy_utils as sau
from database.schema import metadata

engine = sa.create_engine('mysql+pymysql://root:password@localhost:3306/quizbot')
if not sau.database_exists(engine.url):
    sau.create_database(engine.url)

metadata.create_all(engine)

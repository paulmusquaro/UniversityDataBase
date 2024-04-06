from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://postgres:blah_blah_blah@localhost:5432/witchcraft")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()



# docker run --name witchcraft -p 5432:5432 -e POSTGRES_PASSWORD=blah_blah_blah -d postgres
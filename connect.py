from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://postgres:blah_blah_blah@localhost:5432/witchcraft")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


# autocommit=False, autoflush=False, 
# docker run --name witchcraft -p 5432:5432 -e POSTGRES_PASSWORD=blah_blah_blah -d postgres
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DATABASE_URL
from sqlalchemy.orm import Session

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session():
    with Session(engine) as session:
        yield session
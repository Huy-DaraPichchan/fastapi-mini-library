from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database will be stored in a file named mini_library.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./mini_library.db"

# check_same_thread is Fase (only required when using sqlite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
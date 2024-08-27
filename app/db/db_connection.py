from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

# from .config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://postgres:postgres@postgres:5432/postgres"
)
# settings.database_url_psycopg2

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSession = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
metadata = Base.metadata

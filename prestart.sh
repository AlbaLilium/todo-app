USE_LOCAL_DB=False alembic revision --autogenerate -m "init database"
USE_LOCAL_DB=False alembic upgrade head
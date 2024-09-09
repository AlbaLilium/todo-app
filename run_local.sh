# python3 -m venv venv
# source venv/bin/activate
# pip install --no-cache-dir --upgrade -r requirements.txt
USE_LOCAL_DB=True alembic revision --autogenerate -m "init database"
USE_LOCAL_DB=True alembic upgrade head
USE_LOCAL_DB=True uvicorn main:app --port 8000  --reload

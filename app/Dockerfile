FROM tiangolo/uvicorn-gunicorn-fastapi:python3.12

#WORKDIR /app

COPY ../requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY .. .

#ENV MODULE_NAME=app.main
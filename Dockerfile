FROM python:3.10-bookworm

WORKDIR /app

ADD . /app/

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8000", "easyapplyapp:create_app()"]

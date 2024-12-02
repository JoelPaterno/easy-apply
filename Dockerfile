FROM python:3.10-bookworm

# Install system dependencies required for wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wget \
    fontconfig \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    wkhtmltopdf \
    xfonts-75dpi \
    xfonts-base \
    xvfb

WORKDIR /app

ADD . /app/

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8000", "easyapplyapp:create_app()"]

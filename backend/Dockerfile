FROM python:3.7.2
WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt
COPY . .

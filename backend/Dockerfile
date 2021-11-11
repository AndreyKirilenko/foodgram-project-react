FROM python:3.7.2
WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt
COPY . .
# CMD gunicorn api_foodgram.wsgi:application --bind 0.0.0.0:8000
# #CMD python3 manage.py runserver 0:8000
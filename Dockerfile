FROM python:3.9

RUN mkdir /code
WORKDIR /code

COPY requirements.txt ./
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY csv_poc csv_poc/
COPY migrations migrations/

EXPOSE 5000

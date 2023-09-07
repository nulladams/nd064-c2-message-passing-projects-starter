FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache gcc g++ musl-dev linux-headers geos libc-dev postgresql-dev libpq-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./app .

ENTRYPOINT ["python", "main.py"]
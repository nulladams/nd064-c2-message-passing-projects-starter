FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1

# WORKDIR /app
WORKDIR .

RUN apk add --no-cache gcc g++ musl-dev linux-headers geos libc-dev postgresql-dev libpq-dev
# COPY requirements.txt requirements.txt
# COPY wsgi.py wsgi.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# COPY ./app ./app

# RUN python -m grpc_tools.protoc -I./app --python_out=./app --grpc_python_out=./app ./app/person.proto

#RUN ls

#RUN echo "test ls"

EXPOSE 5000

#ENTRYPOINT ["python", "main.py"]

CMD ["flask", "run", "--host", "0.0.0.0"]
# CMD ["python", "main.py"]
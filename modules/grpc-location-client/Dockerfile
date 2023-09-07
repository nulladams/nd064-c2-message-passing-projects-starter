FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1

#RUN apk add --no-cache gcc g++ musl-dev linux-headers geos libc-dev postgresql-dev libpq-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./app .

RUN python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ location.proto

#RUN ls

#RUN echo "test ls"


ENTRYPOINT ["python", "main.py"]

#CMD ["flask", "run", "--host", "0.0.0.0"]
# CMD ["python", "main.py"]
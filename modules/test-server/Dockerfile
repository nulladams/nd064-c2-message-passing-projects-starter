FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1

#RUN apk add --no-cache gcc g++ musl-dev linux-headers geos libc-dev postgresql-dev libpq-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ test.proto

#RUN ls

#RUN echo "test ls"

EXPOSE 5021

ENTRYPOINT ["python", "main.py"]

#CMD ["flask", "run", "--host", "0.0.0.0"]
# CMD ["python", "main.py"]
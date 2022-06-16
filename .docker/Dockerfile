FROM python:3.8-slim

COPY . /ck-backend
WORKDIR /ck-backend
RUN apt update
RUN apt install -y build-essential libpq-dev 
RUN apt install -y libffi-dev
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirement.txt

ENV ENV=app-config 
ENTRYPOINT ["python", "app_grpc.py"]
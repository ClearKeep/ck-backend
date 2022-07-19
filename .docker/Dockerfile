FROM python:3.8-slim

COPY . /ck-backend
WORKDIR /ck-backend
RUN apt update
RUN apt install -y build-essential libpq-dev libffi-dev
RUN pip install --upgrade pip setuptools pipenv
RUN pipenv install

ENV ENV=app-config PATH="/ck-backend/.venv/bin:$PATH"
ENTRYPOINT ["python", "app_grpc.py"]
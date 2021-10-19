FROM python:3
COPY .. /clearkeep-backend
WORKDIR /clearkeep-backend
# setup library
RUN pip install --upgrade pip
RUN pip install -r requirement.txt
RUN pip install psycopg2
# generate protobuf
RUN sh protos/gen.sh
# start application
EXPOSE 5000
CMD python ./app.py
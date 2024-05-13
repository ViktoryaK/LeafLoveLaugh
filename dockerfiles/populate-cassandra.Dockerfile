FROM python:3.9-slim

COPY ./utils/populate_cassandra.py /opt/lll/
COPY ./data/plants_clean_40.csv /opt/lll/data/

RUN pip install cassandra-driver

WORKDIR /opt/lll/

ENTRYPOINT [ "python", "populate_cassandra.py" ]

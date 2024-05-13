FROM python:3.9-slim

COPY ./utils/populate_postgres.py /opt/lll/
COPY ./data/plants_clean_40.csv /opt/lll/data/

WORKDIR /opt/lll/

RUN pip install psycopg2-binary

ENTRYPOINT [ "python", "populate_postgres.py" ]
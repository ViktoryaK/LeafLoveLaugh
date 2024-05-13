FROM python:3.9-slim

COPY ./app/services/search/ /opt/lll/app/services/search/
COPY ./app/*.py /opt/lll/app/

RUN pip install fastapi cassandra-driver "uvicorn[standard]"

WORKDIR /opt/lll

ENTRYPOINT [ "uvicorn", "app.services.search.search:app", "--host", "0.0.0.0", "--port", "8080"]

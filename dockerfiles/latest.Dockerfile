FROM python:3.9-slim

COPY ./app/services/latest/ /opt/lll/app/services/latest/
COPY ./app/*.py /opt/lll/app/

RUN pip install fastapi aiokafka cassandra-driver "uvicorn[standard]"

WORKDIR /opt/lll

ENTRYPOINT [ "uvicorn", "app.services.latest.latest:app", "--host", "0.0.0.0", "--port", "8080"]

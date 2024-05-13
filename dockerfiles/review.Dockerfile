FROM python:3.9-slim

COPY ./app/services/review/ /opt/lll/app/services/review/
COPY ./app/*.py /opt/lll/app/

RUN pip install fastapi kafka-python cassandra-driver "uvicorn[standard]"

WORKDIR /opt/lll

ENTRYPOINT [ "uvicorn", "app.services.review.review:app", "--host", "0.0.0.0", "--port", "8080"]

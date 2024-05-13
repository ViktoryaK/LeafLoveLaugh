FROM python:3.9-slim

COPY ./app/services/catalog/ /opt/lll/app/services/catalog/
COPY ./app/*.py /opt/lll/app/

RUN pip install fastapi psycopg2-binary "uvicorn[standard]"

WORKDIR /opt/lll

ENTRYPOINT [ "uvicorn", "app.services.catalog.catalog:app", "--host", "0.0.0.0", "--port", "8080"]
